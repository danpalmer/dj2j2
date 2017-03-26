def test_empty_identity(assert_equal):
    assert_equal('', '')


def test_identity(assert_equal):
    assert_equal('foo', 'foo')


def test_identity_long(data_file, assert_equal):
    input_content = data_file('simple_1.html')
    expected = data_file('simple_1.out.html')
    assert_equal(input_content, expected)
