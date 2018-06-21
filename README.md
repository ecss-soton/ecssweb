# ecssweb

Website for the University of Southampton Electronics and Computer Science Society

https://society.ecs.soton.ac.uk

## Documents

To find out more about models of ecssweb, see the [wiki](https://github.com/ecss-soton/ecssweb/wiki)

## Requirements and Installation

- Requires Python 3 to run the Django 2.0 project

- `python3-saml` requires `xmlsec`, it needs some pre-install steps:

  On Mac:

    ```
    brew install libxml2 libxmlsec1
    ```

  On Linux (Debian):

    ```
    apt-get install libxml2-dev libxmlsec1-dev libxmlsec1-openssl
    wget http://xmlsoft.org/sources/libxml2-2.9.1.tar.gz
    tar -xvf libxml2-2.9.1.tar.gz
    cd libxml2-2.9.1
    ./configure && make && make install
    ```

    If it fails you might need to run `apt-get install python3-dev` and then try again.

  For other platforms see https://github.com/mehcode/python-xmlsec#pre-install

- Install the packages in `requirements.txt`

  ```
  pip install -r requirements.txt
  ```

## Configuration

- Rename `ecssweb/settings.example.py` to `settings.py` and changes the settings in it
- After migrate database schema, load initial data using `python manage.py loaddata init_data.example.yaml`

### SAML

- Rename `ecsswebauth/saml_config/settings.example.json` to `settings.json` and changes the settings in it

- Put your X.509 certs in `ecsswebauth/saml_config/certs/` name them `sp.crt` and `sp.key`
  
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

## License

Licensed under the [MIT license](LICENSE).
