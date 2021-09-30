import subprocess
import re

bitcoin_cli = 'bitcoin-cli'
addresses = []

def normalize_output(output):
    str_out = str(output)
    num = re.sub("[^0123456789\.]", "", str_out)
    return num

def get_balance(wallet_name='std_wallet'):
    rpc_wallet_cmd = '-rpcwallet=' + wallet_name
    res = subprocess.check_output([bitcoin_cli, 
                                   '-regtest', 
                                   rpc_wallet_cmd, 
                                   'getbalance'])
    return normalize_output(res)

def create_new_address(wallet_name='std_wallet'):
    rpc_wallet_cmd = '-rpcwallet=' + wallet_name
    res = subprocess.check_output([bitcoin_cli, 
                                   '-regtest', 
                                   rpc_wallet_cmd, 
                                   'getnewaddress'])
    print(res)
    addresses.append(res.decode())
    return res.decode()

def list_avail_addr(wallet_name='std_wallet'):
    print("Addresses created in current session" + 
                "\n---------------------------------------------------------")
    for idx, val in enumerate(addresses):
        print("Addr #", idx + 1, ": ", val)
    print("---------------------------------------------------------")

def list_unspent(confirmed=True, wallet_name='std_wallet'):
    rpc_wallet_cmd = '-rpcwallet=' + wallet_name
    if (confirmed):
        res = subprocess.check_output([bitcoin_cli, 
                                       '-regtest', 
                                       rpc_wallet_cmd,
                                       'listunspent'])
    else:
        res = subprocess.check_output([bitcoin_cli, 
                                       '-regtest', 
                                       rpc_wallet_cmd,
                                       'listunspent', 
                                       '0'])
    return res

def send_to_address(addr, amount, wallet_name='std_wallet'):
    rpc_wallet_cmd = '-rpcwallet=' + wallet_name
    res = subprocess.check_output([bitcoin_cli, 
                                   '-regtest', 
                                   rpc_wallet_cmd, 
                                   'sendtoaddress', 
                                   addr, 
                                   amount])

def help_menu():
    print("Following options are available: ")
    print("(a) Check the balance")
    print("(b) Create a new address")
    print("(c) Send bitcoins to the address")
    print("(d) List unspend transactions")
    print("(h) Show help menu")
    print("(quit) Exit program")

if __name__ == '__main__':
    quit = 'quit'
    cmd = ''

    help_menu()

    while(cmd != quit):
        cmd = input().lower()
        if(cmd == 'a' or cmd == '(a)'):
            print("Specify wallet:")
            wal = input()
            balance = get_balance(wal)
            print("Balance of wallet ", wal, ": ", balance)
        if(cmd == 'b' or cmd == '(b)'):
            print("Specify wallet:")
            wal = input()
            addr = create_new_address(wal)
            print("Address ", addr, " created and added to session...")
        if(cmd == 'c' or cmd == '(c)'):
            list_avail_addr()
            print("Specify address by index:")
            index = int(input()) - 1
            print("Specify sending wallet:")
            wallet = input()
            print("Specify amount")
            amount = input()
            addr = addresses[index]
            send_to_address(addr, amount, wallet)
            print(amount, " sent to ", addr, "...")
        if(cmd == 'd' or cmd == '(d)'):
            print("Do you want to include unconfirmed transactions in output?(y/n)")
            y_n = input().lower()
            if(y_n == 'y'):
                res = list_unspent(False)
                print("Summary (including unconfirmed transactions): ")
                print(res)
            else:
                res = list_unspent(True)
                print("Summary (excluding unconfirmed transactions): ")
        if(cmd == 'h' or cmd == '(h)'):
            help_menu()
