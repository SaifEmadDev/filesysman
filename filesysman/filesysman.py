"""Utilities for creating, deleting, renaming, searching, copying, moving,
organizing, and managing files and folders, with support for multithreaded
file operations.
"""

from datetime import datetime as _datetime
from pathlib import Path as _Path
import shutil as _shutil
from concurrent.futures import ThreadPoolExecutor as _ThreadPoolExecutor


class File:
    """Represents a single file and provides operations for managing it.

    The class supports creating, deleting, renaming, copying, moving, reading,
    writing, appending, and inspecting the represented file.
    """

    def __init__(self, file_path: str):
        """Initializes a File instance with the path of a file.

        Args:
            file_path: The path of the file to represent.

        Raises:
            IsADirectoryError: If the specified path is an existing directory.
        """
        self.__file_path = _Path(file_path)

        if self.__file_path.exists() and self.__file_path.is_dir():
            raise IsADirectoryError(
                f"Expected a file, but '{self.__file_path}' is a directory."
            )

    def __str__(self) -> str:
        """Returns the path of the represented file."""
        return str(self.__file_path)

    def create(
        self,
        folder_name: str = ".",
        exist_ok: bool = True,
    ) -> None:
        """Creates the represented file in the current directory or a folder.

        Args:
            folder_name: The name or path of the folder in which to create
                the file.
            exist_ok: Whether to allow the file to already exist.
        """
        folder = _Path(folder_name)
        folder.mkdir(parents=True, exist_ok=True)

        file = folder / self.__file_path
        file.touch(exist_ok=exist_ok)

        self.__file_path = file

    def delete(self, missing_ok: bool = False) -> None:
        """Deletes the represented file.

        Args:
            missing_ok: Whether to ignore the file if it does not exist.
        """
        self.__file_path.unlink(missing_ok=missing_ok)

    def rename(self, new_name: str) -> None:
        """Renames the represented file while keeping it in its current folder.

        Args:
            new_name: The new name of the file.
        """
        path = self.__file_path
        new_path = path.rename(path.parent / new_name)

        self.__file_path = new_path

    def copy(self, destination: str = ".") -> None:
        """Copies the represented file to a destination folder.

        The destination folder is created if it does not exist. The original
        file remains unchanged, and the File instance continues to represent
        the original file.

        Args:
            destination: The name or path of the destination folder.
        """
        _Path(destination).mkdir(parents=True, exist_ok=True)
        _shutil.copy2(self.__file_path, destination)

    def move(self, destination: str = ".") -> None:
        """Moves the represented file to a destination folder.

        The destination folder is created if it does not exist. The File
        instance is updated to represent the file at its new location.

        Args:
            destination: The name or path of the destination folder.
        """
        destination = _Path(destination)
        destination.mkdir(parents=True, exist_ok=True)

        _shutil.move(self.__file_path, destination)
        self.__file_path = destination / self.name

    def exists(self) -> bool:
        """Returns whether the represented file exists."""
        return self.__file_path.exists()

    def is_empty(self) -> bool:
        """Returns whether the represented file is empty."""
        return self.size == 0

    def read(self) -> str:
        """Returns the text content of the represented file."""
        return _Path.read_text(self.__file_path)

    def write(self, text: str) -> None:
        """Writes text to the represented file, replacing its existing
        content.
        """
        self.__file_path.write_text(text)

    def append(self, text: str) -> None:
        """Adds text to the end of the represented file."""
        with self.__file_path.open("a") as file:
            file.write(text)

    @property
    def path(self) -> _Path:
        """Returns the path of the represented file."""
        return self.__file_path

    @property
    def name(self) -> str:
        """Returns the name of the represented file."""
        return self.__file_path.name

    @property
    def stem(self) -> str:
        """Returns the stem of the represented file."""
        return self.__file_path.stem

    @property
    def suffix(self) -> str:
        """Returns the extension of the represented file."""
        return self.__file_path.suffix

    @property
    def size(self) -> int:
        """Returns the size of the represented file in bytes."""
        return self.__file_path.stat().st_size

    @property
    def parent(self) -> _Path:
        """Returns the path of the folder containing the file."""
        return self.__file_path.parent

    @property
    def absolute_path(self) -> _Path:
        """Returns the absolute path of the represented file."""
        return self.__file_path.absolute()

    @property
    def is_absolute(self) -> bool:
        """Returns whether the file's path is absolute."""
        return self.__file_path.is_absolute()

    @property
    def created_time(self) -> _datetime:
        """Returns the file's creation time as a datetime object."""
        return _datetime.fromtimestamp(self.__file_path.stat().st_ctime)

    @property
    def modified_time(self) -> _datetime:
        """Returns the file's last modification time as a datetime object."""
        return _datetime.fromtimestamp(self.__file_path.stat().st_mtime)

    @property
    def accessed_time(self) -> _datetime:
        """Returns the file's last access time as a datetime object."""
        return _datetime.fromtimestamp(self.__file_path.stat().st_atime)


