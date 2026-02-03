# cloc-python

A Python CLI wrapper for [cloc](https://github.com/AlDanial/cloc) (Count Lines of Code) that can be executed via `uvx` without needing to install cloc on your system.

## Install

No installation required! Just run via `uvx`:

```bash
uvx cloc-python [options]
```

## Requirements

- **Windows**: No dependencies! The bundled `cloc.exe` is standalone.
- **Linux/macOS**: Perl is required (usually pre-installed)
  - Ubuntu/Debian: `sudo apt install perl`
  - CentOS/RHEL: `sudo yum install perl`
  - Arch Linux: `sudo pacman -S perl`
  - macOS: Usually pre-installed, or `brew install perl`
  - Docker: `docker run --rm -v $(pwd):/workdir miquella/cloc`

> **Note**: Most Linux distributions and macOS come with Perl pre-installed. You only need to install it if you're using a minimal container (like Alpine) or a custom system.

## Usage

This wrapper passes all arguments directly to the underlying cloc binary:

```bash
# Count lines in current directory
uvx cloc-python .

# Count lines in specific files
uvx cloc-python file1.py file2.py

# Exclude certain directories
uvx cloc-python --exclude-dir=vendor,node_modules .

# JSON output
uvx cloc-python --json .

# See all cloc options
uvx cloc-python --help
```

More options available on the [cloc's repository README](https://github.com/AlDanial/cloc/blob/master/README.md).


## cloc version

This package includes cloc v2.08.
