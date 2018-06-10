# ecssweb

## Requirements and Installation

- Requires Python 3 to run the Django 2.0 project

- `python3-saml` requires `xmlsec`, it needs some pre-install steps:

  On Mac:

  ```
  brew install libxml2 libxmlsec1
  ```

  For other platforms see https://github.com/mehcode/python-xmlsec#pre-install

- Install the packages in `requirements.txt`

## Configuration

- Rename `ecssweb/settings.example.py` to `settings.py` and changes the settings in it

### SAML

- Rename `ecsswebauth/saml-config/settings.example.json` to `settings.json` and changes the settings in it

- Put your X.509 certs in `ecsswebauth/saml-config/certs/` name them `sp.crt` and `sp.key`
  
  You can run this to generate your certs:

  ```
  openssl req -new -x509 -days 3652 -nodes -out sp.crt -keyout sp.key
  ```

> For more information, see https://github.com/onelogin/python3-saml

## Maintenance

To regularly clear the inactive sessions and non-persistent users from the database, you can setup the cron job to it

- Give the `maintance.sh` script execute permission

  ```
  chmod u+x maintance.sh
  ```

- Run `crontab -e` to open the text editor and add the following line:

  ```
  0 0 * * * /path/to/project/maintance.sh /path/to/python/env/ /path/to/project/
  ```

  This makes the maintance script runs every day at midnight