class Folder:
    """Represents a single folder and provides operations for managing it.

    The class supports creating, deleting, renaming, copying, moving, clearing,
    and inspecting the represented folder.
    """

    def __init__(self, folder_path: str):
        """Initializes a Folder instance with the path of a folder.

        Args:
            folder_path: The path of the folder to represent.

        Raises:
            NotADirectoryError: If the specified path is an existing file.
        """
        self.__folder_path = _Path(folder_path)

        if self.__folder_path.exists() and self.__folder_path.is_file():
            raise NotADirectoryError(
                f"Expected a directory, but '{self.__folder_path}' is a file."
            )

    def __str__(self) -> str:
        """Returns the path of the represented folder."""
        return str(self.__folder_path)

    def create(
        self,
        folder_name: str = ".",
        parents: bool = False,
        exist_ok: bool = False,
    ) -> None:
        """Creates the represented folder in the current directory or another
        folder.

        Args:
            folder_name: The name or path of the folder in which to create
                the folder.
            parents: Whether to create missing parent folders.
            exist_ok: Whether to allow the folder to already exist.
        """
        folder = _Path(folder_name) / self.__folder_path
        folder.mkdir(parents=parents, exist_ok=exist_ok)

        self.__folder_path = folder

    def delete(self, filled_ok: bool = False) -> None:
        """Deletes the represented folder.

        Args:
            filled_ok: Whether to delete the folder and all of its contents
                if it is not empty.
        """
        if filled_ok:
            _shutil.rmtree(self.__folder_path)
        else:
            self.__folder_path.rmdir()

    def rename(self, new_name: str) -> None:
        """Renames the represented folder while keeping it in its current
        parent folder.

        Args:
            new_name: The new name of the folder.
        """
        folder = self.__folder_path
        new_folder = folder.rename(folder.parent / new_name)

        self.__folder_path = new_folder

    def copy(self, destination: str = ".") -> None:
        """Copies the represented folder to a destination folder.

        The original folder remains unchanged, and the Folder instance
        continues to represent the original folder. If the destination folder
        already exists, its contents are preserved and the copied contents are
        added to it.

        Args:
            destination: The name or path of the destination folder.
        """
        _shutil.copytree(
            self.__folder_path,
            destination,
            dirs_exist_ok=True,
        )

    def move(self, destination: str = ".") -> None:
        """Moves the represented folder to a destination folder.

        The destination folder is created if it does not exist. The represented
        folder is moved inside the destination folder, and the Folder instance
        is updated to represent the folder at its new location.

        Args:
            destination: The name or path of the destination folder.
        """
        destination = _Path(destination)
        destination.mkdir(parents=True, exist_ok=True)

        _shutil.move(self.__folder_path, destination)
        self.__folder_path = destination / self.name

    def clear(self) -> None:
        """Deletes all contents of the represented folder without deleting
        the folder itself.
        """
        for item in self.__folder_path.iterdir():
            if item.is_file():
                item.unlink()
            else:
                _shutil.rmtree(item)

    def exists(self) -> bool:
        """Returns whether the represented folder exists."""
        return self.__folder_path.exists()

    def is_empty(self) -> bool:
        """Returns whether the represented folder is empty."""
        return not any(self.__folder_path.iterdir())

    @property
    def path(self) -> _Path:
        """Returns the path of the represented folder."""
        return self.__folder_path

    @property
    def name(self) -> str:
        """Returns the name of the represented folder."""
        return self.__folder_path.name

    @property
    def parent(self) -> _Path:
        """Returns the path of the folder containing the folder."""
        return self.__folder_path.parent

    @property
    def absolute_path(self) -> _Path:
        """Returns the absolute path of the represented folder."""
        return self.__folder_path.absolute()

    @property
    def created_time(self) -> _datetime:
        """Returns the folder's creation time as a datetime object."""
        return _datetime.fromtimestamp(self.__folder_path.stat().st_ctime)

    @property
    def modified_time(self) -> _datetime:
        """Returns the folder's last modification time as a datetime object."""
        return _datetime.fromtimestamp(self.__folder_path.stat().st_mtime)

    @property
    def accessed_time(self) -> _datetime:
        """Returns the folder's last access time as a datetime object."""
        return _datetime.fromtimestamp(self.__folder_path.stat().st_atime)

    @property
    def current_size(self) -> int:
        """Returns the total size in bytes of files directly inside the
        folder.
        """
        size = 0

        for item in self.__folder_path.iterdir():
            if item.is_file():
                size += item.stat().st_size

        return size

    @property
    def total_size(self) -> int:
        """Returns the total size in bytes of all files in the folder and
        its subfolders.
        """
        size = 0

        for item in self.__folder_path.rglob("*"):
            if item.is_file():
                size += item.stat().st_size

        return size

    @property
    def is_absolute(self) -> bool:
        """Returns whether the folder's path is absolute."""
        return self.__folder_path.is_absolute()


