#!/usr/bin/env python
import click

from jinja2 import Template as JTemplate
from django.template import Template as DTemplate

@click.command()
@click.option('--indir', help="Input directory")
@click.option('--outdir', help="Output directory")
def run(indir, outdir):
    """
    A utility to transpile Django templates to Jinja2 templates.
    """

    # Temporarily use files instead of directories
    transpile(indir, outdir)
    validate(outdir)

def transpile(infile_path, outfile_path):
    with open(infile_path, 'rb') as infile:
        with open(outfile_path, 'wb') as outfile:
            outfile.write(transpile_content(infile.read()))

def transpile_content(incontent):
    template = DTemplate(incontent)
    import ipdb; ipdb.set_trace()

def validate(outfile_path):
    try:
        with open(outfile_path, 'rb') as outfile:
            JTemplate(outfile.read()) # ignore result
    except Exception:
        click.echo("File %s failed to parse" % outfile_path)
