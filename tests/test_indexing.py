def test_indexing(assert_equal):
    assert_equal(
        '{{ foo.0 }}',
        '{{ foo[0] }}',
    )