def create_files(
    number: int,
    file_name: str = "File",
    sep: str = " ",
    extension: str = ".txt",
    folder_name: str = ".",
    max_workers: int = 1,
) -> None:
    """Creates multiple numbered files in the current directory or a folder.

    The files are named using the specified base name, separator, number,
    and extension. The extension is normalized to lowercase. Multiple files
    can be created concurrently by increasing the number of worker threads.

    Args:
        number: The number of files to create.
        file_name: The base name to use for the files.
        sep: The separator placed between the file name and number.
        extension: The file extension.
        folder_name: The name or path of the folder in which to create
            the files.
        max_workers: The maximum number of worker threads used to create
            files.

    Raises:
        ValueError: If number or max_workers is less than 1.
    """
    if max_workers < 1:
        raise ValueError("max_workers must be at least 1")

    if number <= 0:
        raise ValueError("The number must be positive!")

    extension = (
        extension.lower()
        if extension.startswith(".")
        else f".{extension.lower()}"
    )

    folder = _Path(folder_name)
    folder.mkdir(parents=True, exist_ok=True)

    if max_workers == 1:
        for number in range(1, number + 1):
            (folder / f"{file_name}{sep}{number}{extension}").touch()
    else:
        with _ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []

            for number in range(1, number + 1):
                future = executor.submit(
                    (folder / f"{file_name}{sep}{number}{extension}").touch
                )
                futures.append(future)

            for future in futures:
                future.result()


def delete_files(
    number: int,
    file_name: str,
    sep: str = " ",
    extension: str = ".txt",
    folder_name: str = ".",
    max_workers: int = 1,
) -> None:
    """Deletes multiple numbered files from the specified folder.

    The files are identified using the specified base name, separator, number,
    and extension. The extension is normalized to lowercase. Multiple files
    can be deleted concurrently by increasing the number of worker threads.

    Args:
        number: The number of files to delete.
        file_name: The base name of the files.
        sep: The separator placed between the file name and number.
        extension: The file extension.
        folder_name: The name or path of the folder containing the files.
        max_workers: The maximum number of worker threads used to delete files.

    Raises:
        ValueError: If number or max_workers is less than 1.
    """
    if max_workers < 1:
        raise ValueError("max_workers must be at least 1")

    if number <= 0:
        raise ValueError("The number must be positive!")

    extension = (
        extension.lower()
        if extension.startswith(".")
        else f".{extension.lower()}"
    )

    folder = _Path(folder_name)

    if max_workers == 1:
        for number in range(1, number + 1):
            path = folder / f"{file_name}{sep}{number}{extension}"
            path.unlink(missing_ok=True)
    else:
        with _ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []

            for number in range(1, number + 1):
                path = folder / f"{file_name}{sep}{number}{extension}"

                future = executor.submit(
                    path.unlink,
                    missing_ok=True,
                )
                futures.append(future)

            for future in futures:
                future.result()


