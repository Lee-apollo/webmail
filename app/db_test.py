from db_interface import add_user, is_login_valid, list_users, get_emails_by_user, list_emails


def hash(passwd):
    return passwd

if __name__ == "__main__":

    list_users()
       
    print("EMAILS:")
    list_emails()

    
    emails = get_emails_by_user("Apollo")
    print(emails)

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


