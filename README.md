# demo-allauth-bootstrap

Simple, out-of-the-box Django website with a visitor (no login) area and
a user (login required) area, where registration and login can be via providers
like Google and Facebook.


## tl;dr

1. Clone or download the repo
2. Do a little setup
3. Run the server - dev is done
4. [Remove some files, rename some more](#make-the-repo-yours),
   and and you've got the basis of your new site


## Objectives

1. Help anyone building a new site get up and going quickly with allauth.

2. Help remind me how a basic site hangs together ;)


## Tips

### Overall tip

Tinker with it out-of-the-box. If it does what you like, you can 
[remove a few things](#make-the-repo-yours) and use the code as a basis for your
own site.
 

### Tips for Facebook

- You'll need the Facebook App ID (NOT any client ID) and the secret.
- Repeat, the Facebook App ID and NOT any client ID is what should be entered
  for "client ID"
- Create an app in the [facebook-developer-settings] area and then create a test app
  from that. The test app seems to be the only thing that will work with a
  localhost Django app.
- Read the [article by Sarah][2] or see below for moe.


### Tips for Google

- You'll need the Google client ID and secret from the Google Developer Console.


## Pre-setup

If you want to use a provider like Facebook or Google, you'll need to do do setup
on those sites to get settings you'll need in Django.


### Configure Facebook Login

Follow these instructions if you want to use Facebook as an authentication provider.
Skip otherwise.

Sarah describes this nicely in [her article][2]

Aside from UI changes, the method she described worked well.

1. Go to [facebook-developer-settings].

2. Add app

3. Create a test app (under the above app)

4. Go to Settings > Advanced

5. Do *not* add any server to Server IP Whitelist ([facebook-whitelist-ip-error])

6. Add product "Facebook Login"

7. Enable if not automatically selected: Client OAuth Login, Web OAuth Login

8. Add OAuth redirect URL (in any order):
  ``http://127.0.0.1:8000/``
  ``http://127.0.0.1:8000/accounts/facebook/``
  ``http://127.0.0.1:8000/accounts/facebook/login/callback/``

  Note: If you're loading your site with ``localhost:8000`` you should use "http://localhost:8000/..." 
  above. Whichever you choose, do it consistently and you should be ok.

Note: The "app secret" and "client id" are a bit confusing with Facebook.  
You want to record the "Facebook App Secret" and the "Facebook App ID". The latter
"Facebook App ID" becomes the "client ID" from a Django Allauth perspective.


### Configure Google Login

Follow these instructions if you want to use Google as an authentication provider.
Skip this section otherwise.

To set up Google, follow the [Google oauth instructions][3] or [this help answer][4]
which is basically:


1. Go to https://console.developers.google.com/

2. Create a new app

3. Make sure that app is selected (next to the "Google APIs" Logo in the top-left)

4. In the left navigation rail under "APIs and Services", click "Credentials"

5. Create new oauth client ID

   You will need to specify some "consent screen details". You can skip most
   of the fields. 

6. For Authorized Javascript Origins, add: http://127.0.0.1:8000

7. For Authorized Redirect URIs, add: http://127.0.0.1:8000/accounts/google/login/callback/

8. Click "Create"

9. Copy the "client ID" and "client secret" strings and keep each handy - you'll need them shortly.


Reminder: if you're loading your site at ``localhost:8000`` then you'll need to set the
URIs above to ``http://localhost:8000/..." etc. I recommend not doing that. Instead, just
load your local site as http://127.0.0.1:8000/


### Configure authentication with other providers

The django-allauth library covers []_many_ others providers][allauth-providers]  


## First-time setup

1. Make sure you have Python 3.x installed. I used Python 3.6.

   Python 2.7.x used to work but Django 2.0 dropped support for Python 2.x, and is
   dropping support for Python 3.4.

2. Create a ``virtualenv`` and requirements.

    For example:

        $ cd demo-allauth-bootstrap
        $ python3 -m venv mypy       # you can call it anything, not just "mypy"
        $ . mypy/bin/activate
        $ pip install -r requirements.txt

3. Generate the initial settings:

        $ python configure.py

   Follow the prompts. This will generate the initial `settings.py`

4. Set up the initial migrations:

   A specific `makemigrations` is needed for the `auth_user` table:
   
        $ python manage.py makemigrations allauthdemo_auth

5. Build the database schema:

        $ python manage.py migrate

6. Create the superuser:

        $ python manage.py createsuperuser

   Tip: do _not_ enter the same email address that you'll connect via Google/Facebook with.
   In development I use a made up address like "me@admin.test".

7. Add the social providers:

   Run this for each provider you want to include.
   
        $ python manage.py set_auth_provider google GOOGLE_CLIENT_ID GOOGLE_SECRET_ID
        saved: Google (...)
        
        $ python manage.py set_auth_provider facebook FACEBOOK_CLIENT_ID FACEBOOK_SECRET_ID
        saved: Facebook (...)

   This essentially runs SQL like:
   
        DELETE FROM socialaccount_socialapp WHERE provider='google';
        INSERT INTO socialaccount_socialapp (provider, name, secret, client_id, `key`)
        VALUES ("google", "Google", "SECRET", "CLIENT", '');
        INSERT INTO socialaccount_socialapp_sites (socialapp_id, site_id) VALUES (
          (SELECT id FROM socialaccount_socialapp WHERE provider='google'),1);
        
8. Check it's working:

        $ python manage.py runserver

   Load the site at http://127.0.0.1:8000

   You should see a landing page. Click "Join" or "Login".


9. Log into admin and change the default site:

   Go to http://127.0.0.1:8000/admin/sites/site/ - you may need to log out, then log back in as the
   superuser you created above.

   You don't technically have to rename the site but the default "example.com" isn't very useful.
   In development I change the domain to "127.0.0.1" and the name to "<project name> (Dev)".


### Doing it over

When you're getting oriented you may find you want to start over for any reason.

If you're using sqlite as the database (the default), just remove the file and start
the sequence again:

```
rm db.sqlite3
python configure
python manage.py makemigrations allauthdemo_auth
python manage.py migrate
python manage.py set_auth_provider google ...
python manage.py runserver
```

If you're using Postgres or similar, remove and recreate the database.


## Notes

### Make the repo yours

If you've got the site up and want to use it as the basis for your own real site,
here's what I do:

- Remove all the git history:

        rm -rf .git/

  and start a new history:

        git init

- Remove unnecessary files:

        rm LICENSE README.md allauthdemo/settings.template.py configure.py

- Rename the `"allauthdemo"` directory to something more appropriate

- Optionally rename the class `auth.models.User` to something more specific.
  You'll need to rebuild the database (I suggest you do this after you've built the
  initial app and renamed things anyway). Don't leave this too late as trying to
  migrate the `User` class to a new name doesn't work nicely when you've got real data.

- Check the `auth.models.UserProfile` class. The draft one includes date-of-birth (`dob`),
  which you might want to remove.

- Change settings so Postgres or another full database is used, not sqlite (which is
  awesome, but not right for a real project!)


### How I built this

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


### Why I built this

I'd struggled with outdated Django registration modules before and was pleasantly
surprised to find django-allauth. Sarah's tutorial is superb but I wanted something
more full to use as a basis for future work, and figured it might help others.


### Credits

Thanks to Raymond for django-allauth and Sarah for her tutorial.


### Rough Edges

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
[facebook-whitelist-ip-error]: http://stackoverflow.com/questions/21118089/uncaught-oauthexception-this-ip-cant-make-requests-for-that-application
[allauth-providers]: https://django-allauth.readthedocs.io/en/latest/providers.html
