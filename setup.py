from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="mymra", 
    version="1.4.9.9",  
    packages=find_packages(include=["mymra"]),
    install_requires=[
        'pycryptodome',
    ],
    description="A tool for embedding and extracting files and strings with AES encryption.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author = 'Oleg Beznogy',
    author_email = 'olegbeznogy@gmail.com',
    url="https://github.com/moshiax/mymra",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'mymra=mymra.mymra:main', 
        ],
    },
)