def rename_files(
    number: int,
    old_name: str,
    new_name: str,
    old_sep: str = " ",
    new_sep: str = " ",
    extension: str = ".txt",
    folder_name: str = ".",
    max_workers: int = 1,
) -> None:
    """Renames multiple numbered files while preserving their numbering.

    The base name and separator can be changed while the extension is
    normalized to lowercase. Multiple files can be renamed concurrently
    by increasing the number of worker threads.

    Args:
        number: The number of files to rename.
        old_name: The current base name of the files.
        new_name: The new base name of the files.
        old_sep: The separator currently used between the file name and number.
        new_sep: The separator to use between the new file name and number.
        extension: The file extension of the files.
        folder_name: The name or path of the folder containing the files.
        max_workers: The maximum number of worker threads used to rename
            files.

    Raises:
        ValueError: If number or max_workers is less than 1, or if an old path
            is equal to its new path.
        FileExistsError: If a destination file already exists.
    """
    if max_workers < 1:
        raise ValueError("max_workers must be at least 1")

    if number <= 0:
        raise ValueError("The number must be positive!")

    extension = (
        extension.lower()
        if extension.startswith(".")
        else f".{extension.lower()}"
    )

    folder = _Path(folder_name)
    rename_tasks = []

    for number in range(1, number + 1):
        path = folder / f"{old_name}{old_sep}{number}{extension}"

        if path.exists():
            new_path = folder / f"{new_name}{new_sep}{number}{extension}"
            rename_tasks.append((path, new_path))

    for old_path, new_path in rename_tasks:
        if old_path == new_path:
            raise ValueError("The old path is equal to the new path")

        if new_path.exists():
            raise FileExistsError("File already exists!")

    if max_workers == 1:
        for old_path, new_path in rename_tasks:
            old_path.rename(new_path)
    else:
        with _ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []

            for old_path, new_path in rename_tasks:
                future = executor.submit(
                    old_path.rename,
                    new_path,
                )
                futures.append(future)

            for future in futures:
                future.result()


def get_files(
    folder_name: str = ".",
    keyword: str | None = None,
    recursive: bool = False,
    extension: str | None = None,
) -> list[_Path]:
    """Returns files matching the specified search criteria.

    Files can be filtered by keyword and file extension. When recursive is
    True, files inside subfolders are also included in the results. The
    keyword must not be empty.

    Args:
        folder_name: The name or path of the folder to search.
        keyword: The keyword to search for in file names. If None, no keyword
            filtering is applied.
        recursive: Whether to search inside subfolders.
        extension: The file extension used to filter the results. If None, no
            extension filtering is applied.

    Returns:
        A list containing the paths of the matching files.

    Raises:
        ValueError: If keyword is an empty string.
    """
    if keyword == "":
        raise ValueError("The keyword must not be empty!")

    if keyword:
        keyword = keyword.lower()

    if extension:
        extension = (
            extension.lower()
            if extension.startswith(".")
            else f".{extension.lower()}"
        )

    files = []
    folder = _Path(folder_name)

    if extension:
        items = (
            folder.rglob(f"*{extension}")
            if recursive
            else folder.glob(f"*{extension}")
        )
    else:
        items = folder.rglob("*") if recursive else folder.iterdir()

    for item in items:
        if item.is_file():
            if keyword:
                if keyword in item.stem.lower():
                    files.append(item)
            else:
                files.append(item)

    return files


