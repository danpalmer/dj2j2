import dj2j2

def test_empty_identity():
    assert dj2j2.transpile_content('') == ''

def test_identity():
    assert dj2j2.transpile_content('foo') == 'foo'

def test_identity_long(data_file):
    out = dj2j2.transpile_content(data_file('simple_1.html'))
    expected = data_file('simple_1.out.html')
    assert out == expected
