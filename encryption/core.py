import helpers
import sys
import argparse
import os
####################################################
# Functions
####################################################

def encrypt_files (files):



def cloud_prepare(src, dst, enc_password, enc_key_path):
    # get list of all files
    # run over the list and : A.encrypt B. Copy to destionation C. clean source encrypted file
    list_of_src_files = helpers.get_full_list_of_files_in_path(src) # list of files = full path + file name + original file name [in case encrypted]
    list_of_dst_files = helpers.get_full_list_of_files_in_path(dst)
    encrypt_files(list_of_src_files)
    return True


def pre_run_validation():
    helpers.validate_supported_os()
    helpers.validate_axcrytp_installed()
    helpers.validate_number_of_args(sys.argv)

def arg_parser():
    parser = argparse.ArgumentParser(description='Pre-Cloud encryption')
    subparsers = parser.add_subparsers(help='Lets encrypt',dest="subparser_name")
    parser_a = subparsers.add_parser('encrypt', help='Encrypt files and copy to destination folder utilty')
    parser_a.add_argument('source', help='Source folder', type=helpers.valid_path)
    parser_a.add_argument('destination', help='Destination folder', type=helpers.valid_path)
    parser_a.add_argument('encryption_password', help='Set Encryption password')
    parser_a.add_argument('encryption_key_path', help='Encryption key path', type=helpers.valid_path)
    parser_a.add_argument('--silent', help='Silent mode run, used to execute program automaticly from task scheduler \n'\
                                         'Using password from memory if such exists', type=helpers.is_encryption_password_in_memory)

    parser_b = subparsers.add_parser('Maintaince_commands', help='Optional commands for the encrypt utility')
    parser_b.add_argument('--get_encryption_password', help='Get encryption password from memory', action='store_true')
    parser_b.add_argument('--clear_encryption_password', help='Clear encryption password from memory', action='store_true')
    parser_b.add_argument('--set_encryption_password', help='Set encryption password to memory', action='store_true')

    args = parser.parse_args()

    if (args.subparser_name == "encrypt"):
        _src = args.source
        _dst = args.destination
        _enc_key_path = args.encryption_key_path
        if (args.silent):
            _enc_password = helpers.get_encrpytion_password()
        else:
            _enc_password = args.encryption_password
        cloud_prepare (_src, _dst, _enc_password, _enc_key_path)

    elif (args.subparser_name == "Maintaince_commands"):
        # Handle optional params related to password
        if args.clear_encryption_password:
            helpers.clean_encrpytion_password()
            exit(0)

        if args.get_encryption_password:
            print (helpers.get_encrpytion_password())
            exit(0)

        if args.set_encryption_password:
            helpers.set_encrpytion_password_cli()
            exit(0)
    else:
        print("Unexpected error")

####################################################
# Runner
####################################################

pre_run_validation()
arg_parser()
