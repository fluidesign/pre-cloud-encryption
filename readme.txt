##########################################################
Idea forked from:
	https://github.com/raulcano/goodsync-encryption
	Script Name: GoodSync-Encrypt-Decrypt.bat
	Author: Raul Cano Argamasilla
	Email: raul.cano.argamasilla@gmail.com
	Date: 14.10.2013
##########################################################

Requirements:
  AxCrypt (Windows version)
  Python version 3.6 and above
	 
Description: 
This script is used in order to keep a remote encrypted repository of 
ALL the files in a local directory. The synchronization is kept between
the local files (not encrypted) and the remote copies (encrypted).
To avoid saving any plain passwords, during the encryption/decryption process a user will be asked to provide with a password and/or key.

Typical use case:
1.The user creates a job to be synced with a cloud repository (or another folder, whatever).
2.Every time the job is run, all the files on that folder are automatically encrypted and the originals are deleted temporarily, leaving the encrypted versions only in the local directory.
3.The analysis and comparison of versions is done among only the encrypted files in both sides(L   and R).
4a.If changes are detected, the corresponding files will be synced (either uploaded or downloaded)  
4b.If no changes are detected, nothing happens.
5.Finally, the local files are decrypted back in the local directory, leaving only plain
  unencrypted files there (no encrypted files will remain at this point).

How to use:
1. Help : [Route_to_script\]core.py -h
1.a You can add -h at any stage for additional help topic
2. Encrypt : [Route_to_script\]core.py encrypt <source_path> <destination_path>
3. Decrypt : [Route_to_script\]core.py decrypt <source_path> <destination_path>


Future development:
1. GUI
2. Extended support for:
2.a Fully automated encryption/decryption process
2.b Logging