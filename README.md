# demo-allauth-bootstrap

An out-of-the-box working example of [django-allauth] using Twitter
Bootstrap and showing some basic functionality like grabbing user name
and profile picture at signup.

## tl;dr

You'll need to do quick setup with providers like Facebook and Google, but
after that you should have a Django project with user signup and management
that "just works", out of the box.

## Objectives

1. Help anyone building a new site get up and going quickly with allauth.

2. Help remind me how a basic site hangs together ;)


## Tips before you run this

Set up one or both of Facebook and Google as developer apps.

Tips for Facebook:
- You'll need the Facebook App ID (NOT any client ID) and the secret.
- Repeat, the Facebook App ID and NOT any client ID is what should be entered
  for "client ID"
- Create an app in the [facebook-developer-settings] area and then create a test app
  from that. The test app seems to be the only thing that will work with a
  localhost Django app.
- Read the [article by Sarah][2] or see below for moe.

Tips for Google:
- You'll need the Google client ID and secret.



## Getting Running

1. Install Python. I used Python 3.4.3 at the moment but 2.7.x works fine too.

2. Install a ``virtualenv`` and requirements:

        $ cd demo-allauth-bootstrap
        $ virtualenv mypy
        $ . mypy/bin/activate
        $ pip install -r requirements.txt

3. Set up and Run:

   I used a ``Makefile``. You don't have to. You can look inside the ``Makefile``
   and see how it's run.

        $ make configure   # Builds a seed.sql that can be used in `make rebuild`
        $ make rebuild     # A bit better than `python manage.py syncdb`
        $ make run         # The same as `python manage.py runserver`


4. Visit http://127.0.0.1:8000/


At this point you should have a site that allows registration and
login of local users. If you enabled Google or Facebook during ``make configure``,
those destinations should allow you to join and log in to the site.


## Some Notes

### A word about seed data

During development I find that I frequently want to erase and rebuild the database,
and setting up seed data like the admin user and ``Sites`` objects can be tedious.
There are ways to set this up in code (the ``allauth`` source does this) but I've
chosen to do it with a SQL file, produced with:

    Makefile --> runs Python configure.py --> produces seed.sql

I want to point out that this use of Makefiles and seed data is nothing to do with
``allauth``, it's just my hack way of getting set up and running.

You can edit ``seed.sql`` then destroy and rebuild your database easily with this:

    make rebuild

### A word about Makefiles

If your system doesn't have ``make`` (I'm looking at you, Windows), have a look in
the ``Makefile`` for what commands to run. It's pretty straightforward.


### Configure Facebook Login

Sarah describes this nicely in [her article][2]

Aside from UI changes, the method she described worked well.

Go to [facebook-developer-settings].

### Configure Google Login

To set up Google, follow the [Google oauth instructions][3] or [this help answer][4]
which is basically:


1. Go to https://console.developers.google.com/

2. Create a new app and enable the Google+ API

3. Left navigation APIs & auth > Credentials

4. Create new client ID

5. For Authorized Javascript Origins: http://127.0.0.1:8000

6. For Authorized Redirect Url: http://127.0.0.1:8000/accounts/google/login/callback/

Run ``make configure``, enter the details, then ``make rebuild`` and ``make run``.
Alternatively edit the ``seed.sql`` file from a previous run and then ``make rebuild run``.


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

I'd struggled with outdated Django registration modules before and was pleasantly
surprised to find django-allauth. Sarah's tutorial is superb but I wanted something
more full to use as a basis for future work, and figured it might help others.


## Credits

Thanks to Raymond for django-allauth and Sarah for her tutorial.


## Rough Edges

In no order:

* I don't like the handling of Django "messages". The messages accumulate in the cookie,
  which is weird on its own, and clear only when displayed. I don't get why it was done
  that way. I'm sure there are better ways to handle it; I just haven't looked into it yet.

* The default allauth rendering for profile (email, social accounts etc) is adequate but
  could do with some work.


[django-allauth]: https://github.com/pennersr/django-allauth
[2]: http://www.sarahhagstrom.com/2013/09/the-missing-django-allauth-tutorial/#Create_and_configure_a_Facebook_app
[3]: https://developers.google.com/+/web/api/rest/oauth#login-scopes
[facebook-developer-settings]: https://developers.facebook.com/

