from setuptools import setup

setup(
    name='artudistree',
    version='1.0',
    py_modules=['artudistree'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        artudistree=artudistree:create_tree
    ''',
)
