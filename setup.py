import os
from setuptools import setup

README = """
See the README on `GitHub
<https://github.com/uw-it-aca/django-splunk-logger>`_.
"""

# The VERSION file is created by travis-ci, based on the tag name
version_path = 'django-splunk-logger/VERSION'
VERSION = open(os.path.join(os.path.dirname(__file__), version_path)).read()
VERSION = VERSION.replace("\n", "")

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

url = "https://github.com/uw-it-aca/django-splunk-logger"
setup(
    name='DjangoSplunkLogger',
    version=VERSION,
    packages=['django-splunk-logger'],
    author="UW-IT AXDD",
    author_email="aca-it@uw.edu",
    include_package_data=True,
    install_requires=['Django<3',
                      'requests'],
    license='Apache License, Version 2.0',
    description=('A Python log handler for forwarding log events to Splunk'),
    long_description=README,
    url=url,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
    ],
)


