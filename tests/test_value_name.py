def test_indexing(transpile):
    _, report = transpile('{{ foo.7_days }}')
    assert report.failed_files == {None: "Identifiers cannot begin with digits"}
