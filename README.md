# files

A simple Python library for creating, managing, searching, copying, moving, and organizing files and folders.

## Features

- Create and delete files and folders
- Read, write, and append file content
- Rename files and folders
- Copy and move files and folders
- Search for files by keyword
- Search recursively through subfolders
- Find files by extension
- Organize files by extension
- Get information about files and folders
- Count files
- Find and remove empty folders
- Work with multiple files at once

## Installation

Install the package using pip:

    pip install files

## Quick Start

### Working with Files

    from files import File

    file = File("example.txt")

    file.create()
    file.write("Hello, World!")

    print(file.read())
    print(file.name)
    print(file.suffix)
    print(file.size)

### Working with Folders

    from files import Folder

    folder = Folder("my_folder")

    folder.create()

    print(folder.exists())
    print(folder.name)
    print(folder.path)

### Working with Multiple Files

    from files import create_files, get_files

    create_files(
        "file1.txt",
        "file2.txt",
        "file3.txt"
    )

    files = get_files()

    for file in files:
        print(file)

## Searching for Files

Search for files containing a specific keyword in their names:

    from files import find_files

    files = find_files("report")

    for file in files:
        print(file)

You can also search recursively through subfolders:

    from files import find_files_recursive

    files = find_files_recursive("report")

    for file in files:
        print(file)

## Organizing Files by Extension

Files can be organized into folders based on their extensions:

    from files import organize_by_extension

    organize_by_extension()

For example:

    Before:

    folder/
    ├── photo.jpg
    ├── document.pdf
    ├── script.py
    └── notes.txt

    After:

    folder/
    ├── JPG/
    │   └── photo.jpg
    ├── PDF/
    │   └── document.pdf
    ├── PY/
    │   └── script.py
    └── TXT/
        └── notes.txt

## Main API

### Classes

- File
- Folder

### File and Folder Operations

- create_files()
- delete_files()
- rename_files()
- copy_files()
- move_files()

### Searching and Retrieving

- get_files()
- find_files()
- get_files_count()
- get_files_recursive()
- find_files_recursive()
- get_folders()

### Organization and Cleanup

- organize_by_extension()
- rename_by_keyword()
- delete_by_keyword()
- clear_empty_folders()

## Requirements

- Python 3.8 or newer

## License

This project is licensed under the MIT License.