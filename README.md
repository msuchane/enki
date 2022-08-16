# enki

Command-line validation tool.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Levi-Leah/enki.git
    ```

1. Navigate to the root directory of the repository:
    ```bash
    cd enki
    ```

1. Run the installation script:
    ```bash
    sh install.sh
    ```

1. Source your `~/.baschrc` file:
    ```bash
    source ~/.bashrc
    ```

## Verification steps

* To verify that `enki` is installed, run:
    ```bash
    enki -h
    ```

## Usage

* To see the help message, run:
    ```bash
    enki -h
    ```

* To validate the files, run:
    ```bash
    enki validate <PATH>
    ```
    Replace `<PATH>` with the path to files or directories you want to validate.

    **Note**
    `enki` does not descend into symlinks.


## Examples

* To validate all files in the directory, run:
    ```bash
    enki validate path/
    ```

* To validate a specific file or files, run:
    ```bash
    enki validate path/to/file.adoc
    enki validate path/to/file.adoc path/to/another-file.adoc
    ```

* To validate all files that match a global pattern, run:
    ```bash
    enki validate path/to/**/**/*adoc
    ```

* To validate all files that match the special character, run:
    ```bash
    enki validate path/to/*adoc
    ```

## Error messages

`enki` has the following error levels:

- enki errors
- validation errors

### enki errors

enki error have the `ENKI ERROR:` prefix and occur when `enki` is unable to perform the validation.

For more information, see [enki errors](docs/enki-errors.md).

### Validation errors

Validation error have the `VALIDATION ERROR:` prefix and occur when the files you are validating did not pass the validation checks.

For more information, see [validation errors](docs/validation-errors.md).

## Reporting a bug
[Issue tracker](https://github.com/Levi-Leah/enki/issues)


## License
[MIT](https://choosealicense.com/licenses/mit/)
