from time import sleep
from random import randint

import modules.config as config
# importing generated info
import modules.generateaccountinformation as accnt
from modules.generateaccountinformation import duplicates, proxy_checker,  available
from modules.storeusername import store
from modules.selenium_proxy_auth import get_chromedriver
# library import
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import requests
import re
import logging
import datetime
logger = logging.getLogger(__name__)


class AccountCreator:
    def __init__(self, use_custom_proxy):
        self.sockets = []
        self.use_custom_proxy = use_custom_proxy
        self.url = 'https://www.instagram.com/'
        self.__collect_sockets()

    def __collect_sockets(self):
        r = requests.get("https://www.sslproxies.org/")
        matches = re.findall(r"<td>\d+.\d+.\d+.\d+</td><td>\d+</td>", r.text)
        revised_list = [m1.replace("<td>", "") for m1 in matches]
        for socket_str in revised_list:
            self.sockets.append(socket_str[:-5].replace("</td>", ":"))

    def createaccount(self, proxy, n):
        """Create accounts.
        :proxy: should be a dict if containing user/pw auth
        """
        options = webdriver.ChromeOptions()
        # options.add_argument('--proxy-server=%s' % proxy) # [ONLY WORKS IF NO AUTH]
        x = 0
        while x < n:
            try:
                file = 'jarvee_import.txt'

                account = accnt.genUsername()
                username = account[0]
                name = account[1]

                if duplicates(username, file) is True:  # if duplicate found(True)
                    print('Duplicate found: {0}'.format(username))
                    continue
                if available(username) is False:  # if not available(False)
                    print('User not available: {0}'.format(username))
                    continue
                proxy_string = '{user}:{password}@{host}:{port}'.format(
                    user=proxy['username'],
                    password=proxy['password'],
                    host=proxy['address'],
                    port=proxy['port']
                )
                check = proxy_checker(proxy_string)  # to check if proxy works
                if check is False:
                    print('Proxy failed, retrying...')
                    continue
                x += 1
                driver = get_chromedriver(use_proxy=True, proxy=proxy)
                driver.set_page_load_timeout(40)
                driver.get(self.url)
                sleep(5)
                email, pw = accnt.grabEmail().split(':')
                # username

                # fill the email value
                email_field = driver.find_element_by_name('emailOrPhone')
                email_field.send_keys(email)

                # fill the fullname value
                fullname_field = driver.find_element_by_name('fullName')
                fullname_field.send_keys(name)

                # fill username value
                username_field = driver.find_element_by_name('username')
                username_field.send_keys(username)

                # fill password value
                password_field = driver.find_element_by_name('password')
                passW = accnt.generatePassword()
                password_field.send_keys(passW)

                submit = driver.find_element_by_xpath(
                     '//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[7]/div/button')
                submit.click()

                print('Registering....')
                store('{username},{password},{email},{email_password},{proxy}'.format(
                    username=username,
                    password=passW,
                    email=email,
                    email_password=pw,
                    proxy=proxy
                ))
                now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                sleep(4)
                driver.save_screenshot(r'../errors/screenshot-%s.png' % now)
                # driver.close()
            except TimeoutException as e:
                print("Page load timeout occurred, resetting...")
                now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                driver.save_screenshot(r'../errors/screenshot-%s.png' % now)
                driver.close()

    def creation_config(self):
        try:
            if self.use_custom_proxy == False:
                for i in range(0, config.Config['amount_of_account']):
                    if len(self.sockets) > 0:
                        current_socket = self.sockets.pop(0)
                        try:
                            self.createaccount(current_socket)
                        except Exception as e:
                            logger.error('Error!, Trying another Proxy {}'.format(current_socket))
                            self.createaccount(current_socket)

            else:
                sess_id = randint(100001, 200001)
                city = 'new_york'
                proxy_s = None
                fields = proxy_s.split(':')
                host = fields[0].strip('\n')
                port = fields[1].strip('\n')
                user = fields[2].strip('\n')
                pw = fields[3].strip('\n')

                proxy = {'address': host,
                         'port': port,
                         'username': user,
                         'password': pw}
                amount_per_proxy = config.Config['amount_per_proxy']

                if amount_per_proxy != 0:
                    print("Creating {} amount of users for this proxy".format(amount_per_proxy))
                    for i in range(0, amount_per_proxy):
                        try:
                            self.createaccount(proxy, 2)

                        except Exception as e:
                            logger.error("An error has occured" + e)

                else:
                    random_number = randint(1, 20)
                    print("Creating {} amount of users for this proxy".format(random_number))
                    for i in range(0, random_number):
                        try:
                            self.createaccount(proxy, 1)
                        except Exception as e:
                            logger.error(e)
        except Exception as e:
            logger.error(e)


def runbot():
    for i in range(0, 5):
        account = AccountCreator(config.Config['use_custom_proxy'])
        account.creation_config()


runbot()
