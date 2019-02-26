from mdtemplate import create_form
import os


def test_reset_output_dirs(remove_temporary_dirs):
    create_form.reset_temp_dir()
    dir = os.getcwd()
    content = os.listdir(create_form.TEMP_DIR)
    value = [create_form.TEMP_IMG_DIR.name]
    path = create_form.TEMP_DIR


    assert os.listdir(create_form.TEMP_DIR) == \
           [create_form.TEMP_IMG_DIR.name]
    assert os.listdir(create_form.OUTPUT_DIR) == []
