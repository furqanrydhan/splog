#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import setuptools

def setup():
    with open(os.path.join('src', 'splog.py'), 'r') as f:
        for line in f.readlines():
            if 'version' in line:
                try:
                    exec(line)
                    assert(isinstance(version, basestring))
                    break
                except (SyntaxError, AssertionError, NameError):
                    pass
    try:
        assert(isinstance(version, basestring))
    except (AssertionError, NameError):
        version = 'unknown'
    
    setuptools.setup(
        name='splog',
        version=version,
        description='StylePage tools: Python logging',
        author='mattbornski',
        url='http://github.com/stylepage/splog',
        package_dir={'': 'src'},
        py_modules=[
            'splog',
        ],
    )

if __name__ == '__main__':
    setup()