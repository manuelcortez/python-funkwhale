# Python Funkwhale: Python Wrapper for the Funkwhale API.

[![pipeline status](https://code.manuelcortez.net/manuelcortez/python-funkwhale/badges/master/pipeline.svg)](https://code.manuelcortez.net/manuelcortez/python-funkwhale/commits/master)

[![coverage report](https://code.manuelcortez.net/manuelcortez/python-funkwhale/badges/master/coverage.svg)](https://code.manuelcortez.net/manuelcortez/python-funkwhale/commits/master)

Python-funkwhale is a lightweight wrapper over the [Funkwhale](https://funkwhale.audio) API. Only dependent on [Requests,](https://2.python-requests.org/en/master/) the idea of this wrapper is to support as much of the [Funkwhale API](https://docs.funkwhale.audio/api.html) as possible and be ready for new additions without needing to add a single line of code. It supports a "magic" method of building API calls based in class attributes that will ensure new additions will work inmediately as soon as added to the server API.

## Installation

So far, the API wrapper is still considered unstable, a proper setup file is in the works. As soon as I can be sure everything works as expected, I will add a setup file here so it can be installed as a proper Pytohn package. For now, the only way to use this package is by copying the funkwhale folder in a directory present in os.path so it can be found during imports.

## usage

```
>>> from funkwhale import session
# Create the session instance (no login is performed at this step).
# Use the demo server and credentials.
>>> mySession = session.Session()
# Or provide your own data.
>>> mySession = session.Session(instance_endpoint="https://demo.funkwhale.audio", username="demo", password="demo")
# Alternatively, if you already have a JWT token you can pass it to the session class
>>> mySession = session.Session(instance_endpoint="https://demo.funkwhale.audio", token="xxxxxxxxx")
# Do login.
>>> mySession.login()
# If username and password were provided, the login method generated already the JWT token.
# You can save this somewhere for passing it later.
>>> print(mySession.token)
xxxxxxxxx
# Create the API object, that will be responsible for calling the funkwhale's server.
>>> api = mySession.get_api()
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
# In some situations, Funkwhale returns partial or full URLS in some API calls.
# We can use the direct_post and direct_get in the api object for calling the requests methods
# This will call requests.get and requests.post without any magic in the API.
# for example, to retrieve a next page after calling to api.artists.get, there is a key called next.
>>> print(artists["next"])
http://demo.funkwhale.audio:80/api/v1/artists/?page=2&page_size=5
# In this case we will not use api.artists.get because it builds the URL based in class attributes.
# Instead we just use the direct_get method.
>>> next_artists = api.direct_get(artists["next"])
>>> for i in  next_artists["results"]:
...     print(i["name"])
...
Nine Inch Nails
Neon NiteClub
Igor Pumphonia
MicheyQ
JekK
# also, we can pass partial URLS such as /api/v1/listen/track_id to the API.
# the API has a function called full_url which will convert the URL properly into a full URL so it can be used in other apps
# Or used to be called with direct_post/direct_get
# This kind of URL is returned by funkwhale in tracks, for example.
# retrieve a single Track.
>>> track = api.tracks.get(1)
# the listen_url is a partial URL so we cannot pass it directly to request methods.
>>> print (tracks["listen_url"])
/api/v1/listen/778e01b2-85d9-4f73-b30d-3007a011c5f3/
# Convert it to a full URL which will be accepted by all request methods and in other apps
# As long as the provided credentials are valid.
>>> api.full_url(track["listen_url"])
https://demo.funkwhale.audio/api/v1/listen/778e01b2-85d9-4f73-b30d-3007a011c5f3/
>>>
```

More usage examples are located in the tests directory. Also You can see all available methods directly in the [Funkwhale interactive API.](https://docs.funkwhale.audio/swagger/)