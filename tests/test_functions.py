import pytest
from filesysman import (
    create_files,
    delete_files,
    rename_files,
    get_files,
    get_files_count,
    rename_by_keyword,
    delete_by_keyword,
    copy_files,
    move_files,
    organize_by_extension,
    get_folders,
    clear_empty_files,
    clear_empty_folders,
)


def test_create_files(tmp_path):
    create_files(
        3,
        file_name="Test",
        folder_name=tmp_path,
    )

    assert (tmp_path / "Test 1.txt").exists()
    assert (tmp_path / "Test 2.txt").exists()
    assert (tmp_path / "Test 3.txt").exists()


def test_delete_files(tmp_path):
    create_files(
        3,
        file_name="Test",
        folder_name=tmp_path,
    )

    delete_files(
        3,
        file_name="Test",
        folder_name=tmp_path,
    )

    assert not (tmp_path / "Test 1.txt").exists()
    assert not (tmp_path / "Test 2.txt").exists()
    assert not (tmp_path / "Test 3.txt").exists()


def test_rename_files(tmp_path):
    create_files(
        3,
        file_name="Old",
        folder_name=tmp_path,
    )

    rename_files(
        3,
        old_name="Old",
        new_name="New",
        folder_name=tmp_path,
    )

    assert not (tmp_path / "Old 1.txt").exists()
    assert not (tmp_path / "Old 2.txt").exists()
    assert not (tmp_path / "Old 3.txt").exists()

    assert (tmp_path / "New 1.txt").exists()
    assert (tmp_path / "New 2.txt").exists()
    assert (tmp_path / "New 3.txt").exists()


def test_get_files(tmp_path):
    folder = tmp_path / "folder"
    folder.mkdir()

    file1 = folder / "file1.txt"
    file2 = folder / "file2.txt"
    subfolder = folder / "subfolder"

    file1.write_text("Hello")
    file2.write_text("World")
    subfolder.mkdir()

    result = get_files(folder)

    assert file1 in result
    assert file2 in result
    assert subfolder not in result


def test_get_files_recursive(tmp_path):
    folder = tmp_path / "folder"
    subfolder = folder / "subfolder"
    subfolder.mkdir(parents=True)

    file1 = folder / "file1.txt"
    file2 = subfolder / "file2.txt"

    file1.write_text("Hello")
    file2.write_text("World")

    result = get_files(folder, recursive=True)

    assert file1 in result
    assert file2 in result


def test_get_files_with_keyword(tmp_path):
    folder = tmp_path / "folder"
    folder.mkdir()

    matching_file = folder / "python_file.txt"
    other_file = folder / "hello.txt"

    matching_file.write_text("Python")
    other_file.write_text("Hello")

    result = get_files(folder, keyword="python")

    assert matching_file in result
    assert other_file not in result


def test_get_files_with_extension(tmp_path):
    folder = tmp_path / "folder"
    folder.mkdir()

    txt_file = folder / "file.txt"
    py_file = folder / "file.py"

    txt_file.write_text("Text")
    py_file.write_text("Python")

    result = get_files(folder, extension=".txt")

    assert txt_file in result
    assert py_file not in result


def test_get_files_with_keyword_and_extension(tmp_path):
    folder = tmp_path / "folder"
    folder.mkdir()

    matching_file = folder / "python_file.py"
    wrong_extension = folder / "python_file.txt"
    wrong_keyword = folder / "hello.py"

    matching_file.write_text("Python")
    wrong_extension.write_text("Text")
    wrong_keyword.write_text("Hello")

    result = get_files(
        folder,
        keyword="python",
        extension=".py",
    )

    assert matching_file in result
    assert wrong_extension not in result
    assert wrong_keyword not in result


def test_get_files_recursive_with_keyword_and_extension(tmp_path):
    folder = tmp_path / "folder"
    subfolder = folder / "subfolder"
    subfolder.mkdir(parents=True)

    matching_file = subfolder / "python_file.py"
    wrong_extension = subfolder / "python_file.txt"
    wrong_keyword = subfolder / "hello.py"

    matching_file.write_text("Python")
    wrong_extension.write_text("Text")
    wrong_keyword.write_text("Hello")

    result = get_files(
        folder,
        keyword="python",
        recursive=True,
        extension=".py",
    )

    assert matching_file in result
    assert wrong_extension not in result
    assert wrong_keyword not in result


def test_get_files_keyword_case_insensitive(tmp_path):
    folder = tmp_path / "folder"
    folder.mkdir()

    file1 = folder / "Python_File.txt"
    file2 = folder / "PYTHON_Code.txt"

    file1.write_text("Python")
    file2.write_text("Code")

    result = get_files(folder, keyword="PYTHON")

    assert file1 in result
    assert file2 in result


