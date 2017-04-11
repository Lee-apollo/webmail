# Create tables
from sqlalchemy import *

engine = create_engine('sqlite:///test.db')

metadata = MetaData()

users = Table('users', metadata,
     Column('id', Integer, primary_key=True),
     Column('name', String),
     Column('fullname', String),
)

addresses = Table('addresses', metadata,
   Column('id', Integer, primary_key=True),
   Column('user_id', None, ForeignKey('users.id')),
   Column('email_address', String, nullable=False)
  )



users = Table("users", metadata,
    Column('id', Integer, primary_key=True),
    Column('username', Text, unique=True),
    Column('passwd', Text),
    Column('name', Text)
    )

messages = Table("messages", metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer),
    Column('unread', Integer),
    Column('addrTo', Text),
    Column('addrFrom', Text),
    Column('subject', Text),
    Column('body', Text)
    )

users.create(engine)
messages.create(engine)