# onlinePresence - api

Figure out the online presence for a company or academic institution via put methods.

Displays general information about the domain and SSL certificate.

Pay close attention to the expiration dates for both the domain and SSL certificates.

## Getting Started

Container or Flask

### Container

Build and run the container
```
docker build -t api .
docker run --name test -p 8000:5000 api
```

Test with google.
```
curl -X PUT http://localhost:8000/domainwhois_registrar/google.com
"MarkMonitor, Inc."

curl -X PUT http://localhost:8000/domainwhois_created/google.com
"Mon, 15 Sep 1997 04:00:00 GMT"

curl -X PUT http://localhost:8000/domainwhois_expires/google.com
"Thu, 14 Sep 2028 04:00:00 GMT"
```

### Running Flask locally

Install the dependencies. Use a virtual environment. Run Flask.

```
mkvirtualenv onlinePresence-api
pip install -r requirements.txt
flask run
```

Test the code with google.
```
curl -X PUT http://localhost:5000/domainwhois_registrar/google.com
"MarkMonitor, Inc."
```

# Credits

Richard Penman ( https://github.com/richardpenman ) for python-whois