def test_get_files_extension_case_insensitive(tmp_path):
    folder = tmp_path / "folder"
    folder.mkdir()

    file1 = folder / "file.TXT"
    file2 = folder / "file.py"

    file1.write_text("Text")
    file2.write_text("Python")

    result = get_files(folder, extension="TXT")

    assert file1 in result
    assert file2 not in result


def test_get_files_empty_keyword(tmp_path):
    folder = tmp_path / "folder"
    folder.mkdir()

    with pytest.raises(ValueError):
        get_files(folder, keyword="")


def test_get_files_no_matches(tmp_path):
    folder = tmp_path / "folder"
    folder.mkdir()

    (folder / "hello.txt").write_text("Hello")

    result = get_files(folder, keyword="python")

    assert result == []


def test_get_files_count(tmp_path):
    (tmp_path / "file1.txt").write_text("Hello")
    (tmp_path / "file2.txt").write_text("World")
    (tmp_path / "file3.py").write_text("Python")
    (tmp_path / "folder").mkdir()

    assert get_files_count(tmp_path) == 3
    assert get_files_count(tmp_path, extension=".txt") == 2
    assert get_files_count(tmp_path, extension=".py") == 1


def test_rename_by_keyword(tmp_path):
    (tmp_path / "Python_notes.txt").write_text("Notes")
    (tmp_path / "Python_project.txt").write_text("Project")
    (tmp_path / "Java_notes.txt").write_text("Java")

    rename_by_keyword(
        "python",
        "PythonFile",
        folder_name=tmp_path,
    )

    assert not (tmp_path / "Python_notes.txt").exists()
    assert not (tmp_path / "Python_project.txt").exists()
    assert (tmp_path / "PythonFile 1.txt").exists()
    assert (tmp_path / "PythonFile 2.txt").exists()
    assert (tmp_path / "Java_notes.txt").exists()


def test_rename_by_keyword_with_extension(tmp_path):
    (tmp_path / "Python_notes.txt").write_text("Notes")
    (tmp_path / "Python_project.py").write_text("Project")
    (tmp_path / "Python_test.txt").write_text("Test")

    rename_by_keyword(
        "python",
        "File",
        extension=".txt",
        folder_name=tmp_path,
    )

    assert (tmp_path / "File 1.txt").exists()
    assert (tmp_path / "File 2.txt").exists()
    assert (tmp_path / "Python_project.py").exists()


def test_delete_by_keyword(tmp_path):
    (tmp_path / "Python_notes.txt").write_text("Notes")
    (tmp_path / "Python_project.py").write_text("Project")
    (tmp_path / "Java_notes.txt").write_text("Java")

    delete_by_keyword(
        "python",
        folder_name=tmp_path,
    )

    assert not (tmp_path / "Python_notes.txt").exists()
    assert not (tmp_path / "Python_project.py").exists()
    assert (tmp_path / "Java_notes.txt").exists()


def test_delete_by_keyword_with_extension(tmp_path):
    (tmp_path / "Python_notes.txt").write_text("Notes")
    (tmp_path / "Python_project.py").write_text("Project")
    (tmp_path / "Python_test.txt").write_text("Test")

    delete_by_keyword(
        "python",
        extension=".txt",
        folder_name=tmp_path,
    )

    assert not (tmp_path / "Python_notes.txt").exists()
    assert not (tmp_path / "Python_test.txt").exists()
    assert (tmp_path / "Python_project.py").exists()


def test_copy_files(tmp_path):
    source = tmp_path / "source"
    destination = tmp_path / "destination"

    source.mkdir()

    (source / "file1.txt").write_text("Hello")
    (source / "file2.txt").write_text("World")
    (source / "file3.py").write_text("Python")

    copy_files(source, destination)

    assert (source / "file1.txt").exists()
    assert (source / "file2.txt").exists()
    assert (source / "file3.py").exists()

    assert (destination / "file1.txt").exists()
    assert (destination / "file2.txt").exists()
    assert (destination / "file3.py").exists()


def test_copy_files_with_extension(tmp_path):
    source = tmp_path / "source"
    destination = tmp_path / "destination"

    source.mkdir()

    (source / "file1.txt").write_text("Hello")
    (source / "file2.py").write_text("Python")
    (source / "file3.txt").write_text("World")

    copy_files(source, destination, ".txt")

    assert (destination / "file1.txt").exists()
    assert (destination / "file3.txt").exists()
    assert not (destination / "file2.py").exists()


def test_move_files(tmp_path):
    source = tmp_path / "source"
    destination = tmp_path / "destination"

    source.mkdir()

    (source / "file1.txt").write_text("Hello")
    (source / "file2.txt").write_text("World")

    move_files(source, destination)

    assert not (source / "file1.txt").exists()
    assert not (source / "file2.txt").exists()
    assert (destination / "file1.txt").exists()
    assert (destination / "file2.txt").exists()


