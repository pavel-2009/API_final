import os
import sys
from os.path import abspath, dirname, join

root_dir = dirname(dirname(abspath(__file__)))
sys.path.insert(0, root_dir)
sys.path.insert(0, join(root_dir, 'api_yamdb'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_yamdb.settings')

import django
django.setup()

infra_dir_path = join(root_dir, 'infra')

pytest_plugins = [
]
