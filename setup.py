import os
from codecs import open

from setuptools import setup, find_packages


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
VERSION = __import__('tapeforms').__version__


with open(os.path.join(BASE_DIR, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='django-tapeforms',
    version=VERSION,
    description='A helper to render Django forms using HTML templates.',
    long_description=long_description,
    url='https://github.com/stephrdev/django-tapeforms',
    project_urls={
        'Bug Reports': 'https://github.com/stephrdev/django-tapeforms/issues',
        'Source': 'https://github.com/stephrdev/django-tapeforms',
    },
    author='Stephan Jaekel',
    author_email='steph@rdev.info',
    packages=find_packages(exclude=['examples', 'docs', 'tests', 'tests.*']),
    install_requires=[],
    include_package_data=True,
    keywords='django forms',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