def test_move_files_with_extension(tmp_path):
    source = tmp_path / "source"
    destination = tmp_path / "destination"

    source.mkdir()

    (source / "file1.txt").write_text("Hello")
    (source / "file2.py").write_text("Python")
    (source / "file3.txt").write_text("World")

    move_files(source, destination, ".txt")

    assert not (source / "file1.txt").exists()
    assert not (source / "file3.txt").exists()
    assert (source / "file2.py").exists()

    assert (destination / "file1.txt").exists()
    assert (destination / "file3.txt").exists()
    assert not (destination / "file2.py").exists()


def test_organize_by_extension(tmp_path):
    (tmp_path / "file1.txt").write_text("Hello")
    (tmp_path / "file2.txt").write_text("World")
    (tmp_path / "script.py").write_text("Python")
    (tmp_path / "README").write_text("Read me")

    organize_by_extension(tmp_path)

    assert (tmp_path / "TXT" / "file1.txt").exists()
    assert (tmp_path / "TXT" / "file2.txt").exists()
    assert (tmp_path / "PY" / "script.py").exists()
    assert (tmp_path / "No Extension" / "README").exists()

    assert not (tmp_path / "file1.txt").exists()
    assert not (tmp_path / "file2.txt").exists()
    assert not (tmp_path / "script.py").exists()
    assert not (tmp_path / "README").exists()


def test_organize_by_extension_with_destination(tmp_path):
    source = tmp_path / "source"
    destination = tmp_path / "organized"

    source.mkdir()

    (source / "file1.txt").write_text("Hello")
    (source / "script.py").write_text("Python")
    (source / "README").write_text("Read me")

    organize_by_extension(source, destination)

    assert (source / "file1.txt").exists()
    assert (source / "script.py").exists()
    assert (source / "README").exists()

    assert (destination / "TXT" / "file1.txt").exists()
    assert (destination / "PY" / "script.py").exists()
    assert (destination / "No Extension" / "README").exists()


def test_get_folders(tmp_path):
    folder1 = tmp_path / "folder1"
    folder2 = tmp_path / "folder2"

    folder1.mkdir()
    folder2.mkdir()

    subfolder = folder1 / "subfolder"
    subfolder.mkdir()

    folders = get_folders(tmp_path)

    assert len(folders) == 2
    assert folder1 in folders
    assert folder2 in folders
    assert subfolder not in folders


def test_get_folders_recursive(tmp_path):
    folder1 = tmp_path / "folder1"
    folder2 = tmp_path / "folder2"

    folder1.mkdir()
    folder2.mkdir()

    subfolder = folder1 / "subfolder"
    subfolder.mkdir()

    nested_folder = subfolder / "nested"
    nested_folder.mkdir()

    folders = get_folders(tmp_path, recursive=True)

    assert len(folders) == 4
    assert folder1 in folders
    assert folder2 in folders
    assert subfolder in folders
    assert nested_folder in folders


def test_clear_empty_files(tmp_path):
    (tmp_path / "empty.txt").touch()
    (tmp_path / "empty.py").touch()
    (tmp_path / "filled.txt").write_text("Hello")

    subfolder = tmp_path / "subfolder"
    subfolder.mkdir()
    (subfolder / "nested_empty.txt").touch()
    (subfolder / "nested_filled.txt").write_text("Hello")

    clear_empty_files(tmp_path)

    assert not (tmp_path / "empty.txt").exists()
    assert not (tmp_path / "empty.py").exists()
    assert (tmp_path / "filled.txt").exists()

    assert (subfolder / "nested_empty.txt").exists()
    assert (subfolder / "nested_filled.txt").exists()

    clear_empty_files(tmp_path, recursive=True)

    assert not (subfolder / "nested_empty.txt").exists()
    assert (subfolder / "nested_filled.txt").exists()


def test_clear_empty_folders(tmp_path):
    empty1 = tmp_path / "empty1"
    empty2 = tmp_path / "empty2"
    non_empty = tmp_path / "non_empty"

    empty1.mkdir()
    empty2.mkdir()
    non_empty.mkdir()

    (non_empty / "file.txt").write_text("Hello")

    clear_empty_folders(tmp_path)

    assert not empty1.exists()
    assert not empty2.exists()
    assert non_empty.exists()
    assert (non_empty / "file.txt").exists()


def test_clear_empty_folders_recursive(tmp_path):
    empty1 = tmp_path / "empty1"
    empty1.mkdir()

    folder = tmp_path / "folder"
    folder.mkdir()

    empty2 = folder / "empty2"
    empty2.mkdir()

    non_empty = folder / "non_empty"
    non_empty.mkdir()

    (non_empty / "file.txt").write_text("Hello")

    clear_empty_folders(tmp_path, recursive=True)

    assert not empty1.exists()
    assert not empty2.exists()
    assert non_empty.exists()
    assert (non_empty / "file.txt").exists()


