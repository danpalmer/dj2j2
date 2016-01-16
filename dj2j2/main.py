#!/usr/bin/env python
import click

from jinja2 import Template as JTemplate
from django.template import Template as DTemplate

from .report import Report
from .transpile import transpile_template
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

    report = Report()

    if infile and outfile:
        transpile(report, infile, outfile)
        validate(outfile)

    elif indir and outdir:
        pass

    else:
        # Invalid argument set
        pass

def transpile(report, infile_path, outfile_path):
    with open(infile_path, 'rb') as infile:
        with open(outfile_path, 'wb') as outfile:
            outfile.write(transpile_content(report, infile.read()))

def transpile_content(report, incontent):
    configure_django()
    template = DTemplate(incontent)
    output = transpile_template(report, template)
    return ''.join(output)

def validate(outfile_path):
    try:
        with open(outfile_path, 'rb') as outfile:
            JTemplate(outfile.read()) # ignore result
    except Exception:
        click.echo("File %s failed to parse" % outfile_path)
