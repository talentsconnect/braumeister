import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="braumeister",
    version="0.2.0",
    author="Marcel Steffen",
    author_email="marcel@talentsconnect.com",
    description="Easy release bulding, combining JIRA and git",
    long_description=read('README.md'),
    license="MIT",
    keywords="git jira release",
    url="https://www.talentsconnect.com",
    packages=find_packages(exclude=['ez_setup', 'tests', 'tests.*']),
    include_package_data=True,
    install_requires=['requests', 'colorama'],
    entry_points={
        'console_scripts': ["braumeister = braumeister:main"]
    },
    python_requires='!=2.7, !=3.4, >=3.5',
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "Topic :: Software Development :: Version Control :: Git"
    ],
)
