#!/usr/bin/python3

from bitcoin.rpc import RawProxy
import os
import code
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

	for i in range(3): # Request new addresses from bitcoind
		new_address.append(rpc_interface.getnewaddress(account_name)) # Request a new address
		print('DEBUG: ' + new_address[i])

		address_info = rpc_interface.validateaddress(new_address[i]) # Request the public key

		public_key.append(address_info['pubkey']) # Get the key itself from the returned dictionary
		print('DEBUG: ' + public_key[i])

		private_key.append(rpc_interface.dumpprivkey(new_address[i])) # Get the private key
		print('DEBUG: ' + private_key[i])

	multisig_address = rpc_interface.createmultisig(2, public_key) # Generate the multisig address
	
	rpc_interface.addmultisigaddress(2, public_key, account_name) # Add the multisig address to the wallet

	return multisig_address

print('bitcoind-tool 0.1.2\n')
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

		print(multisig_info)

	elif choice == 'exit':
		sys.exit(0)

	else:
		print('Invalid command.')
