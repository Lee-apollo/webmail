# Create tables
import sqlite3
import db_config as config
# Create connection
db_conn = sqlite3.connect(config.DATABASE_NAME, check_same_thread=False)

# Get cursor
curs = db_conn.cursor()


def LOG(message):
    # print(message)
    return


class User():
    def __init__(self, login, name, user_id):
        self.login = login
        self.name = name
        self.user_id = user_id


class Message():
    user_id = None
    unread = None
    addr_to = None
    addr_from = None
    subject = None
    body = None

    # Init from tuple
    def __init__(self, input_data):
        if type(input_data) == dict:
            self.from_dict(input_data)
        else:
            self.from_tuple(input_data)

    def from_dict(self, input_dict):
        self.addr_from = input_dict["from"]
        self.addr_to = input_dict["to"]
        self.subject = input_dict["subject"]
        self.body = input_dict["body"]
        self.user_id = input_dict["user_id"]

    def from_tuple(self, input_tuple):
        (self.user_id,
         self.unread,
         self.addr_to,
         self.addr_from,
         self.subject,
         self.body) = input_tuple

    def as_tuple(self):
        return (self.user_id,
                self.unread,
                self.addr_to,
                self.addr_from,
                self.subject,
                self.body)

    def as_dict(self):
        return {"from": self.addr_from,
                "to": self.addr_to,
                "subject": self.subject,
                "body": self.body,
                "user_id": self.user_id}


def _create_table_users():
    # Create table
    cmd = '''CREATE TABLE `users` (
    `id` INTEGER primary key,
    `login` TEXT NOT NULL UNIQUE,
    `name` TEXT NOT NULL,
    `pass_hash` TEXT NOT NULL
    );'''
    LOG(cmd)
    curs.execute(cmd)
    db_conn.commit()


def _create_table_emails():
    # Create table
    cmd = '''CREATE TABLE `emails` (
    `id` INTEGER primary key,
    `user_id` INTEGER,
    `unread` INTEGER,
    `addr_to` TEXT NOT NULL,
    `addr_from` TEXT NOT NULL,
    `subject` TEXT NOT NULL,
    `body` TEXT NOT NULL
    );'''
    LOG(cmd)
    curs.execute(cmd)
    db_conn.commit()


def _create_tables():
    try:
        _create_table_users()
    except:
        LOG("Table 'users' already exists")
        pass

    try:
        _create_table_emails()
    except:
        LOG("Table 'emails' already exists")
        pass


def is_login_valid(login, pass_hash):
    cmd = '''SELECT * FROM users WHERE login = ? and pass_hash = ?;'''
    LOG(cmd)
    result = [row for row in curs.execute(cmd, (login, pass_hash))]

    if len(result) == 1:
        return True
    return False


def add_user(login, name, pass_hash):
    cmd = '''INSERT INTO users (login, name, pass_hash) VALUES (?, ?, ?);'''
    # % (login, name, pass_hash)
    print(cmd)
    curs.execute(cmd, (login, name, pass_hash))
    db_conn.commit()


def list_users():
    cmd = '''SELECT * FROM users'''
    print(cmd)
    for row in curs.execute(cmd):
        print(row)


def get_user_by_login(login):
    cmd = '''SELECT login, name, id FROM users WHERE login = ?'''
    result = [row for row in curs.execute(cmd, (login,))]
    print(result)
    if (len(result) == 1):
        return User(login=result[0][0],
                    name=result[0][1],
                    user_id=result[0][2])
    else:
        raise


def get_user_by_id(user_id):
    cmd = '''SELECT login, name, id FROM users WHERE id = ?'''
    result = [row for row in curs.execute(cmd, (user_id,))]
    print(result)
    if (len(result) == 1):
        return User(login=result[0][0],
                    name=result[0][1],
                    user_id=result[0][2])
    else:
        raise


def get_emails(user_id):
    cmd = '''SELECT * FROM emails WHERE user_id = ?'''

    # Create Message object from SQL response - skip first (id) column
    return [Message(row[1:]) for row in curs.execute(cmd, (user_id,))]


def get_emails_by_user(user):
    return get_emails(user.user_id)


def add_email(message):
    cmd = '''INSERT INTO emails
           (user_id, unread, addr_to, addr_from, subject, body)
           VALUES (?, ?, ?, ?, ?, ?);'''
    print(message.as_tuple())
    curs.execute(cmd, message.as_tuple())
    db_conn.commit()


def list_emails():
    cmd = '''SELECT * FROM emails'''
    print(cmd)
    for row in curs.execute(cmd):
        print(row)


def send_email(addr_from, addr_to, subject, body):

    if type(addr_to) != tuple and type(addr_to) != list:
        addr_to = (addr_to,)

    for addr in addr_to:
        try:
            username, domain = addr.split("@")
            print(username, domain)
            if domain != config.DOMAIN:
                continue
            user = get_user_by_login(username)

            msg = Message((user.user_id,
                           1,
                           addr,
                           addr_from,
                           subject,
                           body))
            add_email(msg)

        except Exception as e:
            print(str(e))

# Try to create table
_create_tables()

if __name__ == "__main__":
    list_users()
    add_user("Petr", "John Doe", "pass123")
    list_users()
    add_user("Master", "Zdenda", "123qwe")
    list_users()
    add_user("xyzSuperUser", "Jan", "pppp")
    list_users()

    list_emails()

    emails = [  # fake array of emails
             {"from": "Petr@fake-email.com",
              "to": "Petr@ztelesneny-neuspech.com",
              "subject": "Re: Hello world!",
              "body": "Hi mate. How are you?",
              "user": "Petr"
             },
             {"from": "spam@spam.com",
              "to": "Petr@ztelesneny-neuspech.com",
              "subject": "Buy this shit!",
              "body": "XYZ",
              "user": "Petr"
             },
             {"from": "mail@ztelezneny-neuspech.cz",
              "to": "Petr@ztelesneny-neuspech.com",
              "subject": "Welcome to the best site ever!",
              "body": "Hi Petr",
              "user": "Petr"
             }
    ]

    for email in emails:
        user = get_user_by_login(email["user"])

        message = Message((user.user_id,
                           1,
                           email["to"],
                           email["from"],
                           email["subject"],
                           email["body"]))
        add_email(message)
        list_emails()

    print("EMAILS:")

    for email in get_emails_by_user("Petr"):
        print(email.as_dict())

    db_conn.close()
