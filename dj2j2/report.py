import textwrap
from collections import namedtuple, defaultdict

from .jinja_env import jinja_environment


Position = namedtuple('Position', ('lineno', 'filename'))


class Report(object):
    def __init__(self):
        # These reports are 'detail' -> position
        self.required_libraries = defaultdict(list)
        self.required_extensions = defaultdict(list)
        self.required_globals = defaultdict(list)
        self.required_tags = defaultdict(list)
        self.required_filters = defaultdict(list)

        # Keep track of missing things we would need to mock out in a
        # successful transpilation run
        self.missing_custom_tags = set()
        self.missing_custom_filters = set()
        self.missing_custom_libraries = set()

        # Django/Jinja2 are slightly different for includes.
        self.invalid_includes = []

        # General reporting
        self.failed_files = {}
        self.num_files = 0

        self.requires_django_compat = False

        # State
        self.current_file = None

    def __str__(self):
        template = textwrap.dedent("""
            Finished processing, {{ report.num_files }} files.

            {% if report.failed_files %}Some files failed to transpile:{% endif %}
            {% for file, exc in report.failed_files.items() -%}
                - {{ file }}
                  {{ exc }}
            {% endfor %}
            {% if report.missing_custom_libraries or report.missing_custom_filters or report.missing_custom_tags -%}
            In addition, to transpile you need to declare some custom filters/tags/libraries.
            These can be added with --tags=tag1,tag2, or the same for filters or libraries.
            You will need to ensure that all of these appear in your Jinja environment.

            Tags: {% for tag in report.missing_custom_tags -%}
                {{ tag }}{% if not loop.last %},{% endif %}
            {%- endfor %}
            Filters: {% for filter in report.missing_custom_filters -%}
                {{ filter }}{% if not loop.last %},{% endif %}
            {%- endfor %}
            Libraries: {% for library in report.missing_custom_libraries -%}
                {{ library }}{% if not loop.last %},{% endif %}
            {%- endfor %}
            {% endif %}
        """).strip()

        return jinja_environment.from_string(template).render({'report': self})

    def set_current_file(self, current_file):
        self.num_files += 1
        self.current_file = current_file

    def add_required_library(self, library, token):
        position = Position(token.lineno, self.current_file)
        self.required_libraries[library].append(position)

    def add_required_extension(self, extension, token):
        position = Position(token.lineno, self.current_file)
        self.required_extensions[extension].append(position)

    def add_required_global(self, global_, token):
        position = Position(token.lineno, self.current_file)
        self.required_globals[global_].append(position)

    def add_invalid_include(self, lineno):
        self.invalid_includes.append(Position(lineno, self.current_file))

    def add_failed_file(self, filename, exc):
        self.failed_files[filename] = exc

    def add_required_tag(self, tag_name, token):
        position = Position(token.lineno, self.current_file)
        self.required_tags[position].append(tag_name)

    def add_required_filter(self, filter_name, token):
        position = Position(token.lineno, self.current_file)
        self.required_filters[position].append(filter_name)

    def add_missing_tag(self, tag_name):
        self.missing_custom_tags.add(tag_name)

    def add_missing_filter(self, filter_name):
        self.missing_custom_filters.add(filter_name)

    def add_missing_library(self, library):
        self.missing_custom_libraries.add(library)

    def set_requires_django_compat(self):
        self.requires_django_compat = True
