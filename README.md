### iGender
Have you ever thought how human brain determine gender by just hearing or reading first name?? This artificial intelligent gender prediction tool can easily predict gender(male/female)from first name. I've developed this tiny application in early 2013,just to learn development in Google App Engine Environment. That time, I've also bought a domain name for this project, called i-gender.com for 1 year. This api has served near about 7.5 lakh unique names. It's expired years back and I don't have any wish to re-new it :/.One limited edition of this API is still available @ http://maleorfemale07.appspot.com. 

I just found the source code package while cleaning up one of my old external hard drives. Decided to make it open source, hoping it may help anyone who is in need :)
###How does it work ?
Well, the logic is pretty simple and stupid.You might have already guessed that ;) .When user enters a name,in backend this application logs into Facebook.com and searches the same name in Facebook. Based on the search result it will calculate the gender,confidence and let user know the result. For example, For any given name if FB returns 10 accounts, and out of 10, 8 accounts are Female, it is going to return gender as Female with 80% confidence.). And it will also save the name in a database, so that next time if same name comes in, it doesn't have to go to Facebook.

It uses python regular expression to parse html(mobile version of facebook page). FB has changed their UI a lot since then(2012) so it may not work properly now. You may have to modify the reg-ex in iGender.py (Line 46)

Facebook doesn't return Gender information in search result, if you're searching names publicly without logging into Facebook. To solve the problem, you need to hardcode a valid Facebook user's cookie (Cookie params xs= & c_user=)in iGender.py (Line 44). Because every time logging into FB using username password will be very slow. However, if you're already logged in, a single GET request will do the job and we will get what we want. I've included one script called getsid.py , which extracts required cookie parameter if you enter username password of your test account.

###Setting up the environment
With the request handler script (iGender.py or iGender-memcache.py)and configuration file(app.yaml) mapping every URL to the handler, this project is complete. You can test it with the web server included with the App Engine SDK. You can download Google App Engine Python SDK from here : https://cloud.google.com/appengine/downloads

Once you have a directory for your application and an app.yaml configuration file (Let's say in "iGender" folder), you can start the development web server with the dev_appserver.py command:

```sh
$ dev_appserver.py iGender
```
The web server listens on port 8080 by default. You can visit the application at this URL: 
```sh
http://localhost:8080/
```
That's it.You're ready to go!!
For more info visit : https://cloud.google.com/appengine/docs/python/tools/devserver
###How to Use?
iGender.py or iGender-memcache.py script contains main code responsible for handling request and predicting gender of given name.Using iGender API is very simple.You have to send a http POST request to http://yourdomain.com/ai with POST parameter name=your_name_here
And you should receive JSON Response like this {"gender":"male","confidence":"75"}
Testing 

###Using the API
An Example with Python is given below :
```py
import urllib2
import json
req = urllib2.Request("http://www.i-gender.com/ai", "name=nichole")
response = urllib2.urlopen(req).read()
decoder = json.JSONDecoder()
result = decoder.decode(response)
print result['gender']
print result['confidence']
```
### Licence
"THE BEER-WARE LICENSE" (Revision 42): <debasishm89@gmail.com> wrote this file. As long as you retain this notice you can do whatever you want with this stuff. If we meet some day, and you think this stuff is worth it, you can buy me a beer in return :).

###Cheers
Debasish Mandal
