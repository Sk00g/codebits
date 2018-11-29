"""
data = dict(
            text=self.previous_text.strip(' \t\n'),
            topics=[tup[0] for tup in self.topics],
            chunks=self.chunks,
            codebit_type=self.btype
        )
"""
import pymysql
from enums import *
from model import Codebit, Chunk


class DataEngine:
    def __init__(self):
        # Type lists here because I'm lazy, should probably pull from DB
        self.codebit_types = {
            CodebitType.REMINDER: 1,
            CodebitType.CHILL: 2,
            CodebitType.IMPORTANT: 3
        }

        self.chunk_types = {
            ChunkType.PLAIN_TEXT: 1,
            ChunkType.QUOTE: 2,
            ChunkType.PHONE_NUMBER: 3,
            ChunkType.CODE: 4,
            ChunkType.CLI: 5,
            ChunkType.CREDENTIALS: 6,
            ChunkType.LINK: 7,
            ChunkType.DATE: 8,
            ChunkType.TIME: 9,
            ChunkType.ADDRESS: 10,
        }

    def _get_conn(self):
        return pymysql.connect(host='sql3.freemysqlhosting.net', user='sql3264960', port=3306,
                               db='sql3264960', passwd='4qkCEeX9j6')

    def insert_codebit(self, data):
        print(data)

        codebit = Codebit(data['text'], [], [], data['codebit_type'])

        # Tuple(start, end, enums.Chunk.*)
        codebit.chunks = [Chunk(codebit, ch[2], ch[0], ch[1]) for ch in data['chunks']]
        codebit.topics = data['topics']

        # insert codebit then chunk then topic junctions
        with self._get_conn() as conn:
            sql = "insert into codebits (codebitType_id, content) values (%d, '%s');" % \
                  (self.codebit_types[codebit.ctype], codebit.content)
            conn.execute(sql)
            conn.execute("select LAST_INSERT_ID();")
            for row in conn:
                codebit_id = row
                break

            if codebit.chunks:
                sql = "insert into chunks (startIndex, endIndex, chunkType_id, codebit_id) values "
                for chunk in codebit.chunks:
                    sql += "(%d, %d, %d, %d), " % (chunk.start, chunk.end, self.chunk_types[chunk.ctype], codebit_id)
                sql = sql[:-2] + ";"
                rows = conn.execute(sql)
                print('rows: %d' % rows)

            if codebit.topics:
                sql = "insert into codebit_topic_jnc values "

                for topic in codebit.topics:
                    topic_id = None

                    lsql = "select id from topics where name = '%s';" % topic
                    match = conn.execute(lsql)
                    print('match: %d' % match)
                    if match == 0:
                        lsql = "insert into topics values (NULL, '%s');" % topic
                        conn.execute(lsql)
                        conn.execute("select LAST_INSERT_ID();")
                    for row in conn:
                        print('row: %s' % row)
                        topic_id = row

                    print('codebit_id: %s' % type(codebit_id))
                    print('topic_id: %s' % type(topic_id))
                    sql += "(%d, %d), " % (codebit_id[0], topic_id[0])

                sql = sql[:-2] + ";"
                print(sql)
                rows = conn.execute(sql)
                print('rows: %d' % rows)

            print('finished')






