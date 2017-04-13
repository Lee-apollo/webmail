from db_interface import add_user, is_login_valid, list_users
from db_interface import get_emails_by_user, list_emails, get_user


def hash(passwd):
    return passwd

if __name__ == "__main__":

    print("Users:")
    list_users()

    print("Emails:")
    list_emails()

    user = get_user(1)
    print(user.name)
    print(user.login)
    print(user.id)

    exit(0)

    emails = get_emails_by_user("Petr")
    for email in emails:
        email.as_dict()

    login = input("User name:")
    pass_hash = hash(input("Password:"))

    if is_login_valid(login, pass_hash):
        print("Login valid")
    else:
        print("Login INVALID")

    if is_login_valid_old(login, pass_hash):
        print("Login valid")
    else:
        print("Login INVALID")
