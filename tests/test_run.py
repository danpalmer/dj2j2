description = "A utility to transpile Django templates to Jinja2 templates."

def test_prints_help(dj2j2):
    output = dj2j2('--help')
    assert description in output
