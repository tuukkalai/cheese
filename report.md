# Report

Link to project repo: <https://github.com/tuukkalai/cheese>

## Prerequisites

- [Python >3.8](https://www.python.org/downloads/)

## Running the project

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

## Flaws

### Flaw 1: [Settings include exposed environmental variable `SECRET_KEY`](https://github.com/tuukkalai/cheese/blob/main/cheese/settings.py#L26)

Exposed environmental secret can be seen as a [Cryptographic failure](https://owasp.org/Top10/A02_2021-Cryptographic_Failures/). The value is not exposed within the application, but with searching the web with couple of keywords attacker might find this repository and use the key to gain control of the complete application.

To fix this issue,

  1. import dotenv package ([Uncomment import](https://github.com/tuukkalai/cheese/blob/main/cheese/settings.py#L15))
  2. save the `SECRET_KEY` to `.env`-file
  3. add `.env`-file to `.gitignore`
  4. add `SECRET_KEY` to environmental variables in production system

### Flaw 2: [SQL Injection](https://owasp.org/Top10/A03_2021-Injection/)

Adding query directly with raw-method and insecure way of adding user input in query.

Question ID is extracted from URL and injected directly to query. This allows attacker to craft a URL, which injects 
Following URL prints admin users password hash on the screen: <http://127.0.0.1:8000/question/2%20AND%201%3D2%20UNION%20SELECT%20username,%20password,%20id,%20is_superuser%20FROM%20auth_user%20WHERE%20is_superuser%3D1/>

[[ how to fix it... ]]

### Flaw 3: [this and that](http://example.com)

exact source link pinpointing flaw 2...
description of flaw 2...
how to fix it...

...

### Flaw 5: [this and that](http://example.com)

exact source link pinpointing flaw 5...
description of flaw 5...
how to fix it...
