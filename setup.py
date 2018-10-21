#!/usr/bin/env python3
# encoding: utf-8

import re
import setuptools

with open('ec_client/__init__.py') as f:
	version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

with open('README.rst') as f:
	readme = f.read()

setuptools.setup(
	name='ec_client',
	author='Benjamin Mintz',
	author_email='bmintz@protonmail.com',
	url='https://github.com/EmoteCollector/ec_client',
	version=version,
	license='MIT',
	packages=['ec_client'],
	install_requires=['requests>=2.0.0,<3.0.0'],
	description='client library for the Emote Collector API',
	long_description=readme,
	classifiers=[
		'Development Status :: 2 - Pre-Alpha',
		'Intended Audience :: Developers',
		'Topic :: Internet',
		'Topic :: Software Development :: Libraries',
		'Topic :: Software Development :: Libraries :: Python Modules',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Operating System :: OS Independent',
		'License :: OSI Approved :: MIT License',
	],
)
