#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "docker_django.settings")
    # to avoid oopsies in production:
    os.environ.setdefault("DJANGO_CONFIGURATION", "Prod")

    from configurations.management import execute_from_command_line

    execute_from_command_line(sys.argv)
