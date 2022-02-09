bloglink="http://aminoapps.com/p/wth7tqq"
import amino
import time
from os import path
import json
THIS_FOLDER = path.dirname(path.abspath(__file__))
emailfile=path.join(THIS_FOLDER,"accounts.json")
dictlist=[]
with open(emailfile) as f:
    dictlist = json.load(f)

#dicklis=dictlist.reverse()
def log(cli : amino.Client,email : str, password : str):
    try:
        cli.login(email=email,password=password)
    except Exception as e:
        print(e)
pass

def threadit(acc : dict):
    email=acc["email"]
    password=acc["password"]
    device=acc["device"]
    client=amino.Client(deviceId=device)
    log(cli=client,email=email,password=password)
    print(f"Logged In {email}")
    xd=client.get_from_code(bloglink)
    id=xd.objectId
    cid=xd.path[1:xd.path.index("/")]
    client.join_community(cid)
    subclient=amino.SubClient(comId=cid,profile=client.profile)
    coin=int(client.get_wallet_info().totalCoins)
    print("Total Coins in wallet : "+str(coin))
    if coin>500 and coin!=0:
      N=int(coin/500)
      for _ in range(N):
        subclient.send_coins(coins=500,blogId=id)
        print("\033[1;32m500 coins sent")
        print(f"\033[1;33mNow {client.get_wallet_info().totalCoins} coins in  {email} ")
    time.sleep(10)
    pass
    coins=int(client.get_wallet_info().totalCoins)
    print("Total Coins in wallet : "+str(coins))
    if coins!=0:
     print("\033[1;32Coins on the way")
     if coins!=0 and coins<500 or coins==500:
       subclient.send_coins(coins=coins,blogId=id)
       print(f"Transferred {coins} COINS")
    pass  
    time.sleep(25)
    
def main():
    print(f"\n\33[48;5;5m\33[38;5;234m  {len(dictlist)} ACCOUNTS LOADED  \33[0m\33[48;5;235m\33[38;5;5m \33[0m")
    for amp in dictlist:
        threadit(amp)
    print(f"\n\n\33[48;5;5m\33[38;5;234m Transferred all coins from {len(dictlist)} ACCOUNTS  \33[0m\33[48;5;235m\33[38;5;5m \33[0m")
                 
if __name__ == '__main__':
    main()