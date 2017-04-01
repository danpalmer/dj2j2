#!/usr/bin/env python
import os
import click

from django.template import Template as DTemplate, TemplateSyntaxError
from django.template.base import FILTER_SEPARATOR, FILTER_ARGUMENT_SEPARATOR

from .utils import ensure_dir_exists, get_all_standard_template_filters
from .report import Report
from .transpile import transpile_template
from .jinja_env import jinja_environment
from .exceptions import StopTranspilation
from .django_settings import configure_django


@click.command()
@click.option(
    '--indir',
    type=click.Path(exists=True),
    help="Input directory",
)
@click.option(
    '--outdir',
    type=click.Path(exists=False),
    help="Output directory",
)
@click.option(
    '--infile',
    type=click.Path(exists=True),
    help="Input file",
)
@click.option(
    '--outfile',
    type=click.Path(exists=False),
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
            try:
                outfile.write(transpile_content(report, infile.read()))
            except StopTranspilation:
                return


def transpile_content(report, incontent):
    configure_django()

    incontent = preprocess_content(incontent)

    try:
        template = DTemplate(incontent)
    except TemplateSyntaxError as tse:

        if 'Did you forget to register or load this tag?' in str(tse):
            tag = tse.token.split_contents()[0]
            report.add_missing_tag(tag)
            raise StopTranspilation()

        if 'Invalid filter' in str(tse):
            filters = tse.token.contents.split(FILTER_SEPARATOR)[1:]
            filters = [f.split(FILTER_ARGUMENT_SEPARATOR)[0] for f in filters]
            custom = set(filters) - set(get_all_standard_template_filters())

            for filter_ in custom:
                report.add_missing_filter(filter_)

            raise StopTranspilation()

        if 'is not a registered tag library' in str(tse):
            library = tse.token.split_contents()[1]
            report.add_missing_library(library)
            raise StopTranspilation()

        raise

    output = transpile_template(report, template)
    return ''.join(output)


def preprocess_content(content):
    """
    Handle things that we can't do easily by interpreting the output
    of the Django template engine, or by patching it.
    """
    return content.replace('{#', '{#{#').replace('#}', '#} #}')


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
            jinja_environment.from_string(outfile.read())
    except Exception as e:
        report.add_failed_file(outfile_path, e)
