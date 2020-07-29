import os
import socket
import time
import urllib.request


def getRootDomain(url):
    if url is not None:
        domainSplit = url.split(".")
        rootDomain = domainSplit[-2] + '.' + domainSplit[-1]
        return rootDomain
    else:
        return ''


def update_dns():
    # GET IP FROM WEBSITE
    hostIP = str.strip(urllib.request.urlopen(remoteUrl).read().decode('utf8'))

    # COMPARE DNS TO HOST IP
    domainIP = socket.gethostbyname(DynamicDomain)

    # UPDATE IP FOR DOMAIN IF NO MATCH
    if hostIP != domainIP:
        url = updateUrl + "u={}&p={}&d={}&h={}&i={}".format(Username, Password, AccountDomain, DynamicDomain, hostIP)
        f = urllib.request.urlopen(url)
        message = DynamicDomain + ": IP Changed ({} --> {})".format(domainIP, hostIP)
        print(time.ctime(), ":", message)


if __name__ == "__main__":

    Username = os.getenv('USERNAME', None)
    Password = os.getenv('PASSWORD', None)
    DynamicDomain = os.getenv('DOMAIN', None)
    AccountDomain = getRootDomain(DynamicDomain)
    UpdateFrequency = int(os.getenv("UPDATEEVERY", 3600))
    updateUrl = "https://ssl.gratisdns.dk/ddns.phtml?"
    remoteUrl = "https://checkip.amazonaws.com"

    if None not in (Username, Password, DynamicDomain):
        while True:
            update_dns()
            time.sleep(UpdateFrequency)
    else:
        exit(1)
