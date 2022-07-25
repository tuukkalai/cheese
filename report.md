# Report

Link to project repo: <https://github.com/tuukkalai/cheese>

## Checklist

- [ ] Five different flaws from OWASP Top ten list (selected 2021 list)
- [x] Application should have a backend (Python + Django)
- [x] Saved to public repo
- [ ] 1000 word report

## Scoring

The rubric for the scores are as follows:

- **Excellent**: No issues or only cosmetic issues
- **Good**: The flaw and the fix are correctly done. Minor issues in descriptions.
- **Average**: The flaw described adequately and the fix fixes the problem. Minor misunderstanding of the underlying mechanism. The description is too vague but ultimately correct.
- **Passable**: The flaw is identified correctly, the fix partially corrects the problem. The underlying problem and the effect of the fix is somewhat misuderstood.
- **Failed**: The flaw is missing, or otherwise inappropriate

## Flaws

### Flaw 1: [Cryptographic failure](https://owasp.org/Top10/A02_2021-Cryptographic_Failures/)

[Exposed environmental secret](https://github.com/tuukkalai/cheese/blob/main/cheese/settings.py#L26) can be seen as a Cryptographic failure. The value is not exposed within the application, but with searching the web with couple of keywords attacker might find this repository and use the key to gain control of the complete application.

To fix this issue,

  1. import dotenv package ([Uncomment import](https://github.com/tuukkalai/cheese/blob/main/cheese/settings.py#L15))
  2. save the `SECRET_KEY` to `.env`-file
  3. add `.env`-file to `.gitignore`
  4. add `SECRET_KEY` to environmental variables in production system

### Flaw 2: [Injection](https://owasp.org/Top10/A03_2021-Injection/)

Adding query directly with raw-method and insecure way of adding user input in query.

Question ID is extracted from URL and injected directly to query. This allows attacker to craft a URL, that extracts data from database.

E.g. following URL prints admin users password hash on the screen: <http://127.0.0.1:8000/question/2%20AND%201%3D2%20UNION%20SELECT%20username,%20password,%20id,%20is_superuser%20FROM%20auth_user%20WHERE%20is_superuser%3D1/>

[comment]: <> (TODO: Suggested fix for SQL Injection vulnerability.)

### Flaw 3: [Identification and authentication failures](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/)

"Permits brute force or other automated attacks."

Brute forcing is available for logging in, and password for user `admin` is not that hard to guess.

To test this, activate the virtual environment and run command (assuming the application is running on localhost port 8000):

```sh
python hackpassword.py http://localhost:8000 xato-net-10-million-passwords-10000.txt
```

The script takes quite a long time. Subset of those 10000 passwords are collected in `xato-net-10-million-passwords-every-44th-of-10000.txt`. To test brute force with a subset of passwords, run

```sh
python hackpassword.py http://localhost:8000 xato-net-10-million-passwords-every-44th-of-10000.txt
```

To fix this issue the application should be updated to limit login attempts.

[comment]: <> (TODO: Login attempt limiter.)

The developer should also update default passwords in any frameworks used in application. Developers should actively avoid using passwords found in password lists and same password in different places. Password managers are handy to manage multiple credentials.

### Flaw 4: [Identification and Authentication Failures](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/)

In the application user can vote for given choices. Each question has set of available choices. User can vote within single question only once. Except by crafting the URL with different set of attributes.

In [`views.py]`(https://github.com/tuukkalai/cheese/blob/main/cheese/polls/views.py#L59) user is able to make a vote on other users behalf by setting another user's username in URL. User can also add multiple votes for his/her account.

To fix the issue, commented section on top of given line should be used.

### Flaw 5: [this and that](http://example.com)

exact source link pinpointing flaw 5...
description of flaw 5...
how to fix it...
