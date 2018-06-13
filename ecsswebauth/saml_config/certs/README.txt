Put your X.509 certs here, and name them sp.crt and sp.key

You can run the following command to generate them:
openssl req -new -x509 -days 3652 -nodes -out sp.crt -keyout sp.key

For more info, read https://github.com/onelogin/python3-saml
