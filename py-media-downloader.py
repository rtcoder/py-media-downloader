import time
import urllib2
import urllib
import re
import os, sys
from urlparse import urlparse


def uri_validator(x):
    result = urlparse(x)
    if(result.scheme != '' and result.netloc != ''):
        return True
    else:
        return False

url = ''
for arg in sys.argv:
    if(arg.startswith('url=')):
        url = arg[4:]

if(url == '' or uri_validator(url) == False):
    print 'Error: invalid URL';
    exit()

website = urllib2.urlopen(url)
html = website.read()
links = re.findall('"((http|ftp)s?://.*?(jpg|png|jpeg|bmp|gif))"', html)

uri = urlparse(url)
domain = '{uri.netloc}'.format(uri=uri)
domainfolder = '{uri.path}'.format(uri=uri).strip('/')
fullpath=domain+'/'+domainfolder
if(os.path.exists(fullpath) == False):
    os.makedirs(fullpath, 0777)

print domain
print domainfolder

for i in links:
    print i[0]+' is saving as: '+ i[0].split('/')[-1]+' in '+fullpath
    file = urllib.URLopener()
    file.retrieve(i[0], fullpath+'/'+i[0].split('/')[-1])
