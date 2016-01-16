import dj2j2

def test_empty_identity():
    assert dj2j2.transpile_content('') == ''

def test_identity():
    assert dj2j2.transpile_content('foo') == 'foo'
