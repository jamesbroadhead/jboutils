"""
Provides a standard interface to the 'keyring' package, storing both username and password for services

Usage:
  keychain add SERVICE
  keychain add_json SERVICE FILE
  keychain delete SERVICE
  keychain rm SERVICE

Options:
  -h --help     Show this screen.
"""
from base64 import b64decode, b64encode
from getpass import getpass
import json
import pickle

import docopt
import keyring

USERNAME = "username"
PASSWORD = "password"
DATA = "data"


def get_username(service):
    return _get(service, USERNAME)


def get_password(service):
    return _get(service, PASSWORD)


def get_creds(service):
    return (get_username(service), get_password(service))


def write_creds_interactive(service, question=None):
    """
    @param question: A string which can have either "username" or "password" injected to it to display to the user so that they enter the appropriate value
    """
    if question is None:
        question = 'For service "%s", please enter your {}: ' % (service,)

    username = getpass(question.format(USERNAME)).strip("\n")
    keyring.set_password(service, USERNAME, username)

    password = getpass(question.format(PASSWORD)).strip("\n")
    keyring.set_password(service, PASSWORD, password)

    return username, password


def wipe_creds(service):
    try:
        keyring.delete_password(service, USERNAME)
        keyring.delete_password(service, PASSWORD)
    except:
        pass


def get_json_data(service):
    return _get_serialized_data(json.loads, service)


def get_pickle_data(service):
    return _get_serialized_data(b64_pickle_loads, service)


def write_json_data(service, data):
    return _write_serialized_data(json.dumps, service)


def write_pickle_data(service, data):
    return _write_serialized_data(b64_pickle_dumps, service, data)


def b64_pickle_dumps(data):
    pickled = pickle.dumps(data)
    return b64encode(pickled)


def b64_pickle_loads(data):
    pickled = b64decode(data)
    return pickle.loads(pickled)


# internal


def _get(service, key):
    val = keyring.get_password(service, key)
    if val is None:
        raise ValueError(
            f'keychain: The value for service "{service}", key "{key}" is empty!'
        )
    return val


def _get_data(service):
    return _get(service, DATA)


def _get_serialized_data(deserialize_func, service):
    """ @param deserialize_func: a single-arg func which takes a str/bytes"""
    try:
        serialized = _get_data(service)
    except ValueError:
        return None
    return deserialize_func(serialized)


def _write_data(service, data):
    keyring.set_password(service, DATA, data)


def _write_serialized_data(serialize_func, service, data):
    """ @param serialize_func: a single-arg func which takes a str/bytes"""
    data_str = serialize_func(data)
    return _write_data(service, data_str)


# main


def main():
    args = docopt.docopt(__doc__)

    if args["add"]:
        write_creds_interactive(args["SERVICE"])
    elif args["add_json"]:
        with open(args["FILE"]) as fh:
            _write_data(args["SERVICE"], fh.read())
    else:
        wipe_creds(args["SERVICE"])
