# -*- coding: utf-8 -*-
"""
Deprecated: use 'scripts/seed_all.py' or 'python manage.py seed_all'.
Redirecting to unified seed_all.
"""
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.seed_all import run_seeder

if __name__ == '__main__':
    run_seeder()
