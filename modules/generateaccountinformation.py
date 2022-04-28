import requests
import random
import string 

import os
import emoji
import random
import spintax
import logging

from fake_useragent import UserAgent

from modules.tumblr_username_grabber import grab_usernames

logger = logging.getLogger(__name__)


def emoji_select():
    with open("txts/emojis.txt", 'r') as f:
        emojis = f.readlines()
    random.shuffle(emojis)
    rand_emoji = emoji.emojize(emojis[0], use_aliases=True).strip('\n')
    rand_int = random.randint(1, 2)
    if rand_int == 1:
        return rand_emoji * random.randint(1, 2)
    else:
        return ''


name = ''  # var, will define as global in function below


def firstname():
    global name
    # create multiple lists/arrays consisting of first name/nicknames and shuffle
    names = (['natalie', 'nattie', 'natty', 'natt', 'nat'],
             ['anna'],
             ['juliann', 'julianna', 'julia'],
             ['kelli', 'kel'])

    # print(names[0][0])  # multiple arrays, to access specific array use names[int]
    # to access a specific name use names[int][int], example: names[0][3] to access the name 'natty'

    # randomly pick array below

    rand_choices = random.choices(names, weights=[0.2, 0.2, 0.2, 0.2], k=1)
    rand_choice = rand_choices[0][0]
    # ^ in order to use random shuffle on multiple arrays, you have to use the index
    char_list = ['a', 'n', 'j', 'k']
    website = 'https://www.snapchat.com/add/'  # add snapchat username here

    for char in char_list:
        if rand_choice[0].startswith(char):
            if char == 'a':
                website += 'annaxbanana6'
            elif char == 'n':
                website += 'nattiewood'
            elif char == 'j':
                website += 'jreilly424'
            elif char == 'k':
                website += 'klepage68'
        else:
            pass

    # randomly choose between capitalization of name
    capital_pick = random.choice(['true', 'true', 'false'])
    if capital_pick == 'true':
        # convert name string to list then back to string after capitalizing first character
        l = list(rand_choice)
        if l[0] == 'n':
            del (l[0])
            name = 'N' + "".join(l)  # changing back to string for use

        elif l[0] == 'a':
            del (l[0])
            name = 'A' + "".join(l)  # changing back to string for use

        elif l[0] == 'j':
            del (l[0])
            name = 'J' + "".join(l)  # changing back to string for use

        elif l[0] == 'k':
            del (l[0])
            name = 'K' + "".join(l)  # changing back to string for use

    elif capital_pick == 'false':
        name = rand_choice
    # the global variable 'name' now contains our final name, now just randomly add !//!! and/or emoji to the end

    rand_ast = ['', '', '!', '!!']  # lazy attempt at making the empty entries more likely to be chosen
    random.shuffle(rand_ast)

    name = name + rand_ast[0]

    return name, rand_choice, website  # second thing we're returning here is name without !, emojis, etc.


username = ''  # var, will define as global in function below
surname = ''  # same as above ^