def test_clear_empty_folders_from_deep(tmp_path):
    root = tmp_path / "root"
    folder_a = root / "A"
    folder_b = folder_a / "B"
    folder_c = folder_b / "C"

    folder_c.mkdir(parents=True)

    clear_empty_folders(root, recursive=True, from_deep=True)

    assert not folder_a.exists()
    assert not folder_b.exists()
    assert not folder_c.exists()


def test_copy_files_with_multiple_workers(tmp_path):
    source = tmp_path / "source"
    destination = tmp_path / "destination"

    source.mkdir()

    (source / "file1.txt").write_text("Hello")
    (source / "file2.txt").write_text("World")
    (source / "file3.txt").write_text("Python")

    copy_files(source, destination, max_workers=3)

    assert (destination / "file1.txt").exists()
    assert (destination / "file2.txt").exists()
    assert (destination / "file3.txt").exists()

    assert (destination / "file1.txt").read_text() == "Hello"
    assert (destination / "file2.txt").read_text() == "World"
    assert (destination / "file3.txt").read_text() == "Python"


def test_copy_files_with_one_worker(tmp_path):
    source = tmp_path / "source"
    destination = tmp_path / "destination"

    source.mkdir()

    (source / "file1.txt").write_text("Hello")
    (source / "file2.txt").write_text("World")

    copy_files(source, destination, max_workers=1)

    assert (destination / "file1.txt").exists()
    assert (destination / "file2.txt").exists()


def test_copy_files_invalid_max_workers(tmp_path):
    source = tmp_path / "source"
    destination = tmp_path / "destination"

    source.mkdir()

    with pytest.raises(ValueError):
        copy_files(source, destination, max_workers=0)


def test_copy_files_with_extension_and_multiple_workers(tmp_path):
    source = tmp_path / "source"
    destination = tmp_path / "destination"

    source.mkdir()

    (source / "file1.txt").write_text("Text")
    (source / "file2.txt").write_text("Text")
    (source / "image.png").write_text("Image")

    copy_files(
        source,
        destination,
        extension=".txt",
        max_workers=3,
    )

    assert (destination / "file1.txt").exists()
    assert (destination / "file2.txt").exists()
    assert not (destination / "image.png").exists()


def test_move_files_with_multiple_workers(tmp_path):
    source = tmp_path / "source"
    destination = tmp_path / "destination"

    source.mkdir()

    (source / "file1.txt").write_text("Hello")
    (source / "file2.txt").write_text("World")
    (source / "file3.txt").write_text("Python")

    move_files(source, destination, max_workers=3)

    assert not (source / "file1.txt").exists()
    assert not (source / "file2.txt").exists()
    assert not (source / "file3.txt").exists()

    assert (destination / "file1.txt").exists()
    assert (destination / "file2.txt").exists()
    assert (destination / "file3.txt").exists()

    assert (destination / "file1.txt").read_text() == "Hello"
    assert (destination / "file2.txt").read_text() == "World"
    assert (destination / "file3.txt").read_text() == "Python"


def test_move_files_with_one_worker(tmp_path):
    source = tmp_path / "source"
    destination = tmp_path / "destination"

    source.mkdir()

    (source / "file1.txt").write_text("Hello")
    (source / "file2.txt").write_text("World")

    move_files(source, destination, max_workers=1)

    assert not (source / "file1.txt").exists()
    assert not (source / "file2.txt").exists()

    assert (destination / "file1.txt").exists()
    assert (destination / "file2.txt").exists()


def test_move_files_invalid_max_workers(tmp_path):
    source = tmp_path / "source"
    destination = tmp_path / "destination"

    source.mkdir()

    with pytest.raises(ValueError):
        move_files(source, destination, max_workers=0)


def test_move_files_with_extension_and_multiple_workers(tmp_path):
    source = tmp_path / "source"
    destination = tmp_path / "destination"

    source.mkdir()

    (source / "file1.txt").write_text("Text")
    (source / "file2.txt").write_text("Text")
    (source / "image.png").write_text("Image")

    move_files(
        source,
        destination,
        extension=".txt",
        max_workers=3,
    )

    assert not (source / "file1.txt").exists()
    assert not (source / "file2.txt").exists()

    assert (destination / "file1.txt").exists()
    assert (destination / "file2.txt").exists()

    assert (source / "image.png").exists()
    assert not (destination / "image.png").exists()


