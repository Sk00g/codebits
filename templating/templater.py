"""
*IMPORTANT* - This class should only be responsible for TEXT MANIPULATION and logic. Not graphical representation

Maintains state across calls to 'parse_input', so use multiple instances if required
"""

import re
from enums import *


class Templater:
    def __init__(self):
        self.previous_text = ""
        self.topics = []
        self.chunks = []
        self.btype = CodebitType.CHILL

    """
    Core method. Take in a string. Return a dict object of the following format: 
    {
        "altered_text": ...,
        "partial_command": (start, end),
        "new_topics": [...],
        "removed_topics": [...],
        "new_chunks": (start, end, enums.Chunk.*),
        "codebit_type": enums.CodebitType.*    
    }
     
    """
    def parse_input(self, text: str):
        original_topics = self.topics.copy()
        original_chunks = self.chunks.copy()


        # Find and replace template commands
        full_cmd = re.findall(r":[\-]?[CTPLA]? .{3,}:>|:<[CPLARHI]", text)
        if full_cmd:
            text = self._register_command(text, text.index(full_cmd[0]), full_cmd.pop())

        # Highlight partial commands
        partial_cmd = re.findall(r':[\-<]?[CTPLA]?$|:[\-<]?[CTPLA] .*:?$', text)
        if partial_cmd:
            start = text.index(partial_cmd[0])
            partial_cmd = (start, start + len(partial_cmd[0]))

        # create topics automatically from capitalized words
        words = re.findall(r"[a-zA-Z0-9-_]+", text)
        capitalized_words = [w.rstrip(" /=-_") for w in re.findall(r"[A-Z][A-Za-z0-9]{3,}[ /=\-_]|[A-Z][A-Za-z0-9]{3,}$", text)]
        for word in capitalized_words:
            # Ignore words capitalized at the start
            if text.count(word) == 1 and text.index(word) == 0:
                continue
            self._add_topic(word, False)

        # remove topics that were implicit and are no longer present
        implicit_topics = [kvp[0] for kvp in original_topics if not kvp[1]]
        removed_topics = [t for t in implicit_topics if not t in words[1:]]
        for topic in removed_topics:
            self._remove_topic(topic)

        self.previous_text = text
        return dict(
            altered_text=text,
            partial_command=partial_cmd,
            new_topics=[kvp[0] for kvp in self.topics if kvp not in original_topics],
            removed_topics=[kvp[0] for kvp in original_topics if kvp not in self.topics],
            new_chunks=[chunk for chunk in self.chunks if chunk not in original_chunks],
            codebit_type=self.btype
        )

    """
    Gathers all the data from the last string of parse calls and returns a dictionary of this data
    for the database engine to generate and write SQL. Also clears the data and performs some cleanup
    operations.
    """
    def generate_snapshot(self):
        data = dict(
            text=self.previous_text.strip(' \t\n'),
            topics=[tup[0] for tup in self.topics],
            chunks=self.chunks,
            codebit_type=self.btype
        )

        self.clear_state()

        return data

    """
    Resets all state fields that are maintained across parse calls.
    """
    def clear_state(self):
        self.previous_text = ""
        self.topics = []
        self.chunks = []
        self.btype = CodebitType.CHILL

    # --- Helper Methods ---

    def _register_command(self, text, index, cmd: str):
        print('registering command')

        # Execute dataless command
        if cmd[1] == '<':
            if cmd[2] == TECommand.REMINDER:
                self.btype = CodebitType.REMINDER
            elif cmd[2] == TECommand.CHILL:
                self.btype = CodebitType.CHILL
            elif cmd[2] == TECommand.IMPORTANT:
                self.btype = CodebitType.IMPORTANT
            else:
                raise Exception("attempting to register invalid command: %s" % cmd)

            return text[:index]

        strip_count = 1 if cmd[1] not in ['-', '<'] else 2
        core = cmd[strip_count:]

        # Command with body
        if core[0] in [CHUNK_TYPE.keys()]:
            chunk = (index, len(core[:-2]), CHUNK_TYPE[core[0]])
            self.chunks.append(chunk)
        elif core[0] == TECommand.TOPIC:
            print('adding topic %s' % core[2:-2])
            self._add_topic(core[2:-2], True)

        # Return with command remove or just edges removed
        if cmd[1] == '-':
            return text[:index]
        else:
            return text[:index] + text[index + strip_count + 1] + text[-2]

    def _add_topic(self, topic, explicit):
        if not (topic, explicit) in self.topics:
            self.topics.append((topic, explicit))

    def _remove_topic(self, topic):
        self.topics.remove((topic, False))

    # levenshtein_distance
    def _string_distance(self, string1: str, string2: str):
        # base case: empty strings
        if len(string1) == 0:
            return len(string2)
        if len(string2) == 0:
            return len(string1)

        # test if last characters of the strings match
        cost = 0 if string1[-1] == string2[-1] else 1

        # return minimum of delete char from s, delete char from t, and delete char from both
        return min(self._string_distance(string1[:-1], string2) + 1,
                   self._string_distance(string1, string2[:-1]) + 1,
                   self._string_distance(string1[:-1], string2[:-1]) + cost)