def ig_user():
    global username
    global surname

    user_select = firstname()
    for_user = user_select[1]  # use this var to help create username
    first_name = user_select[0]
    website_url = user_select[2]

    rand_ext = ['.', '_']

    rand_choice = random.choice(['true', 'false'])
    if rand_choice == 'true':  # aka, use . and/or _ in username for Instagram
        username = ''.join('%s%s' % (x, random.choice(rand_ext) if random.random() > 0.5 else '') for x in for_user)
    else:
        username = for_user

    # now figure out which girl was chosen by accessing for_user var then do appropriate action depending on choice
    if str(for_user).startswith('n'):
        surname = random.choice(['wood', 'woody', 'w', 'W'])
    elif str(for_user).startswith('a'):
        surname = random.choice(['thomas', 't', 'T'])
    elif str(for_user).startswith('j'):
        surname = random.choice(['reilly', 'reills', 'r', 'R'])
    elif str(for_user).startswith('k'):
        surname = random.choice(['lepage', 'l', 'L'])

    if username.strip()[-1] == '.' or username.strip()[-1] == '_':
        username = username + surname
    else:
        x = random.randint(0, 3)
        rand_seperator = ['.', '._', '_.', '_', '__', '1']
        random.shuffle(rand_seperator)
        if x == 2:
            username = username + rand_seperator[0] + surname + rand_seperator[1]
        else:
            username = username + rand_seperator[0] + surname + str(random.randint(15, 999))
    if username.strip()[-1] == '.' or username.strip()[-1] == '_':
        username = username.strip()[-1]

    with open("txts/bio.txt", 'r', encoding="utf8") as f:  # gives error if not opened with utf8 encoding
        bios = f.readlines()  # big list of bios inside of a .txt file

    random.shuffle(bios)  # shuffle it, then access index -> 0 like so: bios[0] for random bio each run.
    rand_seperator = ['', ' ', '- ', '-- ', '--- ', '~ ', '~~ ', '/ ', '// ']
    random.shuffle(rand_seperator)

    # lets now randomly choose whether or not we want to lowercase the entire bio

    bio = ''
    _emoji = emoji_select()
    if for_user.startswith('n'):
        user = 'nattiewood'  # <-- snapchat username
        spin_text = spintax.spin(
            '{add me on snapchat|amosc|add my snap|add me on sc|sc}{: |; |~ }') + user + ' ' + _emoji
        bio = bio + '\n' + rand_seperator[0] + spin_text
    elif for_user.startswith('a'):
        user = 'annaxbanana6'  # <-- snapchat username
        spin_text = spintax.spin(
            '{add me on snapchat|amosc|add my snap|add me on sc|sc}{: |; |~ }') + user + ' ' + _emoji
        bio = bio + '\n' + rand_seperator[0] + spin_text

    elif for_user.startswith('j'):
        user = 'jreilly424'  # <-- snapchat username
        spin_text = spintax.spin(
            '{add me on snapchat|amosc|add my snap|add me on sc|sc}{: |; |~ }') + user + ' ' + _emoji
        bio = bio + '\n' + rand_seperator[0] + spin_text
    elif for_user.startswith('k'):
        user = 'klepage68'  # <-- snapchat username
        spin_text = spintax.spin(
            '{add me on snapchat|amosc|add my snap|add me on sc|sc}{: |; |~ }') + user + ' ' + _emoji
        bio = bio + '\n' + rand_seperator[0] + spin_text
    return username, first_name, bio, website_url


first_name = ''


def pic_select(name):
    global first_name
    if str(name).lower().startswith('n'):
        first_name = 'natalie'
    elif str(name).lower().startswith('a'):
        first_name = 'anna'
    elif str(name).lower().startswith('j'):
        first_name = 'julianna'
    elif str(name).lower().startswith('k'):
        first_name = 'kelli'
    pic_list = []
    file_path = ''.format(first_name)
    for path, dirs, files in os.walk(file_path):
        for f in files:
            if f.endswith('.jpg') or f.endswith('.png'):
                vps_path = ''.format(first_name).format(first_name)
                pic_list.append(vps_path + f)
    random.shuffle(pic_list)
    # shuffle list and pick a random picture
    return pic_list[0]


# ge
def generatePassword():
    password = str('')
    return password


# def genEmail(size=random.randint(6, 12), chars=string.ascii_lowercase + str(random.randint(1, 99999))):
#     return ''.join(random.choice(chars) for _ in range(size)) + '@mail.com'


def _emailPick():
    with open('txts/mail_ru.txt', 'r') as f:
        emails = f.readlines()

    return emails[0].strip('\n')


def grabEmail():
    """Grabs email and then deletes used email from .txt file."""
    email = _emailPick()
    with open('txts/mail_ru.txt', 'r+') as f:
        t = f.read()
        to_delete = email.strip()  # input EMAIL
        f.seek(0)
        for line in t.split('\n'):
            if line != to_delete:
                f.write(line + '\n')
        f.truncate()
    return email  # finally, return chosen email(that is now deleted from .txt file to prevent reuse)


def genUsername():
    funcs = random.choice([ig_user, grab_usernames])
    if funcs == ig_user:
        user = ig_user()
        usr = user[0]
        first_n = user[1]
        bio = user[2]
        return usr, first_n, bio
    else:
        user = ig_user()
        usr = grab_usernames()  # username will not be user[0] in this case, grab username from tumblr function
        first_n = user[1]
        bio = user[2]
        return usr, first_n, bio


