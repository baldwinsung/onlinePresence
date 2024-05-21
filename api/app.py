import json
from flask import Flask, jsonify, request
from datetime import datetime
import ssl
import sys
import dns.resolver
import OpenSSL
import whois
from ipwhois import IPWhois

app = Flask(__name__)

@app.route('/', methods=['GET'])
def main_page():
    x = "main page, enter the target path"
    return jsonify(x)

@app.route('/domainwhois_registrar/<domain>', methods=['PUT'])
def domainWhois_registrar(domain):
    w = whois.whois(domain)
    return jsonify(w.registrar)

@app.route('/domainwhois_created/<domain>', methods=['PUT'])
def domainWhois_created(domain):
    w = whois.whois(domain)
    if type(w.creation_date) is list:
        return jsonify(w.creation_date[0])
    else:
        return jsonify(w.creation_date)

@app.route('/domainwhois_expires/<domain>', methods=['PUT'])
def domainWhois_expires(domain):
    w = whois.whois(domain)
    if type(w.expiration_date) is list:
        return jsonify(w.expiration_date[0])
    else:
        return jsonify(w.expiration_date)

if __name__ == '__main__':
   app.run(port=5000)
