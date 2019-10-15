import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nordic2json",
    version="0.0.1",
    description='Nordic Format to JSON converter',
	url='http://github.com/rtous/nordic2json',
	author='Ruben Tous',
	author_email='rtous@ac.upc.edu',
	license='MIT',
    packages=setuptools.find_packages(),
    scripts=['bin/nordic2json'],
    install_requires=[
          'obspy==1.1.1',
          'pandas==0.25.1'
    ]
)

