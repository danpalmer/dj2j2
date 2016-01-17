def test_extends(assert_equal):
    assert_equal(
        '{% extends \'foo/bar.html\' %}',
        '{% extends \'foo/bar.html\' %}',
    )

def test_extends_with_content(assert_equal):
    assert_equal(
        '{% extends \'foo/bar.html\' %}Foobar',
        '{% extends \'foo/bar.html\' %}Foobar',
    )

def test_extends_with_filter(assert_equal):
    assert_equal(
        '{% extends \'foo/Bar.html\'|lower %}Foobar',
        '{% extends \'foo/Bar.html\'|lower %}Foobar',
    )

def test_extends_with_var(assert_equal):
    assert_equal(
        '{% extends foo %}Foobar',
        '{% extends foo %}Foobar',
    )

def test_extends_with_var_and_filter(assert_equal):
    assert_equal(
        '{% extends foo|lower %}Foobar',
        '{% extends foo|lower %}Foobar',
    )

def test_extends_with_filter_args(assert_equal):
    assert_equal(
        '{% extends foo|join:".html" %}Foobar',
        '{% extends foo|join(\'.html\') %}Foobar',
    )
