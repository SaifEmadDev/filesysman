import pytest

from filesysman import (
    File,
    Folder,
    create_files,
    delete_files,
    rename_files,
    copy_files,
    move_files,
    organize_by_extension,
    get_files,
    find_files,
    get_files_count,
    get_files_recursive,
    find_files_recursive,
    get_folders,
    clear_empty_folders,
    rename_by_keyword,
    delete_by_keyword,
    clear_empty_files,
)


def test_create_files_invalid_number(tmp_path):
    with pytest.raises(ValueError):
        create_files(0, folder_name=tmp_path)

    with pytest.raises(ValueError):
        create_files(-1, folder_name=tmp_path)


def test_delete_files_invalid_number(tmp_path):
    with pytest.raises(ValueError):
        delete_files(0, "Test", folder_name=tmp_path)

    with pytest.raises(ValueError):
        delete_files(-1, "Test", folder_name=tmp_path)


def test_rename_files_invalid_number(tmp_path):
    with pytest.raises(ValueError):
        rename_files(0, "Old", "New", folder_name=tmp_path)

    with pytest.raises(ValueError):
        rename_files(-1, "Old", "New", folder_name=tmp_path)


def test_file_create_exist_ok(tmp_path):
    file = File(tmp_path / "test.txt")

    file.create()

    with pytest.raises(FileExistsError):
        file.create(exist_ok=False)

    file.create(exist_ok=True)

    assert file.exists()


def test_file_delete_missing_ok(tmp_path):
    file = File(tmp_path / "test.txt")

    with pytest.raises(FileNotFoundError):
        file.delete()

    file.delete(missing_ok=True)


def test_folder_create_options(tmp_path):
    folder = Folder(tmp_path / "parent" / "child")

    with pytest.raises(FileNotFoundError):
        folder.create()

    folder.create(parents=True)

    assert folder.exists()

    with pytest.raises(FileExistsError):
        folder.create(parents=True)

    folder.create(parents=True, exist_ok=True)

    assert folder.exists()


def test_folder_delete_filled_ok(tmp_path):
    folder = Folder(tmp_path / "folder")

    folder.create()

    (tmp_path / "folder" / "file.txt").write_text("Hello")

    with pytest.raises(OSError):
        folder.delete()

    folder.delete(filled_ok=True)

    assert not folder.exists()


def test_file_copy_to_nonexistent_destination(tmp_path):
    file = File(tmp_path / "test.txt")

    file.create()
    file.write("Hello")

    destination = tmp_path / "copies"

    file.copy(destination)

    assert (destination / "test.txt").exists()


def test_file_move_to_nonexistent_destination(tmp_path):
    file = File(tmp_path / "test.txt")

    file.create()
    file.write("Hello")

    destination = tmp_path / "moved"

    file.move(destination)

    assert not (tmp_path / "test.txt").exists()
    assert (destination / "test.txt").exists()
    assert file.path == destination / "test.txt"


def test_folder_copy_to_nonexistent_destination(tmp_path):
    folder = Folder(tmp_path / "folder")

    folder.create()

    (tmp_path / "folder" / "file.txt").write_text("Hello")

    destination = tmp_path / "copies"

    folder.copy(destination)

    assert (destination / "file.txt").exists()


def test_folder_move_to_nonexistent_destination(tmp_path):
    folder = Folder(tmp_path / "folder")

    folder.create()

    (tmp_path / "folder" / "file.txt").write_text("Hello")

    destination = tmp_path / "moved"

    folder.move(destination)

    assert not (tmp_path / "folder").exists()
    assert (destination / "folder" / "file.txt").exists()
    assert folder.path == destination / "folder"


def test_copy_files_same_folder(tmp_path):
    (tmp_path / "file.txt").write_text("Hello")

    with pytest.raises(FileExistsError):
        copy_files(tmp_path, tmp_path)


def test_move_files_same_folder(tmp_path):
    (tmp_path / "file.txt").write_text("Hello")

    with pytest.raises(FileExistsError):
        move_files(tmp_path, tmp_path)