def test_organize_by_extension_with_multiple_workers(tmp_path):
    folder = tmp_path / "folder"
    folder.mkdir()

    (folder / "image1.jpg").write_text("Image 1")
    (folder / "image2.jpg").write_text("Image 2")
    (folder / "song.mp3").write_text("Song")
    (folder / "README").write_text("Read me")

    organize_by_extension(folder, max_workers=3)

    assert (folder / "JPG" / "image1.jpg").exists()
    assert (folder / "JPG" / "image2.jpg").exists()
    assert (folder / "MP3" / "song.mp3").exists()
    assert (folder / "No Extension" / "README").exists()

    assert not (folder / "image1.jpg").exists()
    assert not (folder / "image2.jpg").exists()
    assert not (folder / "song.mp3").exists()
    assert not (folder / "README").exists()


def test_organize_by_extension_with_destination_and_multiple_workers(
    tmp_path,
):
    source = tmp_path / "source"
    destination = tmp_path / "destination"

    source.mkdir()

    (source / "image.jpg").write_text("Image")
    (source / "song.mp3").write_text("Song")
    (source / "README").write_text("Read me")

    organize_by_extension(
        source,
        destination,
        max_workers=3,
    )

    assert (source / "image.jpg").exists()
    assert (source / "song.mp3").exists()
    assert (source / "README").exists()

    assert (destination / "JPG" / "image.jpg").exists()
    assert (destination / "MP3" / "song.mp3").exists()
    assert (destination / "No Extension" / "README").exists()


def test_organize_by_extension_with_one_worker(tmp_path):
    folder = tmp_path / "folder"
    folder.mkdir()

    (folder / "file1.txt").write_text("Hello")
    (folder / "file2.txt").write_text("World")

    organize_by_extension(folder, max_workers=1)

    assert (folder / "TXT" / "file1.txt").exists()
    assert (folder / "TXT" / "file2.txt").exists()


def test_organize_by_extension_invalid_max_workers(tmp_path):
    folder = tmp_path / "folder"
    folder.mkdir()

    with pytest.raises(ValueError):
        organize_by_extension(folder, max_workers=0)


def test_delete_files_with_multiple_workers(tmp_path):
    folder = tmp_path / "folder"
    folder.mkdir()

    (folder / "file 1.txt").write_text("One")
    (folder / "file 2.txt").write_text("Two")
    (folder / "file 3.txt").write_text("Three")

    delete_files(
        3,
        "file",
        folder_name=folder,
        max_workers=3,
    )

    assert not (folder / "file 1.txt").exists()
    assert not (folder / "file 2.txt").exists()
    assert not (folder / "file 3.txt").exists()


def test_delete_files_with_one_worker(tmp_path):
    folder = tmp_path / "folder"
    folder.mkdir()

    (folder / "file 1.txt").write_text("One")
    (folder / "file 2.txt").write_text("Two")

    delete_files(
        2,
        "file",
        folder_name=folder,
        max_workers=1,
    )

    assert not (folder / "file 1.txt").exists()
    assert not (folder / "file 2.txt").exists()


def test_delete_files_invalid_max_workers(tmp_path):
    folder = tmp_path / "folder"
    folder.mkdir()

    with pytest.raises(ValueError):
        delete_files(
            3,
            "file",
            folder_name=folder,
            max_workers=0,
        )


def test_delete_files_invalid_number(tmp_path):
    folder = tmp_path / "folder"
    folder.mkdir()

    with pytest.raises(ValueError):
        delete_files(
            0,
            "file",
            folder_name=folder,
        )


def test_delete_files_with_extension(tmp_path):
    folder = tmp_path / "folder"
    folder.mkdir()

    (folder / "file 1.TXT").write_text("One")
    (folder / "file 2.TXT").write_text("Two")
    (folder / "file 3.png").write_text("Image")

    delete_files(
        2,
        "file",
        extension="TXT",
        folder_name=folder,
        max_workers=2,
    )

    assert not (folder / "file 1.TXT").exists()
    assert not (folder / "file 2.TXT").exists()
    assert (folder / "file 3.png").exists()


def test_delete_files_missing_files(tmp_path):
    folder = tmp_path / "folder"
    folder.mkdir()

    (folder / "file 1.txt").write_text("One")

    delete_files(
        3,
        "file",
        folder_name=folder,
        max_workers=3,
    )

    assert not (folder / "file 1.txt").exists()
    assert not (folder / "file 2.txt").exists()
    assert not (folder / "file 3.txt").exists()


def test_delete_by_keyword_with_multiple_workers(tmp_path):
    folder = tmp_path / "folder"
    folder.mkdir()

    (folder / "python_file.txt").write_text("Python")
    (folder / "python_code.txt").write_text("Code")
    (folder / "hello.txt").write_text("Hello")

    delete_by_keyword(
        "python",
        folder_name=folder,
        max_workers=3,
    )

    assert not (folder / "python_file.txt").exists()
    assert not (folder / "python_code.txt").exists()
    assert (folder / "hello.txt").exists()


