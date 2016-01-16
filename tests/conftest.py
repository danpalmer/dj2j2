import pytest
import subprocess

@pytest.fixture(scope='session')
def dj2j2():
    def inner(*args, **kwargs):
        call = list(args)
        call.insert(0, 'dj2j2')
        call.extend(['--%s=%s' % x for x in kwargs.items()])

        output = subprocess.Popen(call, stdout=subprocess.PIPE)
        output.wait()

        assert output.returncode == 0

        return str(output.stdout.read())

    return inner
