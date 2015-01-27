#!/usr/bin/python3

from bitcoin.rpc import RawProxy
from os.path import expanduser
import os
import sys

rpc_interface = RawProxy() # Intitialize/Construct(?) the imported function to use the rpc interface

def help():
	print('Theese are the available commands:\n')
	print('help\t- this help function')
	print('create\t- create a new multi signature bitcoin address')
	print('spend\t- spend from a multi signature bitcoin address (not available yet)')
	print('exit\t- terminate the program\n')

def account_exists(account_name): # Check if the account name is valid
	check_name = rpc_interface.getaddressesbyaccount(account_name) # Request addresses in the given account

	if not check_name: # If bitcoind returns an empty list
		print('This account name has not been used.')
		return False

	else:
		print('This account name exists in bitcoind.')
		return True

def create_multisig(account_name): # Function for generating a new multisig address
	new_address = [] # A list to store the addresses returned from bitcoind
	public_key = [] # To store the public keys returned from bitcoind
	private_key = [] # To store the private keys returned from bitcoid

	print('\nIMPORTANT:\n')
	print('Theese are the private keys associated with this multisig address. You need to WRITE THEM DOWN!\n')

	for i in range(3): # Request new addresses from bitcoind
		new_address.append(rpc_interface.getnewaddress(account_name)) # Request a new address

		address_info = rpc_interface.validateaddress(new_address[i]) # Request the public key

		public_key.append(address_info['pubkey']) # Get the key itself from the returned dictionary

		private_key.append(rpc_interface.dumpprivkey(new_address[i])) # Get the private key

		print('\n' + private_key[i] + '\n')

	multisig = rpc_interface.createmultisig(2, public_key) # Generate the multisig address
	
	rpc_interface.addmultisigaddress(2, public_key, account_name) # Add the multisig address to the wallet

	return multisig # Return a dictionary containing the address and the redeemScript

def write_file(account_name, content): # Function to write the redeemScript and the address to a file
	directory = expanduser('~') + '/bitcoind-tool/' + account_name + '/'

	if not os.path.exists(directory): # If the directory does not exist, create it
		os.makedirs(directory)

		print('Created the directory ' + directory)

	else:
		print('The directory ' + directory + ' already exists on the system.')

	filename = directory + account_name + '.multisig' # This will be the name of the file created
	the_file = open(filename, 'w') # This opens the file for writing
	the_file.write(content['address'] + '\n') # This writes the address to the file
	the_file.write(content['redeemScript'])
	the_file.close() # Closes the file

	return filename

print('bitcoind-tool 0.1.3\n')
run = True

while run == True:
	choice = input('Type a command (help): ')

	if choice == 'help':
		help() # Print the help function

	elif choice == 'create':
		check_account = True

		while check_account:
			account_name = input('Specify a name for the multisig address: ')
			check_account = account_exists(account_name) # Check if the account name is taken

		multisig_info = create_multisig(account_name)

		print('\nThe newly created address:\n' + multisig_info['address'])
		print('\nWill now create a file with the rest of the necessary information.\n')

		file_location = write_file(account_name, multisig_info)

		print('\nDone. Created ' + file_location + '\n')

	elif choice == 'exit':
		sys.exit(0)

	else:
		print('Invalid command.')
