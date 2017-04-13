from db_interface import send_email, list_emails, list_users

list_emails()
list_users()
send_email(addr_from = "sender@test.com",
           addr_to = "a@test.com",
           subject = "Hello",
           body = "Hi mate! How are you?")

list_emails()
