# demo-allauth-bootstrap

A working example of django-allauth with Twitter Bootstrap.

## tl;dr

You'll need to do quick setup with providers like Facebook and Google, but
after that this should "just work", out of the box.

## Objectives

1. Help anyone building a new site get up and going quickly with allauth.

2. Help remind me how a basic site hangs together ;)


## Getting Running

Approximately:

1. Install Python. I used Python 2.7.5. I really must upgrade to 3.x sometime...

2. Install a ``virtualenv`` and requirements:

        $ virtualenv mypy
        $ . mypy/bin/activate
        $ pip install -r requirements.txt
        $ python manage.py syncdb
        $ python manage.py runserver

At this point you should have a site that allows registration of local users.

## Getting Running without Social App Integration

1. Register an app with the Social sites of your choice, such as Google and Facebook.
   Some notes on that in below.

2. You can generate some seed data with:

        $ python configure.py
        
        ----------
        Admin User
        ----------
        
        
        Do you want to set up a superuser?
    
        Doing it now means you don't have to re-enter it every time
        you rebuild the database in development.
    
        Please enter "yes" or "no": yes
        
        ...
        
        All done. 
        Wrote ``seed.sql``.
        
        Next, run ``make rebuild`` then ``make run`` 
        (or ``python manage.py runserver``).


I like using ``Makefiles`` for simple tasks but I'm probably in the minority
these days. In any case, once the seed file is generated you can rebuild your
database from scratch, clean all the ``pyc`` files and run the server with:

    make rebuild clean run

Suggestions on a better approach for seed data are welcome.


### Configure Facebook Login

Sarah describes this well here:
http://www.sarahhagstrom.com/2013/09/the-missing-django-allauth-tutorial/#Create_and_configure_a_Facebook_app

Aside from UI changes, the method she described worked well.


### Configure Google Login

To set up Google, follow instructions at https://developers.google.com/+/api/oauth#login-scopes,
which is basically:

1. Go to https://console.developers.google.com/

2. Create a new app and enable the Google+ API

3. Left navigation APIs & auth > Credentials

4. Create new client ID

5. For Authorized Javascript Origins: http://127.0.0.1:8000

6. For Authorized Redirect Url: http://127.0.0.1:8000/accounts/google/login/callback/

Copy the Client ID and secret to SQL config in this repo and put into the database.


## How I built this

The best resources:
* Raymond's GitHub repo:
  https://github.com/pennersr/django-allauth

* allauth docs:
  http://django-allauth.readthedocs.org/en/latest/

* Sarah Hagstrom's magnificent article:
  http://www.sarahhagstrom.com/2013/09/the-missing-django-allauth-tutorial/

I first worked with Sarah's example to understand how the components worked together.
Then I cloned the github repo and worked with the example directory, customising it to
what made sense to me. I moved it to use Bootstrap only and added some basic standard
stuff like a landing page and stubs for terms and contact.

I moved the bootstrap forms to use the bootstrap3 library. At the very least that
made handling Django "messages" better (though see my notes in "Rough Edges" below).
Read about bootstrap3 here: http://django-bootstrap3.readthedocs.org/en/latest/



## Why I built this

TODO

## Credits


## Rough Edges

In no order:

* I don't like the handling of Django "messages". The messages accumulate in the cookie,
  which is weird on its own, and clear only when displayed. I don't get why it was done
  that way. I'm sure there are better ways to handle it; I just haven't looked into it yet.

* The default allauth rendering for profile (email, social accounts etc) is adequate but
  could do with some work.

