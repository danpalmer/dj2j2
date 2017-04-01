def test_now(assert_equal):
    assert_equal(
        '{% now "jS F Y H:i" %}',
        "{{ now('jS F Y H:i') }}",
    )


def test_now_as(assert_equal):
    assert_equal(
        '{% now "jS F Y H:i" as foo %}',
        "{% set foo = now('jS F Y H:i') %}",
    )


def test_now_usage_requires_django_compat_library(transpile):
    _, report = transpile('{% now "Y" %}')
    assert report.requires_django_compat
