'''
This software is licenced under a Beerware licence. 
/*
 * ----------------------------------------------------------------------------
 * "THE BEER-WARE LICENSE" (Revision 42):
 * <debasishm89@gmail.com> wrote this file. As long as you retain this notice you
 * can do whatever you want with this stuff. If we meet some day, and you think
 * this stuff is worth it, you can buy a beer in return Debasish Mandal.
 * ----------------------------------------------------------------------------
 */
'''

'''

This small script extracts requried cookie parameters from Facebook cookies.

'''

import httplib
import urllib
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:20.0) Gecko/20100101 Firefox/20.0',
		'Content-Type': 'application/x-www-form-urlencoded'}
#uname = raw_input('Enter Email : ')
#pwd = raw_input('Enter password : ')
uname = "you_fb_login_email@gmail.com"
pwd = "your_fb_password"
body = "email="+uname+"&pass="+pwd+"&login=Log+In"
conn = httplib.HTTPSConnection('m.facebook.com')
conn.request("POST", "/login.php", body, headers)
response = conn.getresponse()
cook = response.getheaders()[3][1].split('; ',35)
print cook[0]
print cook[31].split(' ',)[1]
