#!/usr/bin/env python
import os
import argparse
import subprocess
from pathlib import Path

ROOT_DIR = Path(os.path.abspath(__file__)).parent.parent
RESULT_DIR = Path(ROOT_DIR.joinpath('tests/func/Results'))
SRC_DIR = ROOT_DIR.joinpath('mdtemplate')
ACCEPTANCE_TEST_DIR = ROOT_DIR.joinpath('tests/func/Tests')

ROBOT_OPTIONS = [
    '--outputdir', str(RESULT_DIR),
    '--pythonpath', str(SRC_DIR),
    '--variable', 'BROWSER:{browser}'
]


def execute_tests(interpreter, browser, rf_options):
    options = []
    # set basic runner command
    runner = interpreter.split() + ['-m', 'robot.run']
    # add all robot options to options list while replacing browser string
    options.extend([opt.format(browser=browser) for opt in ROBOT_OPTIONS])
    # create command by taking basic runner command and adding option list
    command = runner
    command += options + [ACCEPTANCE_TEST_DIR]
    # run resulting command
    subprocess.call(command)


if __name__ == "__main__":
    # set up argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--interpreter', '-I',
                        default='python',
                        help="Python interpreter")
    parser.add_argument('--browser', '-B',
                        help="Use 'firefox' or 'chrome'")
    # get given arguments
    args, rf_options = parser.parse_known_args()

    # assign arguments to variables
    interpreter = args.interpreter
    browser = args.browser.lower().strip()

    execute_tests(interpreter, browser, rf_options)
