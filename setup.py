import sys
import os
from setuptools import setup, find_packages
from stuntcat import __version__

here = os.path.abspath(os.path.dirname(__file__))

name = "stuntcat"

from io import open
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

freeze_cmds = ["bdist_dmg", "bdist_msi", 'build_exe', 'bdist_mac']
if any(x in sys.argv for x in freeze_cmds):
    # https://cx-freeze.readthedocs.io/en/latest/distutils.html
    # Note: we needed to use git cx_freeze because it does not work on mac py3.7.
    #     git+https://github.com/anthony-tuininga/cx_Freeze.git
    #
    from cx_Freeze import setup, Executable

    import cx_Freeze.hooks
    if not hasattr(cx_Freeze.hooks, 'load_pymunk'):
        def load_pymunk(finder, module):
            """The chipmunk.dll or .dylib or .so is included in the package.
               But it is not found by cx_Freeze, so we include it.
            """
            import pymunk
            finder.IncludeFiles(pymunk.chipmunk_path,
                    os.path.join(os.path.basename(pymunk.chipmunk_path)),
                    copyDependentFiles = False)
        cx_Freeze.hooks.load_pymunk = load_pymunk
    if not hasattr(cx_Freeze.hooks, 'load_pycparser'):
        def load_pycparser(finder, module):
            """ These files are missing which causes
                permission denied issues on windows when they are regenerated.
            """
            finder.IncludeModule("pycparser.lextab")
            finder.IncludeModule("pycparser.yacctab")
        cx_Freeze.hooks.load_pycparser = load_pycparser

    # Dependencies are automatically detected, but it might need fine tuning.
    build_exe_options = {
        "packages": [
            "os", "pygame", "sys", "typing", "random", "pyscroll", "pytmx", "thorpy", "pymunk"
        ],
        "excludes": ["tkinter"],
    }
    # GUI applications require a different base on Windows (the default is for a
    # console application).
    base = None
    if sys.platform.startswith("win"):
        base = "Win32GUI"

    options = {
        "build_exe": build_exe_options
    }
    executables = [Executable("run_game.py", base=base)]
    print("options, executables, base", options, executables, base)
else:
    options = {}
    executables = []




setup(
    name=name,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries :: pygame',
        'Topic :: Games/Entertainment :: Arcade',
    ],
    license='LGPL',
    author='stuntcat team',
    author_email='stuntcat@pygame.org',
    maintainer='stuntcat team',
    maintainer_email='stuntcat@pygame.org',
    description='Stuntcat is the first pygame 2 community game.',
    include_package_data=True,
    long_description=long_description,
    long_description_content_type='text/markdown',
    options=options,
    executables=executables,
    package_dir={'stuntcat': 'stuntcat'},
    packages=find_packages(),
    # package_data={'stuntcat': []},
    url='https://github.com/pygame/stuntcat',
    install_requires=[
        "pygame",
        "pyscroll",
        "pytmx",
        "thorpy",
        "pymunk>=5.4.2",
    ],
    version=__version__,
    extras_require={
        ':python_version < "3.5"': [
            'typing',
        ],
    },
    entry_points={
        'console_scripts': [
            'stuntcat=stuntcat.cli:main',
        ],
    },
)
