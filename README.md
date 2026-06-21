# Care Privacy

This project implements a consent flow UI for users to revoke consent at any time.

## Features

* Revoke consent button on user profile page
* Revocation updates consent record status to 'revoked' and emits a webhook
* Revoked consent prevents AI service from accessing user's data

## Tests

Run tests using `python -m pytest`
