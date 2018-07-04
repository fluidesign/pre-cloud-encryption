import helpers
import sys
import argparse
import subprocess
import os
import enum
import shutil
####################################################
# Constants definition
####################################################
AXCRYPT_EXTENSION = '.axx'
####################################################
# Class


class Params(enum.Enum):

    ACTION = "action"
    ENCRYPT = "encrypt"
    DECRYPT = "decrypt"
    SOURCE_PATH = "source"
    DESTINATION_PATH = "destination_path"


class UserArgv(object):
    def __init__(self, argv):

            self.__args = self.__handle_arg_parser(argv)
            self.__action = self.__handle_action(self.__args.subparser_name)
            self.__source = self.__args.source
            self.__destination = self.__args.destination

    def __handle_arg_parser(self, argv):
        try:
            parser = argparse.ArgumentParser(description='Pre-Cloud encryption')
            subparsers = parser.add_subparsers(help='Choose action', dest="subparser_name")
            parser_a = subparsers.add_parser('encrypt', help='Encrypt files and copy to destination folder utilty')
            parser_a.add_argument('source', help='Source folder', type=helpers.valid_path)
            parser_a.add_argument('destination', help='Destination folder', type=helpers.valid_path)

            parser_b = subparsers.add_parser('decrypt', help='Decrypt files and copy to destination folder utilty')
            parser_b.add_argument('source', help='Source folder', type=helpers.valid_path)
            parser_b.add_argument('destination', help='Destination folder', type=helpers.valid_path)

            return parser.parse_args()
        except argparse.ArgumentError as error:
            helpers.MessageHandler.print_to_cli("Exception occured during argument parser, error:{e}".format(e=error))
            helpers.MessageHandler.print_to_cli("Must to exit")
            exit(1)

    def __handle_action(self, received_action_from_user):
        actions = (Params.ENCRYPT.value, Params.DECRYPT.value)
        if received_action_from_user in actions:  # need to fix this shit
            return received_action_from_user
        else:
            helpers.MessageHandler.print_to_cli("Unknown actions, must be one of the following: {a}".format(a=actions))
            exit(1)

    def return_action(self):
        if self.__action:
            return self.__action
        else:
            helpers.MessageHandler.print_to_cli("Object yet initilized, unexpected")
            exit(1)

    def return_source(self):
        if self.__source:
            return self.__source
        else:
            helpers.MessageHandler.print_to_cli("Object yet initilized, unexpected")
            exit(1)

    def return_destination(self):
        if self.__destination:
            return self.__destination
        else:
            helpers.MessageHandler.print_to_cli("Object yet initilized, unexpected")
            exit(1)

####################################################
####################################################
# Functions
####################################################


def move_encrypted_file_to_cloud_folder(src_file, dest_file_path):
    # Example:
    # source : c:\\home\\user
    # destination: d:\\cloud
    # sub folders : \\test\pictures\holiday
    return_bool = False
    try:  # create destination folder tree and copy file
        if os.path.exists(dest_file_path):
            helpers.MessageHandler.print_to_cli("Unexpected behavior, encrypted file found in destination,"
                                                " Destination Path: {p}".format(p=dest_file_path))
        else:
            destination_dir_path = os.path.dirname(dest_file_path)
            helpers.MessageHandler.print_to_cli("Creating required path tree on destination path: {d}".
                                                format(d=destination_dir_path))
            os.makedirs(destination_dir_path, exist_ok=True)
            shutil.move(src_file, dest_file_path)
    except OSError as error:
        helpers.MessageHandler.print_to_cli("Exception during file copy from: {f}, to: {t}. error: {e}".
                                            format(f=src_file, t=dest_file_path, e=error))

    try:
        if os.path.exists(dest_file_path):
            helpers.MessageHandler.print_to_cli("File: {f} copied succesfully to cloud folder".
                                                format(f=dest_file_path))
            return_bool = True
        else:
            helpers.MessageHandler.print_to_cli("Unexpected behavior, File: {f} was NOT copied to cloud folder".
                                                format(f=dest_file_path))
    except OSError as error:
        helpers.MessageHandler.print_to_cli("Exception during destination file verification: {d}, error: {e}".
                                            format(d=dest_file_path, e=error))

    return return_bool


def get_future_encrypted_file_path(path):
    # Example of a duplicate in a folder:
    # hello1.txt
    # hello1-txt.axx
    # replace original ext to -<ext>.<axx>
    try:
        file_name, ext = os.path.splitext(path)
        ext_modified = ext.replace('.', '-')
        axx_ext = helpers.AxcryotSoftware.axcrypt_extenstion()
        return "{f}{e}{ex}".format(f=file_name, e=ext_modified, ex=axx_ext)
    except OSError as error:
        helpers.MessageHandler.print_to_cli("Exception during getting future encrypted file path: {p}, error: {e}".
                                            format(p=path, e=error))


