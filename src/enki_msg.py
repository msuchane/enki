from junit_xml import TestSuite, TestCase
import junit_xml_output


class Report():
    """Create and print report. thank u J."""

    def __init__(self):
        """Create placeholder for problem description."""
        self.report = {}
        self.count = 0

    def create_report(self, category, file_path):
        """Generate report."""
        self.count += 1
        if not category in self.report:
            self.report[category] = []
        self.report[category].append(file_path)

    def print_report(self, output=None):
        """Print report."""

        if output == 'oneline':
            for category, files in self.report.items():
                for file in files:
                    print("{}: ERROR: {} found.".format(file, category))
            return

        if output == 'gitlab':

            test_cases = []

            for category, files in self.report.items():
                for file in files:
                    test_case = TestCase(category, 'ValidationChecks', '', '', '', '', 'timestamp', 'status', 'class', file, 'line', 'log', 'url')
                    test_case.add_failure_info(f'{category} found.', '', 'ERROR')
                test_cases.append(test_case)

            ts = [TestSuite("ValidationErrors", test_cases)]
            print(TestSuite.to_xml_string(ts, prettyprint=True))

            return

        separator = "\n\t"

        for category, files in self.report.items():
            print("\nERROR: {} found in the following files:".format(category))
            print('\t' + separator.join(files))
