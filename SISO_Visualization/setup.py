from setuptools import setup, find_packages

setup(
    name='SISO_GANTT',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'matplotlib',
        'mplcursors'
    ],
    entry_points={
        'console_scripts': [
            'TestDatavisualisation = TestDatavisualisation:main',
        ],
    },
)
