#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""Convenience wrapper for running bootstrap directly from source tree"""

from mdtemplate.mdtemplate import main

if __name__ == "__main__":
    main(autostart=True, debug=True)

# Debug mode activated leads to second initialization of main() method,
# and opening false url (autostart=True) since port was changed but app_unused
# still runs on initial port
