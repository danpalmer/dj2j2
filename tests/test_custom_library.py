custom_library_template = '{% load foo %}'


def test_custom_library(assert_fails):
    assert_fails(custom_library_template)


def test_custom_library_record(transpile):
    output, report = transpile(custom_library_template)
    assert report.missing_custom_libraries == ['foo']
