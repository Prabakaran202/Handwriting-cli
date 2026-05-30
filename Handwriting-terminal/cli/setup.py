# cli/setup.py
from setuptools import setup, find_packages

setup(
    name="writing-terminal",
    version="0.1.0",
    packages=find_packages(),
    install_packages=[
        "click",       # CLI கமாண்டுகளை எளிதாக்க
        "fastapi",     # பேக்கெண்ட் சர்வர்
        "uvicorn",     # வெப் சர்வர் ரன்னர்
        "pywebview",   # (ஆப்ஷனல்) தனி விண்டோவாக UI-ஐ காட்ட
    ],
    entry_points={
        'console_scripts': [
            'wt=wt_cli.main:cli', # டெர்மினலில் wt என டைப் செய்தால் main.py-ல் உள்ள cli() இயங்கும்
        ],
    },
)