def test_organize_by_extension_same_folder(tmp_path):
    (tmp_path / "file.txt").write_text("Hello")

    with pytest.raises(FileExistsError):
        organize_by_extension(tmp_path, tmp_path)


def test_copy_files_nonexistent_destination(tmp_path):
    source = tmp_path / "source"
    destination = tmp_path / "destination"

    source.mkdir()

    (source / "file.txt").write_text("Hello")

    copy_files(source, destination)

    assert (destination / "file.txt").exists()


def test_move_files_nonexistent_destination(tmp_path):
    source = tmp_path / "source"
    destination = tmp_path / "destination"

    source.mkdir()

    (source / "file.txt").write_text("Hello")

    move_files(source, destination)

    assert not (source / "file.txt").exists()
    assert (destination / "file.txt").exists()


def test_extension_without_dot(tmp_path):
    (tmp_path / "file1.txt").write_text("1")
    (tmp_path / "file2.py").write_text("2")

    assert get_files(tmp_path, "txt") == [tmp_path / "file1.txt"]
    assert get_files_count(tmp_path, "txt") == 1


def test_extension_with_uppercase(tmp_path):
    (tmp_path / "file.txt").write_text("1")

    assert get_files(tmp_path, ".TXT") == [tmp_path / "file.txt"]
    assert find_files("file", tmp_path, ".TXT") == [tmp_path / "file.txt"]


def test_no_extension(tmp_path):
    (tmp_path / "README").write_text("Hello")
    (tmp_path / "file.txt").write_text("Hello")

    files = get_files(tmp_path, None)

    assert len(files) == 2
    assert tmp_path / "README" in files
    assert tmp_path / "file.txt" in files


def test_empty_extension(tmp_path):
    (tmp_path / "file.txt").write_text("1")
    (tmp_path / "file.py").write_text("2")

    files = get_files(tmp_path, "")

    assert len(files) == 2
    assert tmp_path / "file.txt" in files
    assert tmp_path / "file.py" in files
    assert get_files_count(tmp_path, "") == 2


def test_recursive_extension_without_dot(tmp_path):
    (tmp_path / "file.txt").write_text("1")

    folder = tmp_path / "folder"
    folder.mkdir()

    (folder / "nested.txt").write_text("2")
    (folder / "nested.py").write_text("3")

    files = get_files_recursive(tmp_path, "txt")

    assert tmp_path / "file.txt" in files
    assert folder / "nested.txt" in files
    assert folder / "nested.py" not in files


def test_find_files_recursive_extension_case(tmp_path):
    (tmp_path / "Python.txt").write_text("1")

    folder = tmp_path / "folder"
    folder.mkdir()

    (folder / "Python.py").write_text("2")

    files = find_files_recursive("python", tmp_path, ".TXT")

    assert files == [tmp_path / "Python.txt"]


def test_create_files_extension_case(tmp_path):
    create_files(
        2,
        file_name="Test",
        extension="TXT",
        folder_name=tmp_path,
    )

    assert (tmp_path / "Test 1.txt").exists()
    assert (tmp_path / "Test 2.txt").exists()


def test_find_files_empty_keyword(tmp_path):
    (tmp_path / "file1.txt").write_text("1")
    (tmp_path / "file2.py").write_text("2")

    with pytest.raises(ValueError):
        find_files("", tmp_path)


def test_find_files_no_match(tmp_path):
    (tmp_path / "python.txt").write_text("1")
    (tmp_path / "java.txt").write_text("2")

    files = find_files("javascript", tmp_path)

    assert files == []


def test_find_files_no_match_with_extension(tmp_path):
    (tmp_path / "python.txt").write_text("1")
    (tmp_path / "python.py").write_text("2")

    files = find_files("python", tmp_path, ".json")

    assert files == []


def test_rename_by_keyword_no_match(tmp_path):
    (tmp_path / "python.txt").write_text("1")
    (tmp_path / "java.txt").write_text("2")

    rename_by_keyword(
        "javascript",
        "New",
        folder_name=tmp_path,
    )

    assert (tmp_path / "python.txt").exists()
    assert (tmp_path / "java.txt").exists()


