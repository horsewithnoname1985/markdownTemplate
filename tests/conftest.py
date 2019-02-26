import pytest
from mdtemplate import create_form
from shutil import rmtree


@pytest.fixture()
def remove_temporary_dirs():
    yield
    rmtree(create_form.TEMP_DIR)
    rmtree(create_form.OUTPUT_DIR)
