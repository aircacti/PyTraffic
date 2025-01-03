class LibraryChecker:
    required_libraries = ['plyer', 'psutil', 'scapy']

    def __init__(self):
        self.missing_libraries = []

    def check_libraries(self):
        self.missing_libraries.clear()

        for lib in self.required_libraries:
            try:
                __import__(lib)
            except ImportError:
                self.missing_libraries.append(lib)

    def are_all_libraries_installed(self):
        self.check_libraries()
        return len(self.missing_libraries) == 0

    def get_missing_libraries(self):
        return self.missing_libraries
