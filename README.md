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

Rename `ecssweb/settings.example.py` and changes the settings in it.
