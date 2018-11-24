import pymysql


if __name__ == '__main__':
    print('attempting connection')
    conn = pymysql.connect(host='sql3.freemysqlhosting.net', user='sql3264960', port=3306, db='sql3264960', passwd='4qkCEeX9j6')

    cursor = conn.cursor()

    print('requesting topics')
    cursor.execute("select * from topics;")

    print(cursor.description)

    for row in cursor:
        print(row)

    cursor.close()
    conn.close()


'''
freemysqlhosting.net creds:
    u/n: scott.kemperman@gmail.com
    pwd: (KBjR8u!IJ9TYWnB

Server: sql3.freemysqlhosting.net
Name: sql3264960
Username: sql3264960
Password: 4qkCEeX9j6
Port number: 3306
'''


