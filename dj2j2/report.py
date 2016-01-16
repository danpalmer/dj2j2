class Position(object):
    def __init__(self, lineno, filename):
        self.lineno = lineno
        self.filename = filename

class Report(object):
    def __init__(self):
        self.required_libraries = {}
        self.current_file = None

    def set_current_file(self, current_file):
        self.current_file = current_file

    def add_required_library(self, library, lineno):
        position = Position(lineno, self.current_file)
        self.required_libraries[position] = library
