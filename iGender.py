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

import cgi
import webapp2
import httplib
import urllib2
import zlib
import re
from google.appengine.ext import db
from google.appengine.api import memcache


class Names(db.Model):
    name = db.StringProperty(required=True)
    confidence = db.StringProperty(required=True)
    result = db.StringProperty(required=True)
class MainPage(webapp2.RequestHandler):
    def get(self):
        self.redirect("/main/index.html")
class ai(webapp2.RequestHandler):
    def post(self):
	final = []
	key = cgi.escape(self.request.get('name')).lower()
	user_db = db.GqlQuery("SELECT * FROM Names WHERE name=:1", key)
	user = user_db.get()
	if user == None:
	    if "" in key or "%20" in key:#So that it can handle spaces name
		key = key.replace(" ","+")
		key = key.replace("%20","+")
	    req = urllib2.Request("http://m.facebook.com/search/?refid=46&search=people&query="+key)
	    req.add_header('User-Agent', 'Opera/9.80 (J2ME/MIDP; Opera Mini/9.80 (J2ME/22.478; U; en) Presto/2.5.25 Version/10.54')	
	    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
	    req.add_header('Accept-Encoding', 'gzip, deflate')
	    req.add_header('Cookie', 'xs=xxxx:xxxx:xxxxxxxxxxxx; c_user=1000044xxxxxxxxx; ')
	    data = zlib.decompress(urllib2.urlopen(req).read(), 16+zlib.MAX_WBITS)
	    match = re.findall('<td class="name"><a href="/(.*?)">',data)
	    if len(match) == 0:# no result found
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.out.write('{"gender":"none","confidence":"0"}')
	    else:
		for uname in match:
		    if "profile.php" not in uname:
			try:
			    req = urllib2.Request("http://graph.facebook.com/?id="+uname.split('?',1)[0])#Second round request using graph API
			    data = urllib2.urlopen(req).read()
			    match1 = re.findall('"gender":"(.*?)"',data)
			    if len(match1) != 0:
				final.append(match1[0])
			except urllib2.URLError, e:
			    print 'Error', e
		if final.count('male') > final.count('female'):
		    e = Names(name=key,confidence=str((final.count('male')*100)/len(final)),result="male")
		    e.put()
		    self.response.headers['access-control-allow-origin'] = '*'
		    self.response.headers['access-control-allow-methods'] = 'POST'
		    self.response.headers['access-control-max-age'] = '60'
		    self.response.headers['Content-Type'] = 'text/plain'
		    self.response.out.write('{"gender":"male","confidence":"'+str((final.count('male')*100)/len(final))+'"}')
		else:
		    e = Names(name=key,confidence=str((final.count('female')*100)/len(final)),result="female")
		    e.put()
		    self.response.headers['access-control-allow-origin'] = '*'
		    self.response.headers['access-control-allow-methods'] = 'POST'
		    self.response.headers['access-control-max-age'] = '60'
		    self.response.headers['Content-Type'] = 'text/plain'
		    self.response.out.write('{"gender":"female","confidence":"'+str((final.count('female')*100)/len(final))+'"}')
	else:
	    self.response.headers['access-control-allow-origin'] = '*'
	    self.response.headers['access-control-allow-methods'] = 'POST'
	    self.response.headers['access-control-max-age'] = '60'
	    self.response.headers['Content-Type'] = 'text/plain'
	    self.response.out.write('{"gender":"'+user.result+'","confidence":"'+user.confidence+'"}')	    
app = webapp2.WSGIApplication([('/', MainPage),
                               ('/ai', ai)],
                              debug=False)
