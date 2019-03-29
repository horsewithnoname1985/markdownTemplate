from configparser import ConfigParser
from mdtemplate import create_form
from pathlib import Path
import os
import configparser
from os.path import dirname


BASE_DIR = Path(dirname(os.path.abspath(__file__)))


def get_mocked_user_input():
    config: ConfigParser = configparser.ConfigParser()
    config.read(BASE_DIR.joinpath('form_data.ini'))
    user_input = config.items(config.sections()[0])
    return dict(user_input)


def test_reset_output_dirs(remove_temporary_dir_after_test):
    """
    GIVEN the temp dir is not available
    WHEN the temp dir is reset
    THEN the temp dir is available
    """
    create_form.TemplateArchiver._reset_temp_dir()
    dir_content = os.listdir(create_form.os.getcwd())
    temp_dir_name = create_form.TEMP_DIR.name

    assert temp_dir_name in dir_content


# TODO: This test is too wide -> reduce to prepare markdown / script
def test_template_archiver(mocker) -> None:
    """
    GIVEN user has input data
    WHEN an archive file is created by this user data
    THEN the proper html template file is copied into the temp output dir
    """

    with mocker.patch(
            "mdtemplate.create_form.UserInputData") as MockedUserData:
        data = get_mocked_user_input()
        MockedUserData.language = data["language"]
        MockedUserData.author = data["author"]
        MockedUserData.date = data["date"]
        MockedUserData.project = data["project"]
        MockedUserData.style = data["style"]
        MockedUserData.title = data["title"]
        MockedUserData.filename = data["filename"]

        create_form.TemplateArchiver(MockedUserData)
        html_template_file_name = MockedUserData.style + "_template_" + \
                                  MockedUserData.language + ".html"
        assert os.path.exists(
            create_form.TEMP_DIR.joinpath(html_template_file_name))


def test_copy_to_temp(tmpdir,
                         reset_temp_dir,
                         remove_temporary_dir_after_test) -> None:
    """
    GIVEN a file is created in any directory
    WHEN the file is passed into the
        PredefinedTemplateFile.copy_to_temp() method
    THEN this file is copied into the temp output directory
    """
    testfile_name = 'test.txt'
    testfile = tmpdir.join(testfile_name)
    testfile.write('Unimportant content')
    testfile = Path(testfile)

    create_form.PredefinedTemplateFile.copy_to_temp(
        source=testfile,
        destination=create_form.TEMP_DIR.joinpath(testfile_name))

    assert os.path.exists(create_form.TEMP_DIR.joinpath(testfile_name))
