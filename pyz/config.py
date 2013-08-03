'''
The :mod:`config` module contains all the configuration available for the project. A default configuration is initially loaded, then a user configuration is loaded, if possible, and overwrites keys in the default configuration.
'''
from __future__ import print_function
import os
import yaml
import pkgutil
import logging

search_paths = [
    '.pyz_config',
    '~/.pyz_config'
    ]

setting = yaml.load(pkgutil.get_data('pyz', 'default_config.yml'))

conf = None
for path in search_paths:
    path = os.path.expanduser(path)
    if os.path.exists(path):
        with open(path, 'r') as f:
            user_conf = yaml.load(f.read())
            break
else:
    print('Configuration File Not Found!  Loading default configuration...')
    print('Paths searched:', search_paths)

    user_conf = {}

# TODO: Add plugin-specific configuration
for key, value in user_conf.iteritems():
    logging.debug('Overwriting {0} with {1}'.format(key, value))
    setting[key] = value
