from setuptools import setup
from os.path import abspath, dirname, join
import re

CURDIR = dirname(abspath(__file__))
version = re.search(r'^__version__\s*=\s*"(.*)"',
                    open('mdtemplate/create_form.py').read(), re.M).group(1)

with open(join(CURDIR, "requirements.txt")) as f:
    REQUIREMENTS = f.read().splitlines()


setup(
    name="mdtemplate",
    version=version,
    package_dir={
        "mdtemplate": "mdtemplate",
    },
    packages=["mdtemplate"],
    include_package_data=True,
    entry_points={
      "console_scripts": ["mdtemplate = mdtemplate.create_form:main"]
    },
    author="Arne Wohletz",
    author_email="arnewohletz@gmx.de",
    description="Web app for markdown template creation",
    install_requires=REQUIREMENTS
)