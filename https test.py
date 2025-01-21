from flask import Flask

app = Flask(__name__)

@app.route('/.well-known/pki-validation/3C48C5164D512ECF2A23C95CB646173D.txt')
def home():
    return "0E7ECA189097681501D01AB17F6B65C180848C35B467B8852C1801104FCFDE95\ncomodoca.com\n06f5778dad2e05b"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, ssl_context=('cert.pem', 'key_without_passphrase.pem'))
