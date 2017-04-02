def test_indexing(transpile):
    _, report = transpile('{{ foo.7_days }}')

    expected = "'7_days' cannot start with a digit in Jinja templates"

    assert len(report.failed_files) == 1
    assert str(list(report.failed_files.values())[0]) == expected
