# ecssweb

## Requirements and Installation

- Requires Python 3 to run the Django 2.0 project.

- `python3-saml` requires `xmlsec`, it needs some pre-install steps:

  On Mac:

  ```
  brew install libxml2 libxmlsec1
  ```

  For other platforms see https://github.com/mehcode/python-xmlsec#pre-install.

- Install the packages in `requirements.txt`

## Configuration

- Rename `ecssweb/settings.example.py` to `settings.py` and changes the settings in it.

### SAML

- Rename `auth/saml-config/settings.example.json` to `settings.json` and changes the settings in it.

- Put your X.509 certs in `auth/saml-config/certs/` name them `sp.crt` and `sp.key`
  
  You can run this to generate your certs:

  ```
  openssl req -new -x509 -days 3652 -nodes -out sp.crt -keyout sp.key
  ```

> For more information, see https://github.com/onelogin/python3-saml
