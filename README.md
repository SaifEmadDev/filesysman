# filesysman

A lightweight Python library for creating, managing, searching, copying, moving, and organizing files and folders.

## Features

- Create and delete files and folders
- Read, write, and append file content
- Rename files and folders
- Copy and move files and folders
- Search for files by keyword
- Search recursively through subfolders
- Filter files by extension
- Organize files by extension
- Get information about files and folders
- Count files with optional recursive and extension filtering
- Rename or delete files by keyword
- Find folders
- Remove empty files
- Find and remove empty folders
- Work with multiple files at once
- Optional multithreading for supported bulk operations

## Installation

Install the latest version from PyPI:

    pip install filesysman

## Quick Start

### Working with Files

    from filesysman import File

    file = File("example.txt")

    file.create()
    file.write("Hello, World!")

    print(file.read())
    print(file.name)
    print(file.suffix)
    print(file.size)

### Working with Folders

    from filesysman import Folder

    folder = Folder("my_folder")

    folder.create()

    print(folder.exists())
    print(folder.name)
    print(folder.path)

### Working with Multiple Files

    from filesysman import create_files, get_files

    create_files(
        "file1.txt",
        "file2.txt",
        "file3.txt",
    )

    files = get_files()

    for file in files:
        print(file)

## Searching for Files

get_files() provides a single interface for retrieving files with optional keyword, recursive, and extension filtering.

### Get All Files

    from filesysman import get_files

    files = get_files()

    for file in files:
        print(file)

### Search by Keyword

    files = get_files(keyword="report")

    for file in files:
        print(file)

### Search Recursively

    files = get_files(recursive=True)

    for file in files:
        print(file)

### Search by Keyword Recursively

    files = get_files(
        keyword="report",
        recursive=True,
    )

    for file in files:
        print(file)

### Filter by Extension

The extension can be provided with or without the leading dot.

    files = get_files(extension=".py")

Or:

    files = get_files(extension="py")

### Combine Filters

    files = get_files(
        keyword="report",
        recursive=True,
        extension=".pdf",
    )

    for file in files:
        print(file)

## Counting Files

Use get_files_count() to count files in a folder.

    from filesysman import get_files_count

    count = get_files_count()

    print(count)

You can also count files recursively:

    count = get_files_count(
        recursive=True,
    )

    print(count)

Or filter the count by extension:

    count = get_files_count(
        recursive=True,
        extension=".py",
    )

    print(count)

## Organizing Files by Extension

Files can be organized into folders based on their extensions:

    from filesysman import organize_by_extension

    organize_by_extension()

For example:

### Before

    folder/
    ├── photo.jpg
    ├── document.pdf
    ├── script.py
    └── notes.txt

### After

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
- get_files_count()
- get_folders()

### Organization and Cleanup

- organize_by_extension()
- rename_by_keyword()
- delete_by_keyword()
- clear_empty_files()
- clear_empty_folders()

## Multithreading

Several bulk file operations support optional multithreading through the max_workers parameter.

For example:

    from filesysman import create_files

    create_files(
        "file1.txt",
        "file2.txt",
        "file3.txt",
        max_workers=4,
    )

By default, max_workers=1 is used, which performs the operation sequentially.

## Requirements

- Python 3.8 or newer

## Version

Current version: **2.0.0**

## License

This project is licensed under the MIT License.
