import configparser
import socket
import urllib.request
import requests
import time
import os


def getRootDomain(url):
    domainSplit = url.split(".")
    rootDomain = domainSplit[-2] + '.' + domainSplit[-1]
    return rootDomain

def update_dns():
    Username = os.getenv('USERNAME', '')
    Password = os.getenv('PASSWORD', '')
    DynamicDomain = os.getenv('DOMAIN', '')
    AccountDomain = getRootDomain(DynamicDomain)
    updateUrl = "https://ssl.gratisdns.dk/ddns.phtml?"
    remoteUrl = "https://checkip.amazonaws.com"

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
    while True:
        update_dns()
        time.sleep(3600)