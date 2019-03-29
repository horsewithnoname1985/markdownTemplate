from configparser import ConfigParser
from mdtemplate import create_form
from pathlib import Path
import os
import configparser
import shutil


def get_mocked_user_input():
    config: ConfigParser = configparser.ConfigParser()
    config.read('../tests/unit/form_data.ini')
    user_input = config['form_data']
    return user_input


def test_reset_output_dirs(remove_temporary_dir_after_test):
    """
    GIVEN the temp dir is not available
    WHEN the temp dir is reset
    THEN the temp dir is available
    """
    create_form.reset_temp_dir()
    dir_content = os.listdir(create_form.os.getcwd())
    temp_dir_name = create_form.TEMP_DIR.name

    assert temp_dir_name in dir_content


# TODO: This test is too wide -> reduce to prepare markdown / script
def test_prepare_files(monkeypatch):
    monkeypatch.setattr(create_form, "get_user_input",
                        get_mocked_user_input)

    create_form.reset_temp_dir()
    create_form.prepare_files()

    user_input = get_mocked_user_input()
    html_template_file_name = user_input['style'] + "_template_" + user_input[
        'language'] + ".html"

    assert os.path.exists(
        create_form.TEMP_DIR.joinpath(html_template_file_name))


def test_copy_to_temp(tmpdir,
                      reset_temp_dir,
                      remove_temporary_dir_after_test):
    a_file = tmpdir.join('test.txt')
    a_file.write('Unimportant content')
    a_file = Path(a_file)

    create_form.copy_to_temp(src=a_file)

    assert os.path.exists(create_form.TEMP_DIR.joinpath('test.txt'))
