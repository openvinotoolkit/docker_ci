# -*- coding: utf-8 -*-
"""Auxiliary authentification details for Snyk security scanning"""
import os

from utils.utilities import check_printable_utf8_chars

# Snyk API base URL for all API endpoints
SNYK_API = check_printable_utf8_chars(os.getenv('SNYK_API', 'https://snyk.io/api/v1/'))
# Snyk API token, obtained from https://app.snyk.io/account to run SDL tests
SNYK_TOKEN = check_printable_utf8_chars(os.getenv('SNYK_TOKEN', ''))
# test comment
