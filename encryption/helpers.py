####################################################
# Imports
####################################################
import keyring
import getpass
import os
import sys
import argparse

####################################################
# Constants definition
####################################################

SUPPORTED_OS = 'nt'
SUPPORTED_OS_PRINT = 'Windows'
KEYRING_SERVICE_NAME = 'pre-cloud-enc'
KEYRING_USER_NAME = 'cloud'
AXCRYPT_EXE = os.environ['ProgramW6432']+'\Axantum\AxCrypt\AxCrypt.exe'
AXCRYPT_EXTENSION = '.axx'
ENCRYPTION_PASSWORD = ''
ENCRYPTION_PASSWORD_ARGV_LEN = 3
SOURCE_PATH = ''
DESTINATION_PATH = ''
MIN_OF_ARGS_PROVIDED = 1

####################################################
# Functions
####################################################


def print_help():
    print("Help will be here")
    sys.exit("Help printed")


def validate_supported_os():
    if not os.name == SUPPORTED_OS:
        print("Using unsupported OS : '{current}', currently only '{supp}' is supported".
              format(current=os.name, supp=SUPPORTED_OS_PRINT))


def validate_axcrytp_installed():
    if not os.path.isfile(AXCRYPT_EXE):
        print("Cannot find Axcrypt installtion folder or executable : {ex}".format(ex=AXCRYPT_EXE))


def valid_path(path):
    if not os.path.exists(path):
        msg = "We could not find the path : '{path}' or its not accessible".format(path=path)
        raise argparse.ArgumentTypeError(msg)
    else:
        return path


def get_encrpytion_password():
    return keyring.get_password(KEYRING_SERVICE_NAME, KEYRING_USER_NAME)


def is_encryption_password_in_memory():
        if get_encrpytion_password() is not None:
            return True
        else:
            return False


def set_encrpytion_password_cli():
    keyring.set_password(KEYRING_SERVICE_NAME, KEYRING_USER_NAME, getpass.win_getpass("Please type the password:"))


def clean_encrpytion_password():
    try:
        if is_encryption_password_in_memory() is True:
            keyring.delete_password(KEYRING_SERVICE_NAME, KEYRING_USER_NAME)
    except keyring.errors.PasswordDeleteError:
         print ("Unable to clean encryption password")


def set_encrpytion_password(password):
    keyring.set_password(KEYRING_SERVICE_NAME, KEYRING_USER_NAME, password)


def handle_encryption_password():
    ENCRYPTION_PASSWORD = get_encrpytion_password()
    if ENCRYPTION_PASSWORD is None:
        print("It seems like no password is configured for user '{usr}', lets configure it first"
              .format(usr=KEYRING_USER_NAME))
        set_encrpytion_password()
    return ENCRYPTION_PASSWORD


def validate_number_of_args(args):
    global MIN_OF_ARGS_PROVIDED

    if (len(args)> MIN_OF_ARGS_PROVIDED):
        return True;
    else:
        exit (1)


def get_full_list_of_files_in_path(path):
    file_paths = []  # List which will store all of the full filepaths.

    # Walk the tree.
    for root, directories, files in os.walk(path):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            file_path = os.path.join(root, filename)
            if ((os.path.splitext(filename)[1]) == AXCRYPT_EXTENSION):
                # reverse the file, replace - with . and revse back
                original_file_name = os.path.splitext(filename)[0][::1].replace('-','.',1)[::1]
            else:
                original_file_name = filename
            file_paths.append([file_path,filename,original_file_name])  # Add it to the list.

    return file_paths  # Self-explanatory.