def test_delete_by_keyword_no_match(tmp_path):
    (tmp_path / "python.txt").write_text("1")
    (tmp_path / "java.txt").write_text("2")

    delete_by_keyword(
        "javascript",
        folder_name=tmp_path,
    )

    assert (tmp_path / "python.txt").exists()
    assert (tmp_path / "java.txt").exists()


def test_delete_by_keyword_empty_keyword(tmp_path):
    (tmp_path / "file1.txt").write_text("1")
    (tmp_path / "file2.py").write_text("2")

    with pytest.raises(ValueError):
        delete_by_keyword("", folder_name=tmp_path)

    assert (tmp_path / "file1.txt").exists()
    assert (tmp_path / "file2.py").exists()


def test_clear_empty_folders_recursive_nested(tmp_path):
    level1 = tmp_path / "level1"
    level2 = level1 / "level2"
    level3 = level2 / "level3"

    level3.mkdir(parents=True)

    clear_empty_folders(tmp_path, recursive=True)

    assert not level3.exists()
    assert level2.exists()
    assert level1.exists()


def test_files_without_extension(tmp_path):
    (tmp_path / "README").write_text("Hello")
    (tmp_path / "LICENSE").write_text("License")

    files = get_files(tmp_path)

    assert len(files) == 2
    assert tmp_path / "README" in files
    assert tmp_path / "LICENSE" in files


def test_empty_folder(tmp_path):
    assert get_files_count(tmp_path) == 0
    assert find_files("anything", tmp_path) == []


def test_file_rename_to_existing_file(tmp_path):
    file1 = File(tmp_path / "file1.txt")
    file2 = File(tmp_path / "file2.txt")

    file1.create()
    file2.create()

    file1.write("File 1")
    file2.write("File 2")

    with pytest.raises(FileExistsError):
        file1.rename("file2.txt")

    assert file1.exists()
    assert file2.exists()


def test_file_copy_over_existing_file(tmp_path):
    file1 = File(tmp_path / "file1.txt")

    file1.create()
    file1.write("New content")

    destination = tmp_path / "destination"
    destination.mkdir()

    (destination / "file1.txt").write_text("Old content")

    file1.copy(destination)

    assert (destination / "file1.txt").read_text() == "New content"
    assert file1.read() == "New content"


def test_folder_copy_over_existing_file(tmp_path):
    folder = Folder(tmp_path / "folder")

    folder.create()

    (tmp_path / "folder" / "file.txt").write_text("New content")

    destination = tmp_path / "destination"
    destination.mkdir()

    (destination / "file.txt").write_text("Old content")

    folder.copy(destination)

    assert (destination / "file.txt").read_text() == "New content"


def test_folder_copy_existing_subfolder(tmp_path):
    folder = Folder(tmp_path / "folder")

    folder.create()

    (tmp_path / "folder" / "new.txt").write_text("New")

    destination = tmp_path / "destination"
    destination.mkdir()

    existing = destination / "existing"
    existing.mkdir()

    (existing / "old.txt").write_text("Old")

    folder.copy(existing)

    assert (existing / "new.txt").exists()
    assert (existing / "old.txt").exists()


def test_rename_files_to_existing_names(tmp_path):
    (tmp_path / "Old 1.txt").write_text("One")
    (tmp_path / "Old 2.txt").write_text("Two")
    (tmp_path / "New 1.txt").write_text("Existing")

    with pytest.raises(FileExistsError):
        rename_files(
            2,
            "Old",
            "New",
            folder_name=tmp_path,
        )

    assert (tmp_path / "Old 1.txt").exists()
    assert (tmp_path / "Old 2.txt").exists()
    assert (tmp_path / "New 1.txt").read_text() == "Existing"


