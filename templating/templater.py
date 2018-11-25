"""
*IMPORTANT* - This class should only be responsible for TEXT MANIPULATION and logic. Not graphical representation

Maintains state across calls to 'parse_input', so use multiple instances if required
"""

from templating.enums import *


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
        "new_topics": [...],
        "removed_topics": [...],
        "new_chunks": (start, end, enums.Chunk.*),
        "codebit_type": enums.CodebitType.*    
    }
     
    """
    def parse_input(self, text: str):
        original_topics = self.topics.copy()
        original_chunks = self.chunks.copy()

        lines = text.split('\n')
        words = []
        for line in lines:
            words.extend(line.split(' '))

        # create topics automatically from capitalized words
        capitalized_words = [word for word in words if len(word) > 2 and word[0].isupper() and word != words[-1] and word != words[0]]
        for word in capitalized_words:
            self._add_topic(word, False)

        # remove topics that were implicit and are no longer present
        implicit_topics = [kvp[0] for kvp in original_topics if not kvp[1]]
        removed_topics = [t for t in implicit_topics if text.find(t) == -1]
        for topic in removed_topics:
            self._remove_topic(topic)

        self.previous_text = text
        return dict(
            altered_text=text,
            new_topics=[kvp[0] for kvp in self.topics if kvp not in original_topics],
            removed_topics=[kvp[0] for kvp in original_topics if kvp not in self.topics],
            new_chunks=[chunk for chunk in self.chunks if chunk not in original_chunks],
            codebit_type=self.btype
        )

    # --- Helper Methods ---

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