def prepare_for_cloud(source_list, params_dict):
    action = params_dict[Params.ACTION.value]
    source_root_path = params_dict[Params.SOURCE_PATH.value]
    destination_root_path = params_dict[Params.DESTINATION_PATH.value]
    number_of_files_for_action = len(source_list)
    number_of_files_created_after_action = 0
    helpers.MessageHandler.print_to_cli("\nExecuting action: {a} \non source folder: {s} \nand copy files to: {d}".
                                        format(a=action, s=source_root_path, d=destination_root_path))
    if action == Params.ENCRYPT.value:
        set_default_passphrase = [helpers.AxcryotSoftware.axcrypt_exe_path(), '-e', '-a', '-b', '22']
        if subprocess.call(set_default_passphrase) == 0:
            helpers.MessageHandler.print_to_cli("Encrypting using configured pass phrase")
        else:
            helpers.MessageHandler.print_to_cli("You must set default pass phrase to continue, exit now")
            exit(1)
        for source_file in source_list:
            encrypted_file_path = get_future_encrypted_file_path(source_file)
            if os.path.exists(encrypted_file_path):
                helpers.MessageHandler.print_to_cli("File: {f}, already exists in destination folder,"
                                                    " nothing to do here".format(f=encrypted_file_path))
            else:
                helpers.MessageHandler.print_to_cli(
                    "Action: {a} on File: {f}".format(a=action, f=source_file))
                encrypt_files = [helpers.AxcryotSoftware.axcrypt_exe_path(), '-b', '22', '-c', '-z', source_file]
                if subprocess.call(encrypt_files) == 0:
                    destination_file_path = str(encrypted_file_path.replace(source_root_path, destination_root_path))
                    helpers.MessageHandler.print_to_cli("File: {f} {a}, about to copy to destination folder: {d}".
                                                        format(f=source_file, a=action, d=destination_file_path))
                    if move_encrypted_file_to_cloud_folder(encrypted_file_path, destination_file_path):
                        number_of_files_created_after_action += 1
                else:
                    print("NOK")
                    exit(1)
    else:
        helpers.MessageHandler.print_to_cli("Under development")

    if number_of_files_for_action == number_of_files_created_after_action:
        helpers.MessageHandler.print_to_cli("\nAll files succssfully prepared for cloud")
    else:
        helpers.MessageHandler.print_to_cli("\nSome files failed. Source file count:{s}, Succesfully prepared: {d}".
                                        format(s=number_of_files_for_action, d=number_of_files_created_after_action))

    return True


def unique_list_of_files(source_list, destination_list):  # assume right is the encrypted
    try:
        exclude_list = []
        include_list = []
        for right in destination_list:
            right_base_name = os.path.basename(right)
            right_base_name_without_axx_ext = os.path.splitext(right_base_name)[0][::1]
            ind = right_base_name_without_axx_ext.rfind("-")
            right_base_name_fixed_ext = right_base_name_without_axx_ext[:ind] + "." + right_base_name_without_axx_ext[ind + 1:]
            right_folder_name = os.path.basename(os.path.dirname(right))
            exclude_list.append("{folder}\{file}".format(folder=right_folder_name, file=right_base_name_fixed_ext))

        for left in source_list:  # left list should not include any encrypted files
            left_base_name = os.path.basename(left)
            left_folder_name = os.path.basename(os.path.dirname(left))
            include = "{folder}\{file}".format(folder=left_folder_name, file=left_base_name)
            include_ext = os.path.splitext(include)[1]
            if (include_ext != helpers.AxcryotSoftware.axcrypt_extenstion()) and (include not in exclude_list):
                include_list.append(left)

    except IOError as error:
        helpers.MessageHandler.print_to_cli("An exception received in function: {f}, error: {e}".
                                            format(f=__name__, e=error))
        exit(1)

    return include_list


def build_list_of_files_for_action(args_dict):
    try:
        action = args_dict["action"]
        if action == Params.ENCRYPT.value:
            # list of files = full path + file name + original file name [in case encrypted]
            list_of_src_files = helpers.get_full_list_of_files_in_path(args_dict[Params.SOURCE_PATH.value])
            list_of_dst_files = helpers.get_full_list_of_files_in_path(args_dict[Params.DESTINATION_PATH.value])
            unique_list = unique_list_of_files(list_of_src_files, list_of_dst_files)
            return unique_list
        elif action == Params.DECRYPT.value:
            helpers.MessageHandler.print_to_cli("Under development")
            return None
        else:
            helpers.MessageHandler.print_to_cli("Unknown action: {a}".format(a=action))
    except Exception as error:
        helpers.MessageHandler.print_to_cli("An exception received in function: {f}, error: {e}".
                                            format(f=__name__, e=error))
        exit(1)


def pre_run_validation():
    helpers.validate_supported_os()
    helpers.validate_axcrytp_installed()
    helpers.validate_number_of_args(sys.argv)


def arg_parser():
    user_args_dict = {}
    user_args = UserArgv(sys.argv)
    user_args_dict[Params.ACTION.value] = user_args.return_action()
    user_args_dict[Params.SOURCE_PATH.value] = user_args.return_source()
    user_args_dict[Params.DESTINATION_PATH.value] = user_args.return_destination()

    return user_args_dict

def print_list_of_files_to_prepare(list_of_files):
    user_choise = input('''\n\nWould you like to view the list of files we're about to prepare: [y/n]''')
    if user_choise.capitalize() == "Y":
        counter = 1
        for file in list_of_files:
            helpers.MessageHandler.print_to_cli("{c}: {f}".format(c=counter, f=file))
            counter = counter + 1


####################################################
# Runner
####################################################

if __name__ == '__main__':
    list_of_files_for_action = []
    arg_dict = {}
    pre_run_validation()
    arg_dict = arg_parser()
    list_of_files_for_action = (build_list_of_files_for_action(arg_dict))
    number_of_files_for_action = len(list_of_files_for_action)
    if number_of_files_for_action > 0:
        helpers.MessageHandler.print_to_cli("Preparing {l} file/s for cloud".format(l=number_of_files_for_action))
        print_list_of_files_to_prepare(list_of_files_for_action)
        prepare_for_cloud(list_of_files_for_action, arg_dict)
    else:
        helpers.MessageHandler.print_to_cli("No new files found to prepare for cloud")
else:
    helpers.MessageHandler.print_to_cli("Kindly execute the app directly via command line")
    exit(0)
