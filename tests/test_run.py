import subprocess

description = "A utility to transpile Django templates to Jinja2 templates."

def test_prints_help():
    call = subprocess.Popen(['dj2j2', '--help'], stdout=subprocess.PIPE)
    call.wait()
    assert call.returncode == 0
    assert description in str(call.stdout.read())
