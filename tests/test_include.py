from dj2j2.report import Position

def test_include_simple(assert_equal):
    assert_equal('{% include "foo.html" %}', '{% include \'foo.html\' %}')

def test_include_var(assert_equal):
    assert_equal('{% include foo %}', '{% include foo %}')

def test_include_with_context(assert_equal):
    assert_equal(
        '{% include "foo.html" with x=bar %}',
        '{% with x=bar %}{% include \'foo.html\' %}{% endwith %}',
    )

def test_include_with_multiple_context(assert_equal):
    assert_equal(
        '{% include "foo.html" with x=bar baz=y z=w %}',
        '{% with baz=y, x=bar, z=w %}{% include \'foo.html\' %}{% endwith %}',
    )

def test_include_only(assert_equal):
    assert_equal(
        '{% include "foo.html" only %}',
        '{% include \'foo.html\' without context %}',
    )

def test_include_only_context(transpile):
    _, report = transpile('{% include "foo.html" with x=bar only %}')

    assert Position(1, None) in report.invalid_includes
