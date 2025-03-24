from setuptools import setup, find_packages

setup(
	name='HoyoDL',
	version='0.1.0',
	description='Download any game file at any version of Hoyo games',
	author='Escartem',
	author_email='escartem.github@gmail.com',
	url='https://github.com/Escartem/HoyoDL',
	packages=find_packages(),
	install_requires=[
		'requests',
	],
	classifiers=[
		'Programming Language :: Python :: 3',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
	],
	python_requires='>=3.6',
)