def test_delete_by_keyword_with_one_worker(tmp_path):
    folder = tmp_path / "folder"
    folder.mkdir()

    (folder / "python_file.txt").write_text("Python")
    (folder / "python_code.txt").write_text("Code")

    delete_by_keyword(
        "python",
        folder_name=folder,
        max_workers=1,
    )

    assert not (folder / "python_file.txt").exists()
    assert not (folder / "python_code.txt").exists()


def test_delete_by_keyword_with_extension(tmp_path):
    folder = tmp_path / "folder"
    folder.mkdir()

    (folder / "python_file.txt").write_text("Text")
    (folder / "python_code.py").write_text("Python")
    (folder / "python_notes.txt").write_text("Notes")

    delete_by_keyword(
        "python",
        extension=".txt",
        folder_name=folder,
        max_workers=2,
    )

    assert not (folder / "python_file.txt").exists()
    assert not (folder / "python_notes.txt").exists()
    assert (folder / "python_code.py").exists()


def test_delete_by_keyword_case_insensitive(tmp_path):
    folder = tmp_path / "folder"
    folder.mkdir()

    (folder / "Python_File.txt").write_text("Python")
    (folder / "PYTHON_Code.txt").write_text("Code")
    (folder / "hello.txt").write_text("Hello")

    delete_by_keyword(
        "PYTHON",
        folder_name=folder,
        max_workers=2,
    )

    assert not (folder / "Python_File.txt").exists()
    assert not (folder / "PYTHON_Code.txt").exists()
    assert (folder / "hello.txt").exists()


def test_delete_by_keyword_empty_keyword(tmp_path):
    folder = tmp_path / "folder"
    folder.mkdir()

    with pytest.raises(ValueError):
        delete_by_keyword(
            "",
            folder_name=folder,
        )


def test_delete_by_keyword_invalid_max_workers(tmp_path):
    folder = tmp_path / "folder"
    folder.mkdir()

    with pytest.raises(ValueError):
        delete_by_keyword(
            "python",
            folder_name=folder,
            max_workers=0,
        )


def test_delete_by_keyword_does_not_delete_non_matching_files(tmp_path):
    folder = tmp_path / "folder"
    folder.mkdir()

    (folder / "python_file.txt").write_text("Python")
    (folder / "hello.txt").write_text("Hello")
    (folder / "notes.txt").write_text("Notes")

    delete_by_keyword(
        "python",
        folder_name=folder,
        max_workers=3,
    )

    assert not (folder / "python_file.txt").exists()
    assert (folder / "hello.txt").exists()
    assert (folder / "notes.txt").exists()


def test_clear_empty_files_with_multiple_workers(tmp_path):
    folder = tmp_path / "folder"
    folder.mkdir()

    (folder / "empty1.txt").touch()
    (folder / "empty2.txt").touch()
    (folder / "empty3.txt").touch()
    (folder / "file.txt").write_text("Hello")

    clear_empty_files(
        folder,
        max_workers=3,
    )

    assert not (folder / "empty1.txt").exists()
    assert not (folder / "empty2.txt").exists()
    assert not (folder / "empty3.txt").exists()
    assert (folder / "file.txt").exists()


def test_clear_empty_files_with_one_worker(tmp_path):
    folder = tmp_path / "folder"
    folder.mkdir()

    (folder / "empty1.txt").touch()
    (folder / "empty2.txt").touch()

    clear_empty_files(
        folder,
        max_workers=1,
    )

    assert not (folder / "empty1.txt").exists()
    assert not (folder / "empty2.txt").exists()


def test_clear_empty_files_recursive(tmp_path):
    folder = tmp_path / "folder"
    subfolder = folder / "subfolder"
    subfolder.mkdir(parents=True)

    (folder / "empty1.txt").touch()
    (subfolder / "empty2.txt").touch()
    (subfolder / "file.txt").write_text("Hello")

    clear_empty_files(
        folder,
        recursive=True,
        max_workers=3,
    )

    assert not (folder / "empty1.txt").exists()
    assert not (subfolder / "empty2.txt").exists()
    assert (subfolder / "file.txt").exists()


def test_clear_empty_files_with_extension(tmp_path):
    folder = tmp_path / "folder"
    folder.mkdir()

    (folder / "empty1.txt").touch()
    (folder / "empty2.txt").touch()
    (folder / "empty3.py").touch()

    clear_empty_files(
        folder,
        extension=".txt",
        max_workers=2,
    )

    assert not (folder / "empty1.txt").exists()
    assert not (folder / "empty2.txt").exists()
    assert (folder / "empty3.py").exists()


