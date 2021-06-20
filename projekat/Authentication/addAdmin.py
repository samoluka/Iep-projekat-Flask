import pymysql

from models import User, database

from configuration import Configuration


def createAdmin():
    connection = pymysql.connect(host='localhost',
                                 port=3306,
                                 user='root',
                                 password='root',
                                 database='authentication',
                                 cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        sql = "SELECT * FROM users WHERE email=%s"
        cursor.execute(sql, ('admin@admin.org',))
        result = cursor.fetchone()
        if (not result):
            sql = "INSERT INTO users (email, password,forename,surname,role,jmbg) VALUES ('admin@admin.org', '1','admin','admin','admin','000000000000')"
            cursor.execute(sql)
        connection.commit()
    return


if __name__ == '__main__':
    createAdmin()
