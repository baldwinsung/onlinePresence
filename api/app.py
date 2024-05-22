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

@app.route('/hostingprovider/<domain>', methods=['PUT'])
def hostingProvider(domain):
    result = dns.resolver.resolve(domain, 'A')
    for ipval in result:
        print ('IP', ipval.to_text())
        ip_apex = ipval.to_text()

        if ip_apex:
            print("A aka APEX Record:", ip_apex)
            lookup = IPWhois(ip_apex)
            p = lookup.lookup_rdap()
            if p['objects'] is not None:
                for x in p['objects']:
                    hosting_provider = p['objects'][x]['contact']['name']
                    print("Hosting Provider: ", hosting_provider)
                    return jsonify(hosting_provider)


@app.route('/sslcertificate_subject/<domain>', methods=['PUT'])
def sslCertificate_subject(domain):
    c = ssl.get_server_certificate((domain, 443), timeout=5)
    x = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, c)
    cn = x.get_subject()
    cn_str = "".join("/{:s}={:s}".format(name.decode(), value.decode()) \
                     for name, value in cn.get_components())

    return jsonify(cn_str.split('/')[1])

@app.route('/sslcertificate_issuer/<domain>', methods=['PUT'])
def sslCertificate_issuer(domain):
    c = ssl.get_server_certificate((domain, 443), timeout=5)
    x = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, c)
    cn = x.get_subject()
    cn_str = "".join("/{:s}={:s}".format(name.decode(), value.decode()) \
                     for name, value in cn.get_components())
    ir = x.get_issuer()
    ir_str = "".join("/{:s}={:s}".format(name.decode(), value.decode()) \
                     for name, value in ir.get_components())

    return jsonify(ir_str.split('/')[2])

@app.route('/sslcertificate_notbefore/<domain>', methods=['PUT'])
def sslCertificate_notbefore(domain):
    c = ssl.get_server_certificate((domain, 443), timeout=5)
    x = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, c)
    nb = datetime.strptime(x.get_notBefore().decode('ascii'), '%Y%m%d%H%M%SZ')

    return jsonify(nb)

@app.route('/sslcertificate_notafter/<domain>', methods=['PUT'])
def sslCertificate_notafter(domain):
    c = ssl.get_server_certificate((domain, 443), timeout=5)
    x = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, c)
    na = datetime.strptime(x.get_notAfter().decode('ascii'), '%Y%m%d%H%M%SZ')

    return jsonify(na)

@app.route('/sslcertificate_san/<domain>', methods=['PUT'])
def sslCertificate_san(domain):
    c = ssl.get_server_certificate((domain, 443), timeout=5)
    x = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, c)

    ec = x.get_extension_count()
    for i in range(0, ec):
        ge = x.get_extension(i)
        if 'subjectAltName' in str(ge.get_short_name()):
            s = ge.__str__()
            l = s.split(',')
            l.sort()

            return jsonify(l)



if __name__ == '__main__':
   app.run(port=5000)
