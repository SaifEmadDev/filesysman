from filesysman import (
    create_files,
    delete_files,
    rename_files,
    get_files,
    find_files,
    get_files_count,
    rename_by_keyword,
    delete_by_keyword,
    copy_files,
    move_files,
    organize_by_extension,
    get_files_recursive,
    find_files_recursive,
    get_folders,
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
    (tmp_path / "file1.txt").write_text("Hello")
    (tmp_path / "file2.py").write_text("Python")
    (tmp_path / "file3.txt").write_text("World")
    (tmp_path / "folder").mkdir()

    files = get_files(tmp_path)

    assert len(files) == 3
    assert tmp_path / "file1.txt" in files
    assert tmp_path / "file2.py" in files
    assert tmp_path / "file3.txt" in files


def test_get_files_with_extension(tmp_path):
    (tmp_path / "file1.txt").write_text("Hello")
    (tmp_path / "file2.py").write_text("Python")
    (tmp_path / "file3.txt").write_text("World")

    files = get_files(tmp_path, ".txt")

    assert len(files) == 2
    assert tmp_path / "file1.txt" in files
    assert tmp_path / "file3.txt" in files
    assert tmp_path / "file2.py" not in files


def test_find_files(tmp_path):
    (tmp_path / "Python_notes.txt").write_text("Python")
    (tmp_path / "Python_project.py").write_text("Python")
    (tmp_path / "Java_notes.txt").write_text("Java")

    files = find_files("python", tmp_path)

    assert len(files) == 2
    assert tmp_path / "Python_notes.txt" in files
    assert tmp_path / "Python_project.py" in files


def test_find_files_with_extension(tmp_path):
    (tmp_path / "Python_notes.txt").write_text("Python")
    (tmp_path / "Python_project.py").write_text("Python")
    (tmp_path / "Java_notes.txt").write_text("Java")

    files = find_files("python", tmp_path, ".txt")

    assert len(files) == 1
    assert tmp_path / "Python_notes.txt" in files


def test_get_files_count(tmp_path):
    (tmp_path / "file1.txt").write_text("Hello")
    (tmp_path / "file2.txt").write_text("World")
    (tmp_path / "file3.py").write_text("Python")
    (tmp_path / "folder").mkdir()

    assert get_files_count(tmp_path) == 3
    assert get_files_count(tmp_path, ".txt") == 2
    assert get_files_count(tmp_path, ".py") == 1


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


def test_get_files_recursive(tmp_path):
    (tmp_path / "file1.txt").write_text("Hello")

    folder1 = tmp_path / "folder1"
    folder1.mkdir()

    (folder1 / "file2.txt").write_text("World")

    folder2 = folder1 / "folder2"
    folder2.mkdir()

    (folder2 / "file3.py").write_text("Python")

    files = get_files_recursive(tmp_path)

    assert len(files) == 3
    assert tmp_path / "file1.txt" in files
    assert folder1 / "file2.txt" in files
    assert folder2 / "file3.py" in files


def test_get_files_recursive_with_extension(tmp_path):
    (tmp_path / "file1.txt").write_text("Hello")

    folder = tmp_path / "folder"
    folder.mkdir()

    (folder / "file2.txt").write_text("World")
    (folder / "file3.py").write_text("Python")

    files = get_files_recursive(tmp_path, ".txt")

    assert len(files) == 2
    assert tmp_path / "file1.txt" in files
    assert folder / "file2.txt" in files
    assert folder / "file3.py" not in files


def test_find_files_recursive(tmp_path):
    (tmp_path / "Python_notes.txt").write_text("Notes")

    folder = tmp_path / "projects"
    folder.mkdir()

    (folder / "Python_project.py").write_text("Project")

    subfolder = folder / "old"
    subfolder.mkdir()

    (subfolder / "Java_project.py").write_text("Java")

    files = find_files_recursive("python", tmp_path)

    assert len(files) == 2
    assert tmp_path / "Python_notes.txt" in files
    assert folder / "Python_project.py" in files
    assert subfolder / "Java_project.py" not in files


def test_find_files_recursive_with_extension(tmp_path):
    (tmp_path / "Python_notes.txt").write_text("Notes")

    folder = tmp_path / "projects"
    folder.mkdir()

    (folder / "Python_project.py").write_text("Project")
    (folder / "Python_test.txt").write_text("Test")

    files = find_files_recursive("python", tmp_path, ".txt")

    assert len(files) == 2
    assert tmp_path / "Python_notes.txt" in files
    assert folder / "Python_test.txt" in files
    assert folder / "Python_project.py" not in files


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