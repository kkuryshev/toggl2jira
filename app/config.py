#! /usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import dirname,abspath,join,exists
from os import getenv
import sys
import logging
from dotenv import load_dotenv

load_dotenv()

l = logging.getLogger('connectionpool')
l.setLevel(logging.INFO)

ROOT_PATH = join('..', dirname(abspath(__file__)))

ROOT_PROJECT_DIR = dirname(sys.modules['__main__'].__file__)

TOOGL_API_TOKEN = getenv('TOOGL_API_TOKEN')
JIRA_URL = getenv('JIRA_URL')
JIRA_LOGIN = getenv('JIRA_USER')
JIRA_PSWD = getenv('JIRA_PASS')

assert JIRA_LOGIN is not None
assert JIRA_PSWD is not None
