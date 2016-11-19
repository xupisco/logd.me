# ownCRM 
Your personal and friendly CRM, cut the crap... only the essentials!

[![Build Status](https://travis-ci.org/xupisco/ownCRM.svg?branch=master)](https://travis-ci.org/xupisco/ownCRM)


## Screenshot
[![Home / Logs](http://i.imgur.com/MdnDs9j.png)](http://i.imgur.com/MdnDs9j.png)


## Setup

1. Create a virtualenv
2. Run: $pip install -r requirements/dev.txt
3. Create a ```conf/settings.ini``` file (contents below):
4. $python manage.py migrate
5. $python manage.py createsuperuser
6. $python manage.py runserver
7. Visit /admin/socialaccount/socialapp/
8. [Create a Facebook APP](https://developers.facebook.com/)
9. Add a new App ID and Secret Key for facebook provider
10. Thank @croves...
11. Enjoy!


### conf/settings.ini

```
[settings]
SECRET_KEY=<anything here>
DEBUG=True

GTM_ID=<Google Tag Manager ID>  
DATABASE_URL=sqlite://./conf/db.sqlite3
```


## Try it now

Development preview is available on [Heroku](http://owncrm-dev.herokuapp.com)!


## UNDER MIT LICENSE

Copyright (C) 2016 Leandro Voltolino <xupisco@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
