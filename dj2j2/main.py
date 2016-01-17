#!/usr/bin/env python
import os
import click

from jinja2 import Template as JTemplate
from django.template import Template as DTemplate

from .utils import ensure_dir_exists
from .report import Report
from .transpile import transpile_template
from .django_settings import configure_django


@click.command()
@click.option(
    '--indir',
    type=click.Path(exists=True),
    help="Input directory",
)
@click.option(
    '--outdir',
    type=click.Path(exists=True),
    help="Output directory",
)
@click.option(
    '--infile',
    type=click.Path(exists=True),
    help="Input file",
)
@click.option(
    '--outfile',
    type=click.Path(exists=True),
    help="Output file",
)
@click.option(
    '--extension',
    help="Template file extension",
    default='html',
)
def run(indir, outdir, infile, outfile, extension):
    """
    A utility to transpile Django templates to Jinja2 templates.
    """

    report = Report()

    if infile and outfile:
        transpile_file(report, infile, outfile)
        validate_file(report, outfile)

    elif indir and outdir and extension:
        transpile_dir(report, indir, outdir, extension)
        validate_dir(report, outdir, extension)

    else:
        # Invalid argument set
        pass

    print(report)


def transpile_dir(report, indir, outdir, extension):
    indir = os.path.abspath(indir)
    outdir = os.path.abspath(outdir)

    for dirpath, _, filenames in os.walk(indir):
        for filename in filenames:
            if not filename.endswith('.%s' % extension):
                continue

            full_filename = os.path.join(dirpath, filename)
            output_local_path = full_filename.replace('%s/' % indir, '')
            output_filename = os.path.join(outdir, output_local_path)

            transpile_file(report, full_filename, output_filename)


def transpile_file(report, infile_path, outfile_path):
    ensure_dir_exists(os.path.dirname(outfile_path))

    with open(infile_path, 'r') as infile:
        with open(outfile_path, 'w') as outfile:
            report.set_current_file(infile_path)
            outfile.write(transpile_content(report, infile.read()))


def transpile_content(report, incontent):
    configure_django()
    template = DTemplate(incontent)
    output = transpile_template(report, template)
    return ''.join(output)


def validate_dir(report, outdir, extension):
    outdir = os.path.abspath(outdir)

    for dirpath, _, filenames in os.walk(outdir):
        for filename in filenames:
            if not filename.endswith('.%s' % extension):
                continue

            full_filename = os.path.join(dirpath, filename)
            validate_file(report, full_filename)


def validate_file(report, outfile_path):
    try:
        with open(outfile_path, 'r') as outfile:
            JTemplate(outfile.read()) # ignore result
    except Exception as e:
        report.add_failed_file(outfile_path, e)
