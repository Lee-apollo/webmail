# Create tables
import sqlite3


# Create connection
db_conn = sqlite3.connect('example.db')

# Get cursor
curs = db_conn.cursor()

def LOG(message):
    print(message)
    return

def create_table_users():
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

#messages = Table("messages", metadata,
#    Column('id', Integer, primary_key=True),
#    Column('user_id', Integer),
#    Column('unread', Integer),
#    Column('addrTo', Text),
#    Column('addrFrom', Text),
#    Column('subject', Text),
#    Column('body', Text)
#    )

def create_table_emails():
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


def create_tables():
    try:
        create_table_users()
    except:
        LOG("Table 'users' already exists")
        pass

    try:
        create_table_emails()
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

def is_login_valid_old(login, pass_hash):
    cmd = '''SELECT * FROM users WHERE login = '%s' and pass_hash = '%s';''' % (login, pass_hash)
    LOG(cmd)
    result = [row for row in curs.execute(cmd)]
    print(result)

    if len(result):
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

def get_user_id(login):
    cmd = '''SELECT * FROM users WHERE login = ?'''
    result = [row for row in curs.execute(cmd, (login,))]
    if (len(result) == 1):
        return result[0][0]
    raise
    
def get_emails(user_id):
    cmd = '''SELECT * FROM emails WHERE user_id = ?'''
    return [row for row in curs.execute(cmd, (user_id,))]


def get_emails_by_user(login):
    user_id = get_user_id(login)
    return get_emails(user_id)


class Message():
    id
    user_id
    unread
    addrTo
    addrFrom
    subject
    body


    def as_tuple(self, sqlRow):
        return (self.user_id, self.unread, self.addr_to, self.addr_from, self.subject, self.body)

    def from_tuple(self, sqlRow):
        (self.user_id, self.unread, self.addr_to, self.addr_from, self.subject, self.body) = sqlRow

    def as_dict(self):
        (self.user_id, self.unread, self.addr_to, self.addr_from, self.subject, self.body) = sqlRow

        return {"from"    : self.add_from,
                "to"      : self.addr_to,
                "subject" : self.subject,
                "body"    : self.body,
                "user_id" : self.user_id
                }


def add_email(addr_from, addr_to, subject, body, user_id):
    cmd = '''INSERT INTO emails 
           (user_id, unread, addr_to, addr_from, subject, body)
           VALUES (?, 1, ?, ?, ?, ?);'''
    curs.execute(cmd, (user_id, addr_to, addr_from, subject, body))
    db_conn.commit()

def list_emails():
    cmd = '''SELECT * FROM emails'''
    print(cmd)
    for row in curs.execute(cmd):
        print(row)



# Try to create table
create_tables()

if __name__=="__main__":
    list_users()
    #add_user("Petr", "John Doe", "pass123")
    #list_users()
    #add_user("Master", "Zdenda", "123qwe")
    #list_users()
    #add_user("xyzSuperUser", "Jan", "pppp")
    #list_users()

    list_emails()

    emails = [ # fake array of emails
        { "from" : "Petr@fake-email.com",
          "to": "Petr@ztelesneny-neuspech.com",
          "subject" : "Re: Hello world!",
          "body" : "Hi mate. How are you?",
          "user" : "Petr"
        },
        { "from" : "spam@spam.com",
          "to": "Petr@ztelesneny-neuspech.com",
          "subject" : "Buy this shit!",
          "body" : "XYZ",
          "user" : "Petr"
        },
        { "from" : "mail@ztelezneny-neuspech.cz",
          "to": "Petr@ztelesneny-neuspech.com",
          "subject" : "Welcome to the best site ever!",
          "body" : "Hi Petr",
          "user" : "Petr"
        }
    ]
    
    #for email in emails:
    #    add_email(email["from"], email["to"], email["subject"], email["body"], get_user_id(email["user"]))
    #    list_emails()

    print("EMAILS:")

    print(get_emails_by_user("Apollo"))

    db_conn.close()

#engine = create_engine('sqlite:///test.db')#
#
#)

#users = Table("users", metadata,
#    Column('id', Integer, primary_key=True),
#    Column('username', Text, unique=True),
#    Column('passwd', Text),
#    Column('name', Text)
#    )


