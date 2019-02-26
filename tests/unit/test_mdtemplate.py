from configparser import ConfigParser

from mdtemplate import create_form
import os
import pytest
import configparser


def test_reset_output_dirs(remove_temporary_dirs):
    create_form.reset_temp_dir()
    dir_content = os.listdir(create_form.os.getcwd())
    temp_dir_name = create_form.TEMP_DIR.name

    assert temp_dir_name in dir_content


def test_prepare_files(monkeypatch):
    def get_mocked_user_input():
        config: ConfigParser = configparser.ConfigParser()
        config.read('../tests/unit/form_data.ini')
        user_input = config['form_data']
        return user_input

    monkeypatch.setattr(create_form, "get_user_input",
                        get_mocked_user_input)

    create_form.reset_temp_dir()
    create_form.prepare_files()

    files = os.listdir(create_form.TEMP_DIR)

    import re
    css_regex = re.compile(r'.*\.css')

    for item in files:
        css_regex.findall(files)

    filter(css_regex.match, files)

    assert r".*\.css" in files
