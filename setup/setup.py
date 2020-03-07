"""Reads the contents of setup.json for setting up the project"""
import json

SETUP_FILE = 'setup.json'

with open(SETUP_FILE) as setup_file:
    setup = json.load(setup_file)

project_name = setup['NAME']
CONFIG_FILE = setup['CONFIG_FILE']
