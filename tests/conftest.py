import pytest
from mdtemplate import create_form
from shutil import rmtree


@pytest.fixture()
def remove_temporary_dir_after_test():
    yield
    rmtree(create_form.TEMP_DIR)

@pytest.fixture()
def reset_temp_dir():
    create_form.reset_temp_dir()
