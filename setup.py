from setuptools import setup

setup(
    name="integrate",
    author="Evgeny Khoroshavin",
    entry_points={
        'console_scripts': [
            'integrate = main:main'
        ]
    }
)
