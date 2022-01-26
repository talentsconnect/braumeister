import os
import re

from setuptools import setup

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('braumeister/core.py').read(),
    re.M
).group(1)


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="braumeister",
    packages=["braumeister", "braumeister.actions"],
    version=version,
    author="Marcel Steffen",
    author_email="marcel@talentsconnect.com",
    description="Easy release bulding, combining JIRA and git",
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    license="MIT",
    keywords="git jira release",
    url="https://www.talentsconnect.com",
    include_package_data=True,
    install_requires=['requests', 'colorama'],
    entry_points={
        'console_scripts': ["braumeister = braumeister.braumeister:main"]
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
