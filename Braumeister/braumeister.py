# -*- coding: utf-8 -*-

from .core import Core

"""braumeister.braumeister: provides entry point main()."""

__version__ = "0.4.0"


def main():
    b = Core()
    b.bootstap()
