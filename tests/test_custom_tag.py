custom_tag_template = '{% static_absolute "foo" %}'


def test_custom_tag(assert_fails):
    assert_fails(custom_tag_template)


def test_custom_tag_record(transpile):
    output, report = transpile(custom_tag_template)
    assert report.missing_custom_tags == set(['static_absolute'])
