def test_url(assert_equal):
    assert_equal(
        '{% url "foo:bar" %}',
        '{{ url(\'foo:bar\') }}',
    )

def test_url_var(assert_equal):
    assert_equal(
        '{% url my_url %}',
        '{{ url(my_url) }}',
    )

def test_url_with_arg(assert_equal):
    assert_equal(
        '{% url "foo:bar" baz %}',
        '{{ url(\'foo:bar\', baz) }}',
    )

def test_url_with_args(assert_equal):
    assert_equal(
        '{% url "foo:bar" baz "qux" %}',
        '{{ url(\'foo:bar\', baz, \'qux\') }}',
    )

def test_url_with_kwarg(assert_equal):
    assert_equal(
        '{% url "foo:bar" x=foo %}',
        '{{ url(\'foo:bar\', x=foo) }}',
    )

def test_url_with_kwargs(assert_equal):
    assert_equal(
        '{% url "foo:bar" x=baz y="qux" %}',
        '{{ url(\'foo:bar\', x=baz, y=\'qux\') }}',
    )

def test_url_as(assert_equal):
    assert_equal(
        '{% url "foo:bar" as my_url %}',
        '{% set my_url = url(\'foo:bar\') %}',
    )
