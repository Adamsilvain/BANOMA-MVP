#!/usr/bin/env python
import os
import sys

if _name_ == "_main_":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "banoma_api.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
