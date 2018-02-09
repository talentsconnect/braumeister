import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="Braumeister",
    version="0.0.5",
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
        'console_scripts': ["braumeister = Braumeister:main"]
    },
    python_requires='>=3.0',
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "Topic :: Software Development :: Version Control :: Git"
    ],
)
