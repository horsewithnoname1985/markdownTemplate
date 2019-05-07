from setuptools import setup
from os.path import abspath, dirname, join
import re

CURDIR = dirname(abspath(__file__))
version = re.search(r'^__version__\s*=\s*"(.*)"',
                    open('mdtemplate/mdtemplate.py').read(), re.M).group(1)

with open(join(CURDIR, "requirements.txt")) as f:
    REQUIREMENTS = f.read().splitlines()


setup(
    name="mdtemplate",
    version=version,
    package_dir={
        "mdtemplate": "mdtemplate",
    },
    packages=["mdtemplate", "wsgi"],
    include_package_data=True,
    entry_points={
        "console_scripts": ["mdtemplate = wsgi.wsgi_runner:main"]
    },
    author="Arne Wohletz",
    author_email="arnewohletz@gmx.de",
    description="Web app_unused for markdown template creation",
    install_requires=REQUIREMENTS
)