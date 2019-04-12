#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""Convenience wrapper for running bootstrap directly from source tree"""

from mdtemplate.create_form import main

if __name__ == "__main__":
    main(autostart=True, debug=False)

# Debug leads to second initialization of main() method,
# and opening false url (autostart=True) since port was changed but app
# still runs on initial port
