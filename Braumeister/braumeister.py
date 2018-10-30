# -*- coding: utf-8 -*-

from .core import Core

"""braumeister.braumeister: provides entry point main()."""

__version__ = "0.3.3"


def main():
    b = Core()
    b.bootstap()
