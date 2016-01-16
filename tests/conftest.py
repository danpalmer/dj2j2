import os
import pytest
import subprocess

import dj2j2
from jinja2 import Template as JTemplate

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
def assert_equal():
    def inner(first, second):
        output = dj2j2.transpile_content(first)
        assert output == second
        JTemplate(output)
    return inner
