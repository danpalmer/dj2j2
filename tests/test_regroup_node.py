def test_simple_regroup(assert_equal):
    assert_equal(
        '{% regroup foo by bar as baz %}',
        "{% set baz = foo|groupby('bar') %}",
    )


def test_complex_regroup(assert_equal):
    assert_equal(
        '{% regroup foo|first by bar as baz %}',
        "{% set baz = foo|first|groupby('bar') %}",
    )


def test_complex_regroup_2(assert_equal):
    assert_equal(
        '{% regroup foo|dictsort:"1" by bar as baz %}',
        "{% set baz = foo|dictsort('1')|groupby('bar') %}",
    )


def test_complex_regroup_groupby_expression(assert_equal):
    assert_equal(
        '{% regroup foo|dictsort:"1" by bar.y.0 as baz %}',
        "{% set baz = foo|dictsort('1')|groupby('bar.y[0]') %}",
    )