def test_rename_by_keyword_to_existing_name(tmp_path):
    (tmp_path / "Python 1.txt").write_text("One")
    (tmp_path / "Python 2.txt").write_text("Two")
    (tmp_path / "Renamed 1.txt").write_text("Existing")

    with pytest.raises(FileExistsError):
        rename_by_keyword(
            "Python",
            "Renamed",
            folder_name=tmp_path,
        )

    assert (tmp_path / "Renamed 1.txt").read_text() == "Existing"


def test_get_files_recursive_deep_structure(tmp_path):
    level1 = tmp_path / "level1"
    level2 = level1 / "level2"
    level3 = level2 / "level3"

    level3.mkdir(parents=True)

    file1 = level1 / "file1.txt"
    file2 = level2 / "file2.txt"
    file3 = level3 / "file3.txt"

    file1.write_text("1")
    file2.write_text("2")
    file3.write_text("3")

    files = get_files_recursive(tmp_path)

    assert len(files) == 3
    assert file1 in files
    assert file2 in files
    assert file3 in files


def test_get_files_recursive_deep_extension(tmp_path):
    level1 = tmp_path / "level1"
    level2 = level1 / "level2"

    level2.mkdir(parents=True)

    txt_file = level1 / "file.txt"
    py_file = level2 / "file.py"

    txt_file.write_text("1")
    py_file.write_text("2")

    files = get_files_recursive(tmp_path, ".TXT")

    assert files == [txt_file]


def test_find_files_recursive_deep_structure(tmp_path):
    level1 = tmp_path / "level1"
    level2 = level1 / "level2"
    level3 = level2 / "level3"

    level3.mkdir(parents=True)

    file1 = level1 / "Python_file.txt"
    file2 = level2 / "another.txt"
    file3 = level3 / "Python_project.py"

    file1.write_text("1")
    file2.write_text("2")
    file3.write_text("3")

    files = find_files_recursive("python", tmp_path)

    assert len(files) == 2
    assert file1 in files
    assert file3 in files


def test_find_files_recursive_deep_extension_case_insensitive(tmp_path):
    level1 = tmp_path / "level1"
    level2 = level1 / "level2"

    level2.mkdir(parents=True)

    file1 = level1 / "Python.TXT"
    file2 = level2 / "Python.py"

    file1.write_text("1")
    file2.write_text("2")

    files = find_files_recursive("python", tmp_path, ".txt")

    assert files == [file1]


def test_get_folders_recursive_deep_structure(tmp_path):
    level1 = tmp_path / "level1"
    level2 = level1 / "level2"
    level3 = level2 / "level3"

    level3.mkdir(parents=True)

    folders = get_folders(tmp_path, recursive=True)

    assert len(folders) == 3
    assert level1 in folders
    assert level2 in folders
    assert level3 in folders


def test_clear_empty_folders_recursive_preserves_non_empty(tmp_path):
    level1 = tmp_path / "level1"
    level2 = level1 / "level2"

    level2.mkdir(parents=True)

    file = level2 / "file.txt"
    file.write_text("content")

    clear_empty_folders(tmp_path, recursive=True)

    assert level1.exists()
    assert level2.exists()
    assert file.exists()


def test_clear_empty_folders_recursive_removes_empty_siblings(tmp_path):
    empty1 = tmp_path / "empty1"
    empty2 = tmp_path / "empty2"
    non_empty = tmp_path / "non_empty"

    empty1.mkdir()
    empty2.mkdir()
    non_empty.mkdir()

    (non_empty / "file.txt").write_text("content")

    clear_empty_folders(tmp_path, recursive=True)

    assert not empty1.exists()
    assert not empty2.exists()
    assert non_empty.exists()
    assert (non_empty / "file.txt").exists()


def test_clear_empty_files_with_extension(tmp_path):
    (tmp_path / "empty.txt").touch()
    (tmp_path / "empty.py").touch()
    (tmp_path / "empty.md").touch()
    (tmp_path / "filled.txt").write_text("Hello")

    clear_empty_files(tmp_path, extension="TXT")

    assert not (tmp_path / "empty.txt").exists()
    assert (tmp_path / "empty.py").exists()
    assert (tmp_path / "empty.md").exists()
    assert (tmp_path / "filled.txt").exists()