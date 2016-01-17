import os
import pytest
import subprocess

import dj2j2

from dj2j2.jinja_env import jinja_environment

@pytest.fixture(scope='session')
def dj2j2_run():
    def inner(*args, **kwargs):
        call = list(args)
        call.insert(0, 'dj2j2')
        call.extend(['--%s=%s' % x for x in kwargs.items()])

        output = subprocess.Popen(call, stdout=subprocess.PIPE)
        output.wait()

        return_text = str(output.stdout.read())

        assert output.returncode == 0, return_text
        return return_text

    return inner

@pytest.fixture(scope='session')
def data_path():
    def inner(name):
        return os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'test_data',
            name,
        )

    return inner

@pytest.fixture(scope='session')
def data_file(data_path):
    def inner(name):
        with open(data_path(name)) as f:
            return f.read()
    return inner

@pytest.fixture(scope='session')
def transpile():
    def inner(content):
        report = dj2j2.Report()
        output = dj2j2.transpile_content(report, content)
        jinja_environment.from_string(output)
        return output, report
    return inner

@pytest.fixture(scope='session')
def assert_equal(transpile):
    def inner(first, second):
        output, report = transpile(first)
        assert second == output
        return output, report
    return inner
