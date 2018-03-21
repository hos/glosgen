from setuptools import setup

setup(
    name = 'glosgen',

    version = '0.0',

    description = '',

    author = 'Onur Solmaz',

    author_email = 'onursolmaz@gmail.com',

    packages = ['glosgen'],

    extras_require = {
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },

    setup_requires = [
        'nltk',
        'wiktionaryparser',
        'inflect',
        # 'ruamel.yaml',
    ],

    entry_points = {
        'console_scripts': [
            'glosgen=glosgen.glosgen:__main__',
        ],
    },
)



