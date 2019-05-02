import pytest
import os

# import logging
# import os
# logging.warning(os.getcwd())

from mdtemplate import mdtemplate
from shutil import rmtree


@pytest.fixture()
def remove_temporary_dir_after_test():
    yield
    if os.path.exists(mdtemplate.TEMP_DIR):
        rmtree(mdtemplate.TEMP_DIR)


@pytest.fixture()
def reset_temp_dir():
    mdtemplate.TemplateArchiver._reset_temp_dir()