def rename_by_keyword(
    keyword: str,
    new_name: str,
    sep: str = " ",
    extension: str | None = None,
    folder_name: str = ".",
    max_workers: int = 1,
) -> None:
    """Renames files whose names contain a specified keyword using sequential
    names.

    Original file extensions are preserved, and files can optionally be
    filtered by extension. Multiple files can be renamed concurrently by
    increasing the number of worker threads. The keyword must not be empty.

    Args:
        keyword: The keyword to search for in file names.
        new_name: The base name to assign to matching files.
        sep: The separator placed between the new file name and number.
        extension: The file extension used to filter matching files.
        folder_name: The name or path of the folder to search.
        max_workers: The maximum number of worker threads used to rename
            files.

    Raises:
        ValueError: If keyword is empty, max_workers is less than 1, or an
            old path is equal to its new path.
        FileExistsError: If a destination file already exists.
    """
    if max_workers < 1:
        raise ValueError("max_workers must be at least 1")

    if not keyword:
        raise ValueError("The keyword must not be empty!")

    keyword = keyword.lower()

    if extension:
        extension = (
            extension.lower()
            if extension.startswith(".")
            else f".{extension.lower()}"
        )

    num = 1
    folder = _Path(folder_name)
    rename_tasks = []

    for item in folder.iterdir():
        if item.is_file():
            name = item.stem.lower()
            exten = item.suffix.lower()

            if extension:
                if keyword in name and extension == exten:
                    new_path = folder / f"{new_name}{sep}{num}{exten}"
                    rename_tasks.append((item, new_path))
                    num += 1
            else:
                if keyword in name:
                    new_path = folder / f"{new_name}{sep}{num}{exten}"
                    rename_tasks.append((item, new_path))
                    num += 1

    for old_path, new_path in rename_tasks:
        if old_path == new_path:
            raise ValueError("The old path is equal to the new path")

        if new_path.exists():
            raise FileExistsError("File already exists!")

    if max_workers == 1:
        for old_path, new_path in rename_tasks:
            old_path.rename(new_path)
    else:
        with _ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []

            for old_path, new_path in rename_tasks:
                future = executor.submit(
                    old_path.rename,
                    new_path,
                )
                futures.append(future)

            for future in futures:
                future.result()


def delete_by_keyword(
    keyword: str,
    extension: str | None = None,
    folder_name: str = ".",
    max_workers: int = 1,
) -> None:
    """Deletes files whose names contain a specified keyword.

    Files can optionally be filtered by file extension. The keyword must not
    be empty. Multiple files can be deleted concurrently by increasing the
    number of worker threads.

    Args:
        keyword: The keyword to search for in file names.
        extension: The file extension used to filter the files. If None, no
            extension filtering is applied.
        folder_name: The name or path of the folder to search.
        max_workers: The maximum number of worker threads used to delete files.

    Raises:
        ValueError: If keyword is empty or max_workers is less than 1.
    """
    if max_workers < 1:
        raise ValueError("max_workers must be at least 1")

    if not keyword:
        raise ValueError("The keyword must not be empty!")

    keyword = keyword.lower()

    if extension:
        extension = (
            extension.lower()
            if extension.startswith(".")
            else f".{extension.lower()}"
        )

    folder = _Path(folder_name)
    files = []

    for item in folder.iterdir():
        if item.is_file():
            name = item.stem.lower()

            if extension:
                exten = item.suffix.lower()

                if keyword in name and extension == exten:
                    files.append(item)
            else:
                if keyword in name:
                    files.append(item)

    if max_workers == 1:
        for item in files:
            item.unlink()
    else:
        with _ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []

            for item in files:
                future = executor.submit(item.unlink)
                futures.append(future)

            for future in futures:
                future.result()


def get_files_count(
    folder_name: str = ".",
    recursive: bool = False,
    extension: str | None = None,
) -> int:
    """Returns the number of files in the specified folder.

    Files can optionally be counted recursively inside subfolders and
    filtered by file extension.

    Args:
        folder_name: The name or path of the folder to search.
        recursive: Whether to search inside subfolders.
        extension: The file extension used to filter the results. If None,
            no extension filtering is applied.

    Returns:
        The number of matching files.
    """
    if extension:
        extension = (
            extension.lower()
            if extension.startswith(".")
            else f".{extension.lower()}"
        )

    files_count = 0
    folder = _Path(folder_name)

    if recursive:
        pattern = f"*{extension}" if extension else "*"

        for item in folder.rglob(pattern):
            if item.is_file():
                files_count += 1
    else:
        for item in folder.iterdir():
            if item.is_file():
                if extension:
                    exten = item.suffix.lower()

                    if extension == exten:
                        files_count += 1
                else:
                    files_count += 1

    return files_count


