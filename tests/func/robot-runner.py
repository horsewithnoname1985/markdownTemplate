#!/usr/bin/env/python
import os
import argparse
import subprocess
from pathlib import Path

# Keep this for later fixing: debugger doesn't work if using PosixPaths
# ("object of type 'PosixPath' has no len()" appears at start and breakpoints
# don't stop execution)
# ===========================================================================
# ROOT_DIR = Path(os.path.abspath(__file__)).parent
# RESULT_DIR = Path(ROOT_DIR.joinpath('Results'))
# SRC_DIR = ROOT_DIR.joinpath('mdtemplate')
# ACCEPTANCE_TEST_DIR = ROOT_DIR.joinpath('Tests')
# TEST_LIB_DIR = ROOT_DIR.joinpath('Libraries')
# VARIABLES_DIR = ROOT_DIR.joinpath('Resources/_Variables')
#===========================================================================

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULT_DIR = os.path.join(ROOT_DIR, 'Results')
SRC_DIR = os.path.join(ROOT_DIR, 'mdtemplate')
ACCEPTANCE_TEST_DIR = os.path.join(ROOT_DIR, 'Tests')
TEST_LIB_DIR = os.path.join(ROOT_DIR, 'Libraries')
VARIABLES_DIR = os.path.join(ROOT_DIR, 'Resources/_Variables')

ROBOT_OPTIONS = [
    '--outputdir', str(RESULT_DIR),
    '--pythonpath', str(SRC_DIR),
    # '--variable', 'BROWSER:{browser}',
    '--variable', 'SRC_DIR:{}'.format(str(SRC_DIR)),
    '--variable', 'VARIABLES_DIR:{}'.format(str(VARIABLES_DIR)),
    '--pythonpath', str(TEST_LIB_DIR)
]


def execute_tests(interpreter, browser, rf_options):
    options = []
    # set basic runner command
    runner = interpreter.split() + ['-m', 'robot.run']
    # add all robot options to options list while replacing browser string
    options.extend([opt.format(browser=browser) for opt in ROBOT_OPTIONS])
    # add all additional command line options
    options.extend(rf_options)
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
