import os,sys

from jproperties import Properties

"""
Read config
"""
props = Properties()
with open('config.properties', 'r') as f:
    props.load(f, 'utf-8')

"""
Placeholders
"""
HUB_HOST = props['hub_url'].data
HUB_HOST_PLACEHOLDER = '%hub_url%'

BROWSERS = props['target_browsers'].data.split(',')
BROWSERS_PLACEHOLDER = '%target_browser%'


def replace_placeholder(lines, browser):
    """
    in-place replace the placeholder
    :param browser: target browser name
    :param lines: target content
    :return: the new list
    """
    new_lines = []
    for line in lines:
        new_line = line.replace(HUB_HOST_PLACEHOLDER, HUB_HOST).replace(
            BROWSERS_PLACEHOLDER, browser)
        new_lines.append(new_line)
    return new_lines


def create_broswer_spec_file(root, filename):
    """
    Create browser specific test files from the original file
    :param root: the root dir
    :param filename: target file name
    :return: list of new file names
    """
    new_filenames = []
    with open(os.path.join(root, test_file), 'r') as f:
        lines = f.readlines()
        for browser in BROWSERS:
            new_contents = replace_placeholder(lines, browser)
            new_filename = browser + '_' + filename
            new_filenames.append(new_filename)
            with open(os.path.join(root, new_filename), 'w+') as out:
                out.writelines(new_contents)
    return new_filenames


def execute_test(filepath):
    """
    Execute the test
    :param filepath: test file path
    :return:
    """
    command = 'python ' + filepath
    ret_val = os.system(command)
    # print(ret_val)
    if ret_val != 0:
        sys.exit(ret_val)


if __name__ == "__main__":
    for root_dir, dirs, files in os.walk("../../SCENARIOS/"):
        for test_file in files:
            # print(test_file)
            if test_file.endswith(".py"):
                new_files = create_broswer_spec_file(root_dir, test_file)
                for new_file in new_files:
                    execute_test(os.path.join(root_dir, new_file))
