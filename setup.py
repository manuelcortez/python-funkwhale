from setuptools import setup

setup(name="funkwhale",
	version="0.1.0",
	author="Manuel cortez",
	author_email="manuel@manuelcortez.net",
	url="https://code.manuelcortez.net/manuelcortez/python-funkwhale",
	packages=["funkwhale"],
	long_description=open("readme.md", "r").read(),
	description="Python wrapper for the Funkwhale API.",
	install_requires=["requests"]
	)