def jarvee(n):
    x = 0
    while True:
        while x < n:
            file = 'jarvee_import.txt'

            user = genUsername()
            usr = user[0]

            if duplicates(usr, file) is True:  # if duplicate found(True)
                print('Duplicate found: {0}'.format(usr))
                continue
            if available(usr) is False:  # if not available(False)
                print('User not available: {0}'.format(usr))
                continue

            x += 1  # will only increment if duplicates/available passes without errors
            full_name = user[1]
            bio = user[2]
            profile_pic = pic_select(full_name)
            email_pass = grabEmail().split(":")
            email_usr, email_pw = email_pass
            if len(usr) == 0 or len(usr) == 1:
                while True:
                    user = genUsername()
                    usr = user[0]
                    full_name = user[1]
                    bio = user[2]
                    profile_pic = pic_select(full_name)
                    if len(usr) == 0 or len(usr) == 1:
                        continue
                    else:
                        break
            proxy = None
            check = proxy_checker(proxy)  # to check if proxy works
            if check is False:
                continue

            format_str = '{email},{accountusername},{accountpassword},{proxyip}:{proxyport},{proxyusername},{proxypassword},{full_name},{website_url},{biography},{gender},{isprivate},{phone},{profilePicture},{emailpassword},{emailServer}'.format(
                email=email_usr,
                accountusername=usr,
                accountpassword=generatePassword(),
                proxyip=proxy,
                proxyport=proxy_port,
                proxyusername=proxy_user + proxy_arg,
                proxypassword=proxy_pw,
                full_name=full_name,
                website_url='',
                biography=bio.lstrip('\n'),
                gender='F',
                isprivate='Yes',  # set to No if not private profile
                phone='',
                profilePicture=profile_pic,
                emailpassword=email_pw,
                emailServer='imap.mail.ru')
            with open(file, 'a', encoding='utf-8') as append_acc:
                append_acc.writelines(format_str + '\n')
        else:
            break


def duplicates(user, file):
    """Function to check for duplicate strings in .txt
    :param user: the username of chosen account
    :param file: the .txt of file to check
    :return: True if duplicate is found, otherwise False
    """
    with open(file, 'r', encoding='utf-8') as file_read:
        lines = file_read.read().splitlines()
    line_list = []
    for line in lines:
        line_list.append(line.split(','))
    return any(user in sl for sl in line_list)


def available(user):
    """Checks if username is available
    :param user: chosen instagram username
    :return: False if username is not available, otherwise True
    """
    ua = UserAgent()
    query = '/_validate_username?username={}'.format(str(user))
    heroku_host = 'http://insta-node.herokuapp.com'
    headers = {'Accept': '*/*',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'en-US,en;q=0.9',
               'User-Agent': ua.random,
               'Referer': 'https://www.instagramavailability.com/',
               'Origin': 'https://www.instagramavailability.com',
               'Connection': 'keep-alive',
               'Host': 'insta-node.herokuapp.com'}
    resp = requests.get(heroku_host + query, headers=headers).json()
    return resp['valid']


def proxy_checker(proxy):
    """Function to check if proxy is valid. (working)"""
    try:
        proxies = {'http': 'http://{}'.format(proxy),
                   'https': 'http://{}'.format(proxy)}
        s = requests.Session()
        chrome_ua = UserAgent().chrome
        headers = {'User-Agent': chrome_ua}
        result = s.get('http://httpbin.org/ip', headers=headers, proxies=proxies)

        if result.status_code == 200:
            return True
        else:
            return False
    except(requests.exceptions.Timeout, requests.exceptions.ConnectTimeout, requests.RequestException)as e:
        logger.error(e)
        return False


def clear_file(file=None):
    """To clear jarvee_import.txt (optional)."""
    if file is None:
        file = 'jarvee_import.txt'
    with open(file, 'w+'):
        pass


if __name__ == '__main__':
    # print(duplicates('hostageofyourlovee', 'jarvee_import.txt'))
    clear_file()
    jarvee()
