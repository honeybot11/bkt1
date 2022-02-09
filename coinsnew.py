#---------------------- ADWATCHER --------------------
import os
#os.system("pip install SAmino==1.9.2")
#os.system("pip install pyfiglet")
from samino import Client
from samino import Local
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from os import path
import pyfiglet
from progress.bar import IncrementalBar
import json
THIS_FOLDER = path.dirname(path.abspath(__file__))
emailfile=path.join(THIS_FOLDER,"accounts.json")
dictlist=[]

with open(emailfile) as f: 
    dictlist = json.load(f)

def adwatcher(client : Client):
   coins = client.get_wallet_info().totalCoins
   print("\n \033[0;37m ❯ Coin Balance before adwatching: " + f"{coins}" + "\033[0;0m \n")
   bar = IncrementalBar('    Adwatching', max=200)
   for _ in range(200):
      Thread(target=client.watch_ad).start()
      bar.next()
   bar.finish()
   coins = client.get_wallet_info().totalCoins
   print("\n \033[0;37m ❯ Coin Balance after adwatching: " + f"{coins}" + "\033[0;0m \n")

def log(cli : Client,email : str, password : str, device : str):
        cli.login(email=email,password=password)
        print("\n \033[0;32;40m ❯ Logged in: " + email + " \033[0;0m")
        print("\n \033[0;32;40m ❯ DeviceID: " + device + " \033[0;0m")


def task(client : Client):
   adwatcher(client)
def threadit(acc : dict):
    email=acc["email"]
    password=acc["password"]
    device=acc["device"]
    client=Client(deviceId=device)
    log(cli=client,email=email,password=password, device=device)
    print("""\n \033[0;30;43m ❯ Starting adwatcher... \033[0;0m""")
    task(client)
    print("""\n \033[0;32;40m ❯ Finished adwatching! \033[0;0m""")

def main():
    f = pyfiglet.figlet_format("Adwatcher", font="standard")
    print("\033[0;32m" + f + "\033[0;0m")
    print("                                    \033[0;30;45m by: Kapidev \033[0;0m \n")
    print("\033[0;30;42m ❯ Successfully loaded " + f"{len(dictlist)}" + " accounts! \033[0;0m")
    for amp in dictlist:
    	threadit(amp)
    print("""\n \033[0;30;42m ❯ Finished adwatching on all accounts! \033[0;0m""")
 
if __name__ == '__main__':
    main()