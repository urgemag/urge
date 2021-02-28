# Urge
## _A Website That Will Inspire And Change Your Life_

Urge is a beautiful, cloud-enabled, flask-powered, motivational and inspirational website.

## ✨ Features

- Dashboard
- Blog
- Courses
- Tools (e.g. MBTI test)
- Musics Part

## 🚀 Tech

Urge uses a number of open source projects to work properly:

- [Flask] - a micro web framework written in Python
- [CKEditor] - a WYSIWYG rich text editor
- [sweetalert2] - a beautiful, responsive, customizable replacement for javascript's popup boxes
- [MongoDB] - a cross-platform document-oriented database program
- [Docker] - an open platform for developing, shipping, and running applications
- [Nginx] - an open source software for web serving, reverse proxying, caching and more
- [Gunicorn] - a python web server gateway interface HTTP server
- [Plyr] - a simple, accessible and customisable media player
- [APlayer] - Wow, such a beautiful HTML5 music player
- [jQuery] - duh


## ⚙️ Installation

Urge only and only requires [Docker](https://www.docker.com/) to run.

Install Docker and start the server, docker takes care of other dependencies.

```sh
apt install docker-compose
```

Now clone the repo:
```sh
git clone https://github.com/urgemag/urge
cd urge
```

Let's take care of .env files...

```sh
cp .env.sample .env
cp flask/.env.sample flask/.env
cp flask/setting.py.sample flask/setting.py
```
1st .env file contains your docker-compose data. fill it like this:
```
PORT=<THE‌_PROJECT_PORT>
MONGO_INITDB_ROOT_USERNAME=<DATABASE_USERNAME>
MONGO_INITDB_ROOT_PASSWORD=<DATABASE_PASSWORD>
```

2nd .env provides the data due to production and debug mode. fill it like this( if you are using docker, set production mode true ):
```
DEBUG_MODE = <TRUE_OR_FALSE>
PRODUCTION = <TRUE_OR_FALSE>
```

3rd .env has the data for Google OAuth. fill it like this:
```
google_client_id = <GOOGLE_CLIEND_ID>
google_client_secret = <GOOGLE_CLIEND_SECRET>

```

last one is a .py file which has many sensitive data in itsself. fill these parts like this:
```
secret_key = <YOUR_RANDOM_SECRET_KEY>

recaptcha_public_key = <PUBLIC‌_KEY_FOR_RECAPTCHA>
recaptcha_secret_key = <PRIVATE_KEY_FOR_RECAPTCHA>

mmerchant_id = <ZARIN_PAL_MMERCHANT_ID>
```


## Docker

just run:
Make sure that you have done all installation steps and made .env files.

```sh
docker-compose up -d
```

if you are not using ssl, please comment these two lines in ./nginx.conf:
```sh
add_header Strict-Transport-Security "max-age=31536000" always;
add_header Content-Security-Policy upgrade-insecure-requests;
```

default port is 1254 but if you changed it in .env file please look for 127.0.0.1:${PORT}
```sh
127.0.0.1:1254
```

## 🤝 Contributing

Contributions, issues and feature requests are welcome.<br />
Feel free to check [issues page](https://github.com/urgemag/urge/issues) if you want to contribute.<br /><br />


## Show your support

Please ⭐️ this repository if this project helped you!


## 📝 License

MIT

**Free Software, Hell Yeah!**

