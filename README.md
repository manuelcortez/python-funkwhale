# Python Funkwhale: Python Wrapper for the Funkwhale API.

[![pipeline status](https://code.manuelcortez.net/manuelcortez/python-funkwhale/badges/master/pipeline.svg)](https://code.manuelcortez.net/manuelcortez/python-funkwhale/commits/master)

[![coverage report](https://code.manuelcortez.net/manuelcortez/python-funkwhale/badges/master/coverage.svg)](https://code.manuelcortez.net/manuelcortez/python-funkwhale/commits/master)

Python-funkwhale is a lightweight wrapper over the [Funkwhale](https://funkwhale.audio) API. Only dependent on [Requests,](https://2.python-requests.org/en/master/) the idea of this wrapper is to support as much of the [Funkwhale API](https://docs.funkwhale.audio/api.html) as possible and be ready for new additions without needing to add a single line of code. It supports a "magic" method of building API calls based in class attributes that will ensure new additions will work inmediately as soon as added to the server API.

## Installation

So far, the API wrapper is still considered unstable, a proper setup file is in the works. As soon as I can be sure everything works as expected, I will add a setup file here so it can be installed as a proper Pytohn package. For now, the only way to use this package is by copying the funkwhale folder in a directory present in os.path so it can be found during imports.

## usage

```
>>> from funkwhale import api
# Create the session instance (no login is performed at this step).
# Use the demo server and credentials.
>>> session = api.Session()
# Or provide your own data.
>>> session = api.Session(instance_endpoint="https://demo.funkwhale.audio", username="demo", password="demo")
# Alternatively, if you already have a JWT token you can pass it to the session class
>>> session = api.Session(instance_endpoint="https://demo.funkwhale.audio", token="xxxxxxxxx")
# Do login.
>>> session.login()
# If username and password were provided, the login method generated already the JWT token.
# You can save this somewhere for passing it later.
>>> print(session.token)
xxxxxxxxx
# Create the API object, that will be responsible for calling the funkwhale's server.
>>> api = session.get_api()
# all API calls follow the format "path.to.api.method(key=value, other_key=other_value)"
# where method can be get and post.
# Retrieve only 5 artists in the current instance.
>>> artists = api.artists.get(page_size=5)
# the data is always a dictionary and we can do something with it already.
>>> for i in artists["results"]:
...     print(i["name"])
...
DJ Black Red
The.madpix.project
Cortéz
Solar Phasing
Professor Kliq
# Some methods have been modified a little from the original API paths due to pytohn's syntax.
# For example, for calling  /api/v1/artists/{id}/libraries
# in python-funkwhale it will be translated as the following call, just removing the {id} part from the path and passing it as an argument to the function.
>>> libraries = api.artists.libraries.get(1)
>>> for i in libraries["results"]:
...     print(i["name"])
...
Demo library
>>>
```

More usage examples are located in the tests directory. Also You can see all available methods directly in the [Funkwhale interactive API.](https://docs.funkwhale.audio/swagger/)