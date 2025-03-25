from setuptools import setup, find_packages
from pathlib import Path

long_description = (Path(__file__).parent / 'README.md').read_text()

setup(
	name='HoyoDL',
	version='0.1.3',
	description='Download any game file at any version of Hoyo games',
	author='Escartem',
	author_email='escartem.github@gmail.com',
	url='https://github.com/Escartem/HoyoDL',
	packages=find_packages(),
	long_description=long_description,
	long_description_content_type='text/markdown',
	install_requires=[
		'requests',
	],
	classifiers=[
		'Programming Language :: Python :: 3',
		'License :: Other/Proprietary License',
		'Operating System :: OS Independent',
	],
	python_requires='>=3.10',
)
