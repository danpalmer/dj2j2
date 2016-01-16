#!/usr/bin/env python
import click

from jinja2 import Template as JTemplate
from django.template import Template as DTemplate

from .django_settings import configure_django

@click.command()
@click.option('--indir', help="Input directory")
@click.option('--outdir', help="Output directory")
@click.option('--infile', help="Input file")
@click.option('--outfile', help="Output file")
def run(indir, outdir, infile, outfile):
    """
    A utility to transpile Django templates to Jinja2 templates.
    """

    if infile and outfile:
        transpile(infile, outfile)
        validate(outfile)

    elif indir and outdir:
        pass

    else:
        # Invalid argument set
        pass

def transpile(infile_path, outfile_path):
    with open(infile_path, 'rb') as infile:
        with open(outfile_path, 'wb') as outfile:
            outfile.write(transpile_content(infile.read()))

def transpile_content(incontent):
    configure_django()
    template = DTemplate(incontent)
    return incontent

def validate(outfile_path):
    try:
        with open(outfile_path, 'rb') as outfile:
            JTemplate(outfile.read()) # ignore result
    except Exception:
        click.echo("File %s failed to parse" % outfile_path)
