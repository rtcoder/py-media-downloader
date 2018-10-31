import time
from urllib.request import urlopen
import urllib.request, urllib.parse, urllib.error
import re
import os, sys
from urllib.parse import urlparse
from decimal import Decimal

def get_url(str):
    if (str.startswith('https://') or str.startswith('http://')):
        return str 
    else:
        return 'http://' + str

def uri_validator(x):
    result = urlparse(x)
    if(result.scheme != '' and result.netloc != ''):
        return True
    else:
        return False

url = ''

for arg in sys.argv:
    if(arg.startswith('url=')):
        url = get_url(arg[4:])

if(url == '' or uri_validator(url) == False):
    print('Error: invalid URL')
    exit()

website = urlopen(url)
html = website.read().decode('utf-8')
links = re.findall('"((http|ftp)s?://.*?(jpg|png|jpeg|bmp|gif))"', html)

uri = urlparse(url)
domain = '{uri.netloc}'.format(uri=uri)
domainfolder = '{uri.path}'.format(uri=uri).strip('/')
fullpath=domain+'/'+domainfolder

if(os.path.exists(fullpath) == False):
    os.makedirs(fullpath, 0o777)

for i in range(0, len(links)):
    value = links[i]
    percent = round(Decimal(100 * (i + 1) / len(links)), 2)
    progress =  '\r' + str(i + 1) + ' / ' + str(len(links)) + '(' + str(percent) + ')'
    print("\r" + value[0])
    print(progress, end='\r')
    file = urllib.request.URLopener()
    file.retrieve(value[0], fullpath+'/'+value[0].split('/')[-1])
