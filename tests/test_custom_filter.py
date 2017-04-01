custom_fitler_template = '{{ foo|bar }}'


def test_custom_filter(assert_fails):
    assert_fails(custom_fitler_template)


def test_custom_filter_record(transpile):
    output, report = transpile(custom_fitler_template)
    assert report.missing_custom_filters == set(['bar'])


def test_does_not_report_valid_filter(transpile):
    output, report = transpile('{{ foo|length|bar }}')
    assert report.missing_custom_filters == set(['bar'])


def test_does_not_include_filter_arguments(transpile):
    output, report = transpile('{{ foo|bar:"baz"|length }}')
    assert report.missing_custom_filters == set(['bar'])
