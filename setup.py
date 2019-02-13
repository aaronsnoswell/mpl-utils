from setuptools import setup

setup(
    name='mpl_utils',
    version='0.0.1a',
    description='A collection of plotting functions for Matplotlib',
    license='MIT',
    packages=['mpl_utils'],
    install_requires=[
        "matplotlib",
        "numpy",
        "scipy",
        "pandas",
    ],
    author='Aaron Snoswell',
    author_email='authornameatfastmaildotcom',
    keywords=['plotting', 'matplotlib'],
    url='https://github.com/aaronsnoswell/mpl-utils'
)
