from setuptools import setup

classifiers = [
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 2",
    "Topic :: Software Development :: Libraries",
]

setup(
    name='Swagxamle',
    version='0.0.2',
    packages=['swagxample'],
    url='https://bitbucket.org/deginner/swagxample',
    license='MIT',
    classifiers=classifiers,
    author='deginner',
    author_email='support@deginner.com',
    description='An HTTP server application using Swagger 2.0, bitjws, and SQLAlchemy.',
    setup_requires=['pytest-runner'],
    install_requires=[
        'secp256k1==0.11',
        "bitjws==0.6.3.1",
        "flask>=0.10.0",
        "flask-login",
        "flask-bitjws>=0.1.1.2",
        "sqlalchemy-login-models"
    ],
    extras_require=["alchemyjsonschema", "flask-swagger"],
    tests_require=['pytest', 'pytest-cov']
)
