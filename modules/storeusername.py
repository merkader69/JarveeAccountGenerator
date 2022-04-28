from .config import Config, ASSET_DIR


def store(username): 
    file = open(ASSET_DIR + '/accounts.txt', 'a+')
    print("storing credentials")
    file.write(username + ', \n')
    file.close()
    print("stored")

