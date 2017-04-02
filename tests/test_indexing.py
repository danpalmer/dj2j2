def test_indexing(assert_equal):
    assert_equal(
        '{{ foo.0 }}',
        '{{ foo[0] }}',
    )


def test_slicing(assert_equal):
    assert_equal(
        '{{ foo|slice:":3" }}',
        '{{ foo[:3] }}',
    )
