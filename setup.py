from setuptools import setup, find_packages

setup(
    name='vython',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'vython=src.main:main'
        ]
    }
)
