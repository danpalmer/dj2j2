from collections import namedtuple, defaultdict


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
        self.missing_custom_tags = []
        self.missing_custom_filters = []
        self.missing_custom_libraries = []

        # Django/Jinja2 are slightly different for includes.
        self.invalid_includes = []

        # General reporting
        self.failed_files = {}
        self.num_files = 0

        self.requires_django_compat = False

        # State
        self.current_file = None

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
        self.missing_custom_tags.append(tag_name)

    def add_missing_filter(self, filter_name):
        self.missing_custom_filters.append(filter_name)

    def add_missing_library(self, library):
        self.missing_custom_libraries.append(library)

    def set_requires_django_compat(self):
        self.requires_django_compat = True
