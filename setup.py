from setuptools import setup, find_packages

setup(
    name="mymra", 
    version="1.4.9.4",  
    packages=find_packages(include=["mymra"]),
    install_requires=[
        'pycryptodome', 
        'argparse', 
    ],
    description="A tool for embedding and extracting files and strings with AES encryption.",
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
