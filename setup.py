import setuptools

import pydiff


setuptools.setup(
    name='PyReadableDiff',
    description='Intuitive human-readable diff for text',
    author='Gevorg Davoian, Iulius Curt, Kevin Decker (the author of the original jsdiff library) and others',
    author_email='davoian.serf@gmail.com',
    url='https://github.com/BeagleInc/PyReadableDiff',
    version=pydiff.__version__,
    packages=setuptools.find_packages(),
    license='Apache-2.0'
)
