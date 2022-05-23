# Cyber Security Base 2022 - Project I

Ths project is part of University of Helsinki course ["Cyber Security Base"](https://cybersecuritybase.mooc.fi/). The aim of this repository is to create an application with multiple security holes.

!! Do not use this repository as a template for your next Django-application !!

## Short description

- Introduce security flaws in software
- Provide steps to fix them

```text
Testing
Username: bob
Password: squarepants
```

## Checklist

- [ ] Five different flaws from OWASP Top ten list (selected 2021 list)
- [x] Application should have a backend (Python + Django)
- [x] Saved to public repo
- [ ] 1000 word report

### Report structure

```md
LINK: link to the repository
installation instructions if needed

FLAW 0 (example):
[Settings include exposed environmental variable `SECRET_KEY`](https://github.com/tuukkalai/cheese/blob/main/cheese/settings.py#L26)
Exposed environmental secret can be seen as a [Cryptographic failure](https://owasp.org/Top10/A02_2021-Cryptographic_Failures/). The value is not exposed within the application, but with searching the web with couple of keywords attacker might find this repository and use the key to gain control of the complete application.
To fix this issue,
  1. import dotenv package ([Uncomment import](https://github.com/tuukkalai/cheese/blob/main/cheese/settings.py#L15))
  2. save the `SECRET_KEY` to `.env`-file
  3. add `.env`-file to `.gitignore`
  4. add `SECRET_KEY` to environmental variables in production system

FLAW 1:
SQL Injection
polls > views > question()

exact source link pinpointing flaw 1...
description of flaw 1...
how to fix it...

FLAW 2:
exact source link pinpointing flaw 2...
description of flaw 2...
how to fix it...

...

FLAW 5:
exact source link pinpointing flaw 5...
description of flaw 5...
how to fix it...
```

## Scoring

The rubric for the scores are as follows:

- Failed: The flaw is missing, or otherwise inappropriate
- Passable: The flaw is identified correctly, the fix partially corrects the problem. The underlying problem and the effect of the fix is somewhat misuderstood.
- Average: The flaw described adequately and the fix fixes the problem. Minor misunderstanding of the underlying mechanism. The description is too vague but ultimately correct.
- Good: The flaw and the fix are correctly done. Minor issues in descriptions.
- Excellent: No issues or only cosmetic issues
