def test_with_as(assert_equal):
    assert_equal(
        '{% with foo as bar %}{% endwith %}',
        '{% with bar=foo %}{% endwith %}',
    )

def test_with_equals(assert_equal):
    assert_equal(
        '{% with foo=bar %}{% endwith %}',
        '{% with foo=bar %}{% endwith %}',
    )

def test_with_equals_multiple(assert_equal):
    assert_equal(
        '{% with foo=bar x=y %}{% endwith %}',
        '{% with foo=bar, x=y %}{% endwith %}',
    )

def test_with_will_require_extension(transpile):
    _, report = transpile('{% with foo as bar %}{% endwith %}')
    assert 'jinja2.ext.with_' in report.required_extensions
