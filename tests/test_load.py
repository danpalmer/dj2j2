def test_load(assert_equal):
    assert_equal('{% load cache %}', '')


def test_load_records_required_load(transpile):
    output, report = transpile('{% load cache %}')
    assert list(report.required_libraries.values())[0][0].lineno == 1
    assert list(report.required_libraries.keys()) == ['cache']


def test_load_multiple(assert_equal):
    assert_equal('{% load cache tz %}', '')


def test_load_multiple_records_required_loads(transpile):
    output, report = transpile('{% load cache tz %}')
    assert sorted(report.required_libraries.keys()) == ['cache', 'tz']
