#!/usr/bin/env python3
# encoding: utf-8

import re
import setuptools

version = ''
with open('aioec/__init__.py') as f:
	version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

readme = ''
with open('README.rst') as f:
	readme = f.read()

setup(
	name='aioec',
	version='0.0.1',
	license='MIT',
	packages=['aioec'],
	description='async client library for the Emoji Connoisseur API',
	classifiers=[
		'Development Status :: 2 - Pre-Alpha',
		'Intended Audience :: Developers',
		'Topic :: Internet',
		'Topic :: Software Development :: Libraries',
		'Topic :: Software Development :: Libraries :: Python Modules',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Operating System :: OS Independent',
		'License :: OSI Approved :: MIT License',
	],
)
