import os
import zipfile

from selenium import webdriver


def manifest_js(proxy_host=None, proxy_port=None, proxy_user=None, proxy_pw=None):
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Toiney Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """
    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
              singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
              },
              bypassList: ["localhost"]
            }
          };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (proxy_host, proxy_port, proxy_user, proxy_pw)
    return manifest_json, background_js


def get_chromedriver(use_proxy=False, user_agent=None, proxy=None):
    """Get ChromeDriver instance.
    :proxy: should be dict containing host:port / user:pass if auth is required"""
    path = os.path.dirname(os.path.abspath(__file__))
    options = webdriver.ChromeOptions()
    if use_proxy:
        pluginfile = 'proxy_auth_plugin.zip'

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            auth_ext = manifest_js(proxy_host=proxy['address'],
                                   proxy_port=proxy['port'],
                                   proxy_user=proxy['username'],
                                   proxy_pw=proxy['password'])
            zp.writestr("manifest.json", auth_ext[0])
            zp.writestr("background.js", auth_ext[1])
        options.add_extension(pluginfile)
    if user_agent:
        options.add_argument(f'user-agent={user_agent}')
    driver = webdriver.Chrome(
        r'C:/chromedriver.exe',
        options=options,
    )
    return driver


# example below #

def example_get():
    sd = 'customer-scorpion_cykibyxy-cc-US:f4ZkMkeF@resi.valar-solutions.com:7777'
    proxy_split = sd.split(':')
    # split address and password
    split_adr = proxy_split[1].split('@')
    # indexes are as follows:
    # proxy user = 0
    # proxy pw = 1
    # proxy host = 2
    # proxy port = 3
    # now make a dictionary
    proxy = {'address': split_adr[1],
             'port': proxy_split[2],
             'username': proxy_split[0],
             'password': split_adr[0]}
    driver = get_chromedriver(use_proxy=False, proxy=proxy)
    driver.get('http://httpbin.org/ip')


if __name__ == '__main__':
    example_get()
