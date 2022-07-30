# Cyber Security Base 2022 - Project I

Ths project is part of University of Helsinki course ["Cyber Security Base"](https://cybersecuritybase.mooc.fi/). The aim of this repository is to create an application with multiple security holes.

```
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!                                                                             !!
!!  Do not use this repository as a template for your next Django-application  !!
!!                                                                             !!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
```

## Running the application

### 0. Prerequisites

- [Python ^3.8](https://www.python.org/downloads/)

### 1. Clone the repo

```sh
git clone https://github.com/tuukkalai/cheese.git && cd cheese
```

### 2. Create and activate Python virtual environment

```sh
python3 -m venv venv
source venv/bin/activate
```

### 3. Install required packages

```sh
pip install -r requirements.txt
```

### 4. Start the application

```sh
python manage.py runserver
```

And open browser with given URL (by default [http://127.0.0.1:8000](http://127.0.0.1:8000))

## Testing credentials

|Username|Password|
|:--|:--|
|bob|squarepants|
|alice|W0nderLand!|

---

## Report

Link to project repo: <https://github.com/tuukkalai/cheese>

### Flaw 1: [Cryptographic failure](https://owasp.org/Top10/A02_2021-Cryptographic_Failures/)

https://github.com/tuukkalai/cheese/blob/3baa5bb5f5a80c1fb0aa31af99860d27966ca0cd/cheese/settings.py#L30

Exposed environmental secret can be seen as a Cryptographic failure. Django utilizes `SECRET_KEY` value to cryptographically sign values handled by the application, for example hidden form field values. With cryptografic signs Django detects tampering of data. If an attacker gains control of the `SECRET_KEY`, he/she might be able to sign any data and gain control of the application. Without Django detecting the tampering of the data.

The `SECRET_KEY` value is not exposed within the application, but with searching the web with couple of keywords attacker might find this repository and use the key in malicious intentions. Now that the `SECRET_KEY` is in this repository's history, I should update the key before deploying the app.

To fix this issue the developer should hide the secret key and store it in safe place. The [`python-dotenv`](https://pypi.org/project/python-dotenv/) package can be used to pass the secret value to the application.

`python-dotenv` package is already introduced to the project. Next steps are to enable the package:

  1. load dotenv (uncomment `load_dotenv()` in [`cheese/settings.py`](https://github.com/tuukkalai/cheese/blob/3baa5bb5f5a80c1fb0aa31af99860d27966ca0cd/cheese/settings.py#L20))
  2. save the `SECRET_KEY` to `.env`-file (uncomment row 1 in [`.env`](https://github.com/tuukkalai/cheese/blob/main/cheese/settings.py#L20))
  3. add `.env`-file to `.gitignore`
  4. load the `SECRET_KEY` value from `.env` (toggle commenting on [rows 30 & 31 in `cheese/settings.py`](https://github.com/tuukkalai/cheese/blob/3baa5bb5f5a80c1fb0aa31af99860d27966ca0cd/cheese/settings.py#L30-L31))

### Flaw 2: [Injection](https://owasp.org/Top10/A03_2021-Injection/)

https://github.com/tuukkalai/cheese/blob/3baa5bb5f5a80c1fb0aa31af99860d27966ca0cd/polls/views.py#L113-L116

The application fetches poll questions from the database using `question_id` from URL parameter in database query. Attacker might notice this solution and craft malicious URL with suitable parameters to extract sensitive information from the database.

For example, following URL prints admin users password hash on the screen: <http://127.0.0.1:8000/question/2%20AND%201%3D2%20UNION%20SELECT%20username,%20password,%20id,%20is_superuser%20FROM%20auth_user%20WHERE%20is_superuser%3D1/>

To fix the issue using the out-of-the-box methods provided by Django:

1. Comment out the parts with raw query data (`polls/views.py` lines [113-116](https://github.com/tuukkalai/cheese/blob/3baa5bb5f5a80c1fb0aa31af99860d27966ca0cd/polls/views.py#L113-L116))
2. Uncomment the following part (`polls/views.py` lines [118-120](https://github.com/tuukkalai/cheese/blob/3baa5bb5f5a80c1fb0aa31af99860d27966ca0cd/polls/views.py#L118-L120))

### Flaw 3: [Identification and authentication failures](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/)

Currently the application does not log or monitor login attempts. Attacker could easily exploit this vulnerability by creating a script that tests multiple username and password combinations to login on someone elses account.

To test this, activate the virtual environment and run command (assuming the application is running on localhost port 8000):

```sh
python hackpassword.py http://localhost:8000 xato-net-10-million-passwords-10000.txt
```

The script takes quite a long time. Subset of those 10000 passwords are collected in `xato-net-10-million-passwords-every-44th-of-10000.txt`. To test brute force with a subset of passwords, run

```sh
python hackpassword.py http://localhost:8000 xato-net-10-million-passwords-every-44th-of-10000.txt
```

To fix this issue the application should be updated to limit login attempts. Developer might be able to create the feature themselves or they can import external package to handle faulty login attempts. One of these external packages mentioned is [`django-axes`](https://pypi.org/project/django-axes/). Currently `django-axes` is already installed to the project, and configured by adding relevant information mentioned in [django-axes documentation](https://django-axes.readthedocs.io/en/latest/index.html).

To enable the feature, in [`cheese/settings.py`](https://github.com/tuukkalai/cheese/blob/3baa5bb5f5a80c1fb0aa31af99860d27966ca0cd/cheese/settings.py#L37) change the [`AXES_ENABLED`] flag from `False` to `True`.

Personally I would add relevant `AXES_ENABLED` flag to environmental variables, and enable it only in production environment. The package blocks the IP address in the event of false logins. Example changes are commented in

https://github.com/tuukkalai/cheese/blob/3baa5bb5f5a80c1fb0aa31af99860d27966ca0cd/cheese/settings.py#L37-L38

https://github.com/tuukkalai/cheese/blob/3baa5bb5f5a80c1fb0aa31af99860d27966ca0cd/.env#L3

The developer should also update default passwords in any frameworks used in application. Developers should actively avoid using passwords found in password lists and same password in different places. Password managers are handy to manage multiple credentials.

### Flaw 4: [Broken access control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)

In the application user can vote for given choices. Each question has set of available choices. User can vote within single question only once. If the user has already voted for a question, opening the question redirects to the results.

Design flaw in the application shows that the vote is registered to user mentioned in URL. Sending GET request with another username allows malicious user to register vote on behalf of other users. Or even create multiple votes from himself/herself.

https://github.com/tuukkalai/cheese/blob/3baa5bb5f5a80c1fb0aa31af99860d27966ca0cd/polls/views.py#L46-L61

To fix the issue, comment [line 60](https://github.com/tuukkalai/cheese/blob/3baa5bb5f5a80c1fb0aa31af99860d27966ca0cd/polls/views.py#L60) and uncomment [line 59](https://github.com/tuukkalai/cheese/blob/3baa5bb5f5a80c1fb0aa31af99860d27966ca0cd/polls/views.py#L59) in `polls/views.py`.

### Flaw 5: [Security misconfiguration](https://owasp.org/Top10/A05_2021-Security_Misconfiguration/)

[`cheese/settings.py`](https://github.com/tuukkalai/cheese/blob/3baa5bb5f5a80c1fb0aa31af99860d27966ca0cd/cheese/settings.py#L34) contain feature flag set by default to `DEBUG = True`.

https://github.com/tuukkalai/cheese/blob/3baa5bb5f5a80c1fb0aa31af99860d27966ca0cd/cheese/settings.py#L34

Leaving that setting as is, attacker will be able view detailed error messages while poking the application. Detailed error message might reveal alternative possibilities to penetrate the system.

To fix this issue, the developer should set the `DEBUG` value to `False` in production environment.

Similarly as with `SECRET_KEY` and `AXES_ENABLED` variables, I would add value for `DEBUG` as an environmental variable. This way the helpful comments are visible in development environment, but hidden in production environment.

https://github.com/tuukkalai/cheese/blob/3baa5bb5f5a80c1fb0aa31af99860d27966ca0cd/.env#L2

## Additional considerations when working with Django

Django provides great documentation and great tools to check if the application is ready for production. Using these helpers should be a no brainer to all developers.

One helpful command for checks is

```sh
python manage.py check --deploy
```