def test_clear_empty_files_extension_case_insensitive(tmp_path):
    folder = tmp_path / "folder"
    folder.mkdir()

    (folder / "empty1.TXT").touch()
    (folder / "empty2.TxT").touch()
    (folder / "empty3.py").touch()

    clear_empty_files(
        folder,
        extension="TXT",
        max_workers=2,
    )

    assert not (folder / "empty1.TXT").exists()
    assert not (folder / "empty2.TxT").exists()
    assert (folder / "empty3.py").exists()


def test_clear_empty_files_invalid_max_workers(tmp_path):
    folder = tmp_path / "folder"
    folder.mkdir()

    with pytest.raises(ValueError):
        clear_empty_files(
            folder,
            max_workers=0,
        )


def test_create_files_with_multiple_workers(tmp_path):
    folder = tmp_path / "folder"

    create_files(
        5,
        folder_name=folder,
        max_workers=3,
    )

    for number in range(1, 6):
        assert (folder / f"File {number}.txt").exists()


def test_create_files_with_one_worker(tmp_path):
    folder = tmp_path / "folder"

    create_files(
        3,
        folder_name=folder,
        max_workers=1,
    )

    for number in range(1, 4):
        assert (folder / f"File {number}.txt").exists()


def test_create_files_invalid_max_workers(tmp_path):
    folder = tmp_path / "folder"

    with pytest.raises(ValueError):
        create_files(
            3,
            folder_name=folder,
            max_workers=0,
        )


def test_create_files_with_custom_parameters(tmp_path):
    folder = tmp_path / "folder"

    create_files(
        3,
        file_name="Test",
        sep="-",
        extension=".PY",
        folder_name=folder,
        max_workers=2,
    )

    for number in range(1, 4):
        assert (folder / f"Test-{number}.py").exists()


def test_create_files_creates_folder(tmp_path):
    folder = tmp_path / "new_folder"

    create_files(
        3,
        folder_name=folder,
        max_workers=2,
    )

    assert folder.exists()

    for number in range(1, 4):
        assert (folder / f"File {number}.txt").exists()


def test_rename_files_with_multiple_workers(tmp_path):
    folder = tmp_path / "folder"
    folder.mkdir()

    for number in range(1, 6):
        (folder / f"File {number}.txt").write_text("Test")

    rename_files(
        5,
        "File",
        "Renamed",
        folder_name=folder,
        max_workers=3,
    )

    for number in range(1, 6):
        assert (folder / f"Renamed {number}.txt").exists()
        assert not (folder / f"File {number}.txt").exists()


def test_rename_files_with_one_worker(tmp_path):
    folder = tmp_path / "folder"
    folder.mkdir()

    for number in range(1, 4):
        (folder / f"File {number}.txt").write_text("Test")

    rename_files(
        3,
        "File",
        "Renamed",
        folder_name=folder,
        max_workers=1,
    )

    for number in range(1, 4):
        assert (folder / f"Renamed {number}.txt").exists()
        assert not (folder / f"File {number}.txt").exists()


def test_rename_files_invalid_max_workers(tmp_path):
    folder = tmp_path / "folder"
    folder.mkdir()

    with pytest.raises(ValueError):
        rename_files(
            3,
            "File",
            "Renamed",
            folder_name=folder,
            max_workers=0,
        )


def test_rename_files_does_not_rename_missing_files(tmp_path):
    folder = tmp_path / "folder"
    folder.mkdir()

    (folder / "File 1.txt").write_text("Test")
    (folder / "File 3.txt").write_text("Test")

    rename_files(
        3,
        "File",
        "Renamed",
        folder_name=folder,
        max_workers=2,
    )

    assert (folder / "Renamed 1.txt").exists()
    assert not (folder / "Renamed 2.txt").exists()
    assert (folder / "Renamed 3.txt").exists()


def test_rename_files_with_custom_parameters(tmp_path):
    folder = tmp_path / "folder"
    folder.mkdir()

    for number in range(1, 4):
        (folder / f"Old-{number}.PY").write_text("Test")

    rename_files(
        3,
        "Old",
        "New",
        old_sep="-",
        new_sep="_",
        extension=".PY",
        folder_name=folder,
        max_workers=2,
    )

    for number in range(1, 4):
        assert (folder / f"New_{number}.py").exists()
        assert not (folder / f"Old-{number}.PY").exists()


def test_rename_by_keyword_with_multiple_workers(tmp_path):
    folder = tmp_path / "folder"
    folder.mkdir()

    (folder / "Python_one.txt").write_text("Test")
    (folder / "Python_two.txt").write_text("Test")
    (folder / "Python_three.txt").write_text("Test")
    (folder / "Other.txt").write_text("Test")

    rename_by_keyword(
        "python",
        "Renamed",
        folder_name=folder,
        max_workers=3,
    )

    for number in range(1, 4):
        assert (folder / f"Renamed {number}.txt").exists()

    assert (folder / "Other.txt").exists()


