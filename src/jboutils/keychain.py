from getpass import getpass

import keyring


def get_username(service):
    return keyring.get_password(service, "username")


def get_password(service):
    return keyring.get_password(service, "password")


def get_creds(service):
    return (get_username(service), get_password(service))


def get_creds_interactive(service, question):
    """
    @param question: A string which can have either "username" or "password" injected to it to display to the user so that they enter the appropriate value
    """
    username = get_username(service)
    passwd = get_password(service)

    if username is None:
        username = getpass(question.format("username")).strip("\n")
        keyring.set_password(service, "username", username)

    if passwd is None:
        password = getpass(question.format(password)).strip("\n")
        keyring.set_password(service, "password", username)

    return username, passwd


def wipe_creds(service):
    try:
        keyring.delete_password(service, "username")
        keyring.delete_password(service, "password")
    except:
        pass
