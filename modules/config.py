"""
    this is for configuration files
    notes: check assets/proxies.txt to use your custom proxies.
 """
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSET_DIR = os.path.join(BASE_DIR, 'assets')

Config = {
    "bot_type": 1,  # change to 2 to use python requests
    "password": "",
    "use_custom_proxy": True,  # default is False change to True to use a file containing multiple proxies of yours.
    "proxy_username": "",
    "proxy_password": "",
    "amount_of_account": 10,  # amount of account you want to create make sure it doesnt exceed 50 for better performance
    "amount_per_proxy": 1,  # this would be amount of account used if you have a you are using multiple proxies
    "proxy_file_path": ASSET_DIR + "/proxies.txt"

}
