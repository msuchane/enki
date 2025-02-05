import os
import re
import sys

from enki_msg import Report
from enki_checks import checks, nesting_in_modules_check, too_many_comments_check
from enki_regex import Regexes


def sort_files(files: list[str]) -> tuple[list[str], list[str], list[str]]:
    """Get a list of assemblies, modules, and unidentified files."""
    prefix_assemblies = []
    prefix_modules = []
    undefined_content = []

    for file in files:

        file_name = os.path.basename(file)

        if file_name.startswith('assembly'):
            prefix_assemblies.append(file)
        elif file_name.startswith(("proc_", "con_", "ref_", "proc-", "con-", "ref-")):
            prefix_modules.append(file)
        else:
            undefined_content.append(file)

    return prefix_assemblies, prefix_modules, undefined_content


def validate(
        all_files: list[str],
        report: Report,
        undefined_content: list[str],
        prefix_assemblies: list[str],
        prefix_modules: list[str]) -> Report:
    """Run validation checks and return the report."""

    undetermined_file_type = []
    confused_files = []

    cwd = os.getcwd()

    for path in all_files:
        relative_path = os.path.relpath(path, cwd)

        with open(path, 'r') as file:
            original = file.read()
            stripped = Regexes.MULTI_LINE_COMMENT.sub('', original)
            stripped = Regexes.SINGLE_LINE_COMMENT.sub('', stripped)

            # this check should run before
            # code blocks
            # internal/single line conditionals
            # are replaced
            too_many_comments_check(original, stripped, report, relative_path)

            stripped = Regexes.CODE_BLOCK_DASHES.sub('', stripped)
            stripped = Regexes.CODE_BLOCK_DOTS.sub('', stripped)
            stripped = Regexes.CODE_BLOCK_TWO_DASHES.sub('', stripped)
            stripped = Regexes.INTERNAL_IFDEF.sub('', stripped)
            stripped = Regexes.SINGLE_LINE_CONDITIONAL.sub('', stripped)

            checks(report, stripped, original, relative_path)

            if path in undefined_content:
                if re.findall(Regexes.MODULE_TYPE, stripped):
                    nesting_in_modules_check(report, stripped, relative_path)
                elif re.findall(Regexes.SNIPPET_TYPE, stripped):
                    continue
                else:
                    undetermined_file_type.append(relative_path)

            if path in prefix_assemblies:
                if re.findall(Regexes.MODULE_TYPE, stripped):
                    confused_files.append(relative_path)
                    nesting_in_modules_check(report, stripped, relative_path)

            if path in prefix_modules:
                if re.findall(Regexes.ASSEMBLY_TYPE, stripped):
                    confused_files.append(path)
                else:
                    nesting_in_modules_check(report, stripped, relative_path)

    return report


def validating_files(files: list[str], start_time: float, output: str = None) -> None:
    """Print the result of validation and exit with an error."""
    report = Report()

    prefix_assemblies, prefix_modules, undefined_content = sort_files(files)
    file_validation = validate(
        files, report, undefined_content, prefix_assemblies, prefix_modules)

    if file_validation.count == 0:
        sys.exit(0)

    file_validation.print_report(start_time, output)
    sys.exit(2)
