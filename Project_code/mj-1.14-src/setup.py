#!/usr/bin/env python

"""
setup.py file for SWIG example
"""

from distutils.core import setup, Extension


ga_player_module = Extension('_ga_player',
                           sources=['ga_player_wrap.c', 'ga_player.c','client.c','game.c','tiles.c','protocol.c','player.c','sysdep.c'],
                           )

setup (name = 'ga_player',
       version = '0.1',
       author      = "SWIG Docs",
       description = """Simple swig example from docs""",
       ext_modules = [ga_player_module],
       py_modules = ["ga_player"],
       headers=['client.h'],
       )