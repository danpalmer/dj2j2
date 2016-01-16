import pytest

description = "A utility to transpile Django templates to Jinja2 templates."

def test_prints_help(dj2j2_run):
    output = dj2j2_run('--help')
    assert description in output

@pytest.mark.skipif('True')
def test_runs_for_file(dj2j2_run, data_path, tmpdir):
    dj2j2_run(
        infile=data_path('simple_1.html'),
        outfile=tmpdir.join('simple_1.out.html'),
    )

@pytest.mark.skipif('True')
def test_runs_for_directory(dj2j2_run, data_path, tmpdir):
    dj2j2_run(
        indir=data_path('simple_2'),
        outdir=tmpdir.join('simple_2.out'),
    )
