class Position(object):
    def __init__(self, lineno, filename):
        self.lineno = lineno
        self.filename = filename

class Report(object):
    def __init__(self):
        self.required_libraries = {}
        self.required_extensions = []
        self.required_globals = []
        self.failed_files = {}
        self.current_file = None
        self.num_files = 0

    def set_current_file(self, current_file):
        self.num_files += 1
        self.current_file = current_file

    def add_required_library(self, library, lineno):
        position = Position(lineno, self.current_file)
        self.required_libraries[position] = library

    def add_required_extension(self, extension):
        self.required_extensions.append(extension)

    def add_required_global(self, global_):
        self.required_globals.append(global_)

    def add_failed_file(self, filename, exc):
        self.failed_files[filename] = exc
