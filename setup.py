import os

from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='Flask-Material',
    version='0.0.5',
    url='https://github.com/HellerCommaA/flask-materialize',
    license='MIT',
    author='Adam Heller',
    author_email='heller@mailbox.org',
    description='An extension that includes Materialize CSS (http://materializecss.com/) in your '
                'project, without any boilerplate code.',
    long_description=read('README.rst'),
    packages=['flask_material'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask>=0.8',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
