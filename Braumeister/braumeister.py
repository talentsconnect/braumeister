# -*- coding: utf-8 -*-

from .core import Core

"""braumeister.braumeister: provides entry point main()."""

def main():
    b = Core()
    b.bootstap()

if __name__ == '__main__':
    main()