def test_rename_by_keyword_with_one_worker(tmp_path):
    folder = tmp_path / "folder"
    folder.mkdir()

    (folder / "Python_one.txt").write_text("Test")
    (folder / "Python_two.txt").write_text("Test")
    (folder / "Other.txt").write_text("Test")

    rename_by_keyword(
        "python",
        "Renamed",
        folder_name=folder,
        max_workers=1,
    )

    for number in range(1, 3):
        assert (folder / f"Renamed {number}.txt").exists()

    assert (folder / "Other.txt").exists()


def test_rename_by_keyword_invalid_max_workers(tmp_path):
    folder = tmp_path / "folder"
    folder.mkdir()

    (folder / "Python.txt").write_text("Test")

    with pytest.raises(ValueError):
        rename_by_keyword(
            "python",
            "Renamed",
            folder_name=folder,
            max_workers=0,
        )


def test_rename_by_keyword_empty_keyword(tmp_path):
    folder = tmp_path / "folder"
    folder.mkdir()

    (folder / "Python.txt").write_text("Test")

    with pytest.raises(ValueError):
        rename_by_keyword(
            "",
            "Renamed",
            folder_name=folder,
        )


def test_rename_by_keyword_with_extension(tmp_path):
    folder = tmp_path / "folder"
    folder.mkdir()

    (folder / "Python_one.txt").write_text("Test")
    (folder / "Python_two.txt").write_text("Test")
    (folder / "Python_three.py").write_text("Test")

    rename_by_keyword(
        "python",
        "Renamed",
        extension=".TXT",
        folder_name=folder,
        max_workers=2,
    )

    assert (folder / "Renamed 1.txt").exists()
    assert (folder / "Renamed 2.txt").exists()

    assert (folder / "Python_three.py").exists()


def test_rename_by_keyword_with_custom_separator(tmp_path):
    folder = tmp_path / "folder"
    folder.mkdir()

    (folder / "Python_one.txt").write_text("Test")
    (folder / "Python_two.txt").write_text("Test")

    rename_by_keyword(
        "python",
        "Renamed",
        sep="-",
        folder_name=folder,
        max_workers=2,
    )

    assert (folder / "Renamed-1.txt").exists()
    assert (folder / "Renamed-2.txt").exists()


def test_rename_by_keyword_does_not_rename_non_matching_files(tmp_path):
    folder = tmp_path / "folder"
    folder.mkdir()

    (folder / "Python.txt").write_text("Test")
    (folder / "Java.txt").write_text("Test")
    (folder / "C++.txt").write_text("Test")

    rename_by_keyword(
        "python",
        "Renamed",
        folder_name=folder,
        max_workers=2,
    )

    assert (folder / "Renamed 1.txt").exists()
    assert (folder / "Java.txt").exists()
    assert (folder / "C++.txt").exists()


def test_rename_by_keyword_to_existing_name(tmp_path):
    folder = tmp_path / "folder"
    folder.mkdir()

    (folder / "Python_one.txt").write_text("Test")
    (folder / "Python_two.txt").write_text("Test")
    (folder / "Renamed 1.txt").write_text("Existing")

    with pytest.raises(FileExistsError):
        rename_by_keyword(
            "python",
            "Renamed",
            folder_name=folder,
            max_workers=2,
        )

    assert (folder / "Python_one.txt").exists()
    assert (folder / "Python_two.txt").exists()


def test_rename_by_keyword_old_path_equals_new_path(tmp_path):
    folder = tmp_path / "folder"
    folder.mkdir()

    (folder / "Python 1.txt").write_text("Test")

    with pytest.raises(ValueError):
        rename_by_keyword(
            "python",
            "Python",
            folder_name=folder,
        )

    assert (folder / "Python 1.txt").exists()


def test_rename_by_keyword_preserves_extensions(tmp_path):
    folder = tmp_path / "folder"
    folder.mkdir()

    (folder / "Python_one.txt").write_text("Test")
    (folder / "Python_two.py").write_text("Test")
    (folder / "Python_three.md").write_text("Test")

    rename_by_keyword(
        "python",
        "Renamed",
        folder_name=folder,
        max_workers=3,
    )

    renamed_files = list(folder.glob("Renamed *"))

    assert len(renamed_files) == 3
    assert {file.suffix for file in renamed_files} == {
        ".txt",
        ".py",
        ".md",
    }


def test_get_files_count_recursive(tmp_path):
    folder = tmp_path / "folder"
    subfolder = folder / "subfolder"
    subfolder.mkdir(parents=True)

    (folder / "file1.txt").write_text("Test")
    (folder / "file2.txt").write_text("Test")
    (subfolder / "file3.txt").write_text("Test")
    (subfolder / "file4.txt").write_text("Test")

    assert get_files_count(folder) == 2
    assert get_files_count(folder, recursive=True) == 4