def copy_files(
    source_folder: str = ".",
    destination_folder: str = ".",
    extension: str | None = None,
    max_workers: int = 1,
) -> None:
    """Copies files from a source folder to a destination folder.

    Existing files in the destination folder are overwritten. Files can
    optionally be filtered by file extension. Multiple files can be copied
    concurrently by increasing the number of worker threads.

    Args:
        source_folder: The name or path of the folder containing the files
            to copy.
        destination_folder: The name or path of the folder to copy the files
            to.
        extension: The file extension used to filter the files to copy.
        max_workers: The maximum number of worker threads used to copy files.

    Raises:
        FileExistsError: If the source and destination folders are the same.
        ValueError: If max_workers is less than 1.
    """
    if max_workers < 1:
        raise ValueError("max_workers must be at least 1")

    if source_folder == destination_folder:
        raise FileExistsError(
            f"'{source_folder}' Folder is the same as "
            f"'{destination_folder}' Folder"
        )

    if extension:
        extension = (
            extension.lower()
            if extension.startswith(".")
            else f".{extension.lower()}"
        )

    source = _Path(source_folder)
    destination = _Path(destination_folder)
    destination.mkdir(parents=True, exist_ok=True)

    files = []

    for item in source.iterdir():
        if item.is_file():
            if extension:
                exten = item.suffix.lower()

                if extension == exten:
                    files.append(item)
            else:
                files.append(item)

    if max_workers == 1:
        for item in files:
            _shutil.copy2(item, destination)
    else:
        with _ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []

            for item in files:
                future = executor.submit(
                    _shutil.copy2,
                    item,
                    destination,
                )
                futures.append(future)

            for future in futures:
                future.result()


def move_files(
    source_folder: str = ".",
    destination_folder: str = ".",
    extension: str | None = None,
    max_workers: int = 1,
) -> None:
    """Moves files from a source folder to a destination folder.

    Files can optionally be filtered by file extension. Multiple files can
    be moved concurrently by increasing the number of worker threads.

    Args:
        source_folder: The name or path of the folder containing the files
            to move.
        destination_folder: The name or path of the folder to move the files
            to.
        extension: The file extension used to filter the files to move.
        max_workers: The maximum number of worker threads used to move files.

    Raises:
        FileExistsError: If the source and destination folders are the same.
        ValueError: If max_workers is less than 1.
        shutil.Error: If a file cannot be moved to the destination folder.
    """
    if max_workers < 1:
        raise ValueError("max_workers must be at least 1")

    if source_folder == destination_folder:
        raise FileExistsError(
            f"'{source_folder}' Folder is the same as "
            f"'{destination_folder}' Folder"
        )

    if extension:
        extension = (
            extension.lower()
            if extension.startswith(".")
            else f".{extension.lower()}"
        )

    source = _Path(source_folder)
    destination = _Path(destination_folder)
    destination.mkdir(parents=True, exist_ok=True)

    files = []

    for item in source.iterdir():
        if item.is_file():
            if extension:
                exten = item.suffix.lower()

                if extension == exten:
                    files.append(item)
            else:
                files.append(item)

    if max_workers == 1:
        for item in files:
            _shutil.move(item, destination)
    else:
        with _ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []

            for item in files:
                future = executor.submit(
                    _shutil.move,
                    item,
                    destination,
                )
                futures.append(future)

            for future in futures:
                future.result()


def organize_by_extension(
    folder_name: str = ".",
    destination_folder: str | None = None,
    no_extension_folder: str = "No Extension",
    max_workers: int = 1,
) -> None:
    """Organizes files into folders based on their file extensions.

    Files with the same extension are moved into the same folder. If a
    destination folder is specified, copies of the files are organized there
    while the original files remain unchanged. Files without an extension
    are placed in a folder with the specified name.

    Args:
        folder_name: The name or path of the folder containing the files
            to organize.
        destination_folder: The name or path of the folder in which to
            organize copies of the files. If None, the files are organized
            in the original folder.
        no_extension_folder: The name of the folder in which to place files
            without an extension.
        max_workers: The maximum number of worker threads used to organize
            files.

    Raises:
        FileExistsError: If the source and destination folders are the same.
        ValueError: If max_workers is less than 1.
    """
    if max_workers < 1:
        raise ValueError("max_workers must be at least 1")

    if folder_name == destination_folder:
        raise FileExistsError(
            f"'{folder_name}' Folder is the same as "
            f"'{destination_folder}' Folder"
        )

    folder = _Path(folder_name)
    tasks = []

    if destination_folder:
        destination = _Path(destination_folder)
        destination.mkdir(parents=True, exist_ok=True)

    for item in folder.iterdir():
        if item.is_file():
            exten = item.suffix

            if exten:
                if destination_folder:
                    exten_folder = destination / exten.lstrip(".").upper()
                    exten_folder.mkdir(exist_ok=True)

                    tasks.append(
                        (_shutil.copy2, item, exten_folder)
                    )
                else:
                    exten_folder = folder / exten.lstrip(".").upper()
                    exten_folder.mkdir(exist_ok=True)

                    tasks.append(
                        (_shutil.move, item, exten_folder)
                    )

            else:
                if destination_folder:
                    no_exten = destination / no_extension_folder
                    no_exten.mkdir(exist_ok=True)

                    tasks.append(
                        (_shutil.copy2, item, no_exten)
                    )
                else:
                    no_exten = folder / no_extension_folder
                    no_exten.mkdir(exist_ok=True)

                    tasks.append(
                        (_shutil.move, item, no_exten)
                    )
    if max_workers == 1:
        for task in tasks:
            function, source, destination = task
            function(source, destination)
    else:
        with _ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []

            for task in tasks:
                future = executor.submit(*task)
                futures.append(future)

            for future in futures:
                future.result()


def get_folders(
    folder_name: str = ".",
    recursive: bool = False,
) -> list[_Path]:
    """Returns folders from the specified folder, optionally including
    subfolders.

    Args:
        folder_name: The name or path of the folder to search.
        recursive: Whether to include folders inside all subfolders.

    Returns:
        A list containing the paths of the matching folders.
    """
    folders = []
    folder = _Path(folder_name)

    if recursive:
        for item in folder.rglob("*"):
            if item.is_dir():
                folders.append(item)
    else:
        for item in folder.iterdir():
            if item.is_dir():
                folders.append(item)

    return folders


def clear_empty_files(
    folder_name: str = ".",
    recursive: bool = False,
    extension: str | None = None,
    max_workers: int = 1,
) -> None:
    """Deletes empty files from the specified folder.

    Files can optionally be filtered by file extension. When recursive is
    True, empty files inside subfolders are also deleted. Multiple files
    can be deleted concurrently by increasing the number of worker threads.

    Args:
        folder_name: The name or path of the folder to search.
        recursive: Whether to check files inside subfolders.
        extension: The file extension used to filter the files. If None, no
            extension filtering is applied.
        max_workers: The maximum number of worker threads used to delete
            files.

    Raises:
        ValueError: If max_workers is less than 1.
    """
    if max_workers < 1:
        raise ValueError("max_workers must be at least 1")

    if extension:
        extension = (
            extension.lower()
            if extension.startswith(".")
            else f".{extension.lower()}"
        )

    folder = _Path(folder_name)
    files = []

    if recursive:
        pattern = f"*{extension}" if extension else "*"

        for item in folder.rglob(pattern):
            if item.is_file() and item.stat().st_size == 0:
                files.append(item)
    else:
        for item in folder.iterdir():
            if item.is_file() and item.stat().st_size == 0:
                if extension:
                    exten = item.suffix.lower()

                    if extension == exten:
                        files.append(item)
                else:
                    files.append(item)

    if max_workers == 1:
        for item in files:
            item.unlink()
    else:
        with _ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []

            for item in files:
                future = executor.submit(item.unlink)
                futures.append(future)

            for future in futures:
                future.result()


def clear_empty_folders(
    folder_name: str = ".",
    recursive: bool = False,
    from_deep: bool = True,
) -> None:
    """Deletes empty folders from the specified folder.

    When recursive is True, empty folders inside subfolders are also
    deleted. If from_deep is True, folders are processed from the
    deepest level upward, allowing parent folders to be deleted after
    their empty subfolders are removed.

    Args:
        folder_name: The name or path of the folder to search.
        recursive: Whether to check folders inside subfolders.
        from_deep: Whether to process recursive folders from the
            deepest level upward.
    """
    folder = _Path(folder_name)

    if recursive:
        folders = [
            item
            for item in folder.rglob("*")
            if item.is_dir()
        ]

        if from_deep:
            folders.sort(
                key=lambda item: len(item.parts),
                reverse=True,
            )

        for item in folders:
            if not any(item.iterdir()):
                item.rmdir()
    else:
        for item in folder.iterdir():
            if item.is_dir() and not any(item.iterdir()):
                item.rmdir()