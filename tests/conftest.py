import pytest
import os
from mdtemplate import create_form
from shutil import rmtree


@pytest.fixture()
def remove_temporary_dir_after_test():
    yield
    if os.path.exists(create_form.TEMP_DIR):
        rmtree(create_form.TEMP_DIR)


@pytest.fixture()
def reset_temp_dir():
    create_form.reset_temp_dir()
