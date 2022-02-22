import argparse
import backend as bc

manager = bc.Manager()

parser = argparse.ArgumentParser(description = 'Программа для работы с судовым интернетом')
parser.add_argument('-pm', '--price_monitor', action = 'store_true',
help = 'Write argument -pm or --price_monitor if you want monitor price. If you get value equal 0,45$, sound will be started')
parser.add_argument('-c', '--connect', action = 'store_true',
help = 'You will connect to internet')
parser.add_argument('-cm', '--connection_monitor', action = 'store_true',
help = 'It will monitor your internet access')
parser.add_argument('-sp', '--set_password', type = str,
help = 'Set your password. It wiil keep in separate file')
parser.add_argument('-su', '--set_user', type = str,
help = 'Set your user_name. It will keep in separate file')
parser.add_argument('-d', '--disconnect', action = 'store_true',
help = 'It will disconnect internet')
parser.add_argument('-rt', '--remaining', action = 'store_true',
help = 'It will check remaining time')
parser.add_argument('-cp', '--check_price', action = 'store_true',
help = 'It will print price for internet')


args = parser.parse_args()

def analize(price_monitor = False, connect = False,
connection_monitor = False, set_password = None,
set_user = None, disconnect = False, remaining = False,
check_price = False):
	print(args)
	print(price_monitor)
	if price_monitor == True:
		manager.price_monitor()
	if connect == True:
		manager.connect()
	if connection_monitor == True:
		manager.connection_monitor()
	if disconnect == True:
		manager.disconnect()
	if remaining == True:
		manager.check_remaining()
	if set_user != None:
		manager.set_user(set_user)
	if set_password !=None:
		manager.set_password(set_password)
	if check_price == True:
		manager.price_check()

if __name__ == '__main__':
	analize(args.price_monitor, args.connect, args.connection_monitor, args.set_password, args.set_user, args.disconnect, args.remaining, args.check_price)
	
