import setuptools

import pydiff


NAME = 'PyReadableDiff'

DESCRIPTION = 'Intuitive human-readable diff for text'

# Use .rst markup for the long description in order to provide
# the link to the repository, since PyPI doesn't support .md markup,
# so we can't use the content of README.md for this purpose.
LONG_DESCRIPTION = 'For more detailed information about the library please ' \
                   'visit `the official repository ' \
                   '<https://github.com/BeagleInc/PyReadableDiff>`_.'

AUTHOR = 'Gevorg Davoian, Iulius Curt, Kevin Decker ' \
         '(the author of the original jsdiff library) and others'

AUTHOR_EMAIL = 'davoian.serf@gmail.com'

URL = 'https://github.com/BeagleInc/PyReadableDiff'

VERSION = pydiff.__version__

PACKAGES = setuptools.find_packages()

KEYWORDS = ['python', 'text', 'diff']

CLASSIFIERS = [
    "Intended Audience :: Developers",
    "License :: OSI Approved :: Apache Software License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Topic :: Software Development :: Libraries :: Python Modules"
]

LICENSE = 'Apache-2.0'


setuptools.setup(
    name=NAME,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    version=VERSION,
    packages=PACKAGES,
    keywords=KEYWORDS,
    classifiers=CLASSIFIERS,
    license=LICENSE
)
