####################################################
# Imports
####################################################
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
# Class
####################################################


class AxcryotSoftware(object):
    @staticmethod
    def axcrypt_exe_path():
        return AXCRYPT_EXE

    @staticmethod
    def axcrypt_extenstion():
        return AXCRYPT_EXTENSION


class MessageHandler(object):
    @staticmethod
    def print_to_cli(message):
        try:
            print(message)
        except TypeError as error:
            print("Exception found in {f}, error:{e}".format(f=__name__, e=error))

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
        print("Cannot find Axcrypt install folder or executable : {ex}".format(ex=AXCRYPT_EXE))


def valid_path(path):
    if not os.path.exists(path):
        msg = "We could not find the path : '{path}' or its not accessible".format(path=path)
        raise argparse.ArgumentTypeError(msg)
    else:
        return path


def validate_number_of_args(args):
    global MIN_OF_ARGS_PROVIDED

    if len(args) > MIN_OF_ARGS_PROVIDED:
        return True
    else:
        MessageHandler.print_to_cli("Wrong number of arguments, should be at least: {n}".
                                    format(n=MIN_OF_ARGS_PROVIDED))
        exit(1)


def get_full_list_of_files_in_path(path):
    file_paths = []  # List which will store all of the full file path.
    files_to_ignore = ['Thumbs.db', 'desktop.ini', '.dropbox', 'DS_Store']
    # Walk the tree.
    for root, directories, files in os.walk(path):
        for filename in files:
            # Join the two strings in order to form the full file path.
            if filename not in files_to_ignore:
                file_path = os.path.join(root, filename)
                file_paths.append(file_path)  # Add it to the list.

    return file_paths  # Self-explanatory.

