from files import Folder


def test_create(tmp_path):
    folder = Folder("my_folder")

    folder.create(tmp_path)

    assert folder.exists()
    assert folder.path == tmp_path / "my_folder"


def test_str(tmp_path):
    folder = Folder(tmp_path / "test_folder")

    assert str(folder) == str(tmp_path / "test_folder")


def test_delete(tmp_path):
    folder = Folder("my_folder")

    folder.create(tmp_path)
    folder.delete()

    assert not folder.exists()


def test_rename(tmp_path):
    folder = Folder("old_folder")

    folder.create(tmp_path)
    folder.rename("new_folder")

    assert folder.name == "new_folder"
    assert folder.exists()
    assert not (tmp_path / "old_folder").exists()


def test_copy(tmp_path):
    folder = Folder("original")

    folder.create(tmp_path)

    file = folder.path / "test.txt"
    file.write_text("Hello, pytest!")

    destination = tmp_path / "copies"
    destination.mkdir()

    folder.copy(destination)

    copied_file = destination / "test.txt"

    assert folder.exists()
    assert destination.exists()
    assert copied_file.exists()
    assert copied_file.read_text() == "Hello, pytest!"


def test_move(tmp_path):
    folder = Folder("original")

    folder.create(tmp_path)

    file = folder.path / "test.txt"
    file.write_text("Hello, move!")

    destination = tmp_path / "moved"

    folder.move(destination)

    moved_folder = destination / "original"
    moved_file = moved_folder / "test.txt"

    assert not (tmp_path / "original").exists()
    assert destination.exists()
    assert moved_folder.exists()
    assert moved_file.exists()
    assert folder.path == moved_folder
    assert moved_file.read_text() == "Hello, move!"


def test_clear(tmp_path):
    folder = Folder("test_folder")

    folder.create(tmp_path)

    (folder.path / "file1.txt").write_text("Hello")
    (folder.path / "file2.txt").write_text("World")

    subfolder = folder.path / "subfolder"
    subfolder.mkdir()

    (subfolder / "file3.txt").write_text("Python")

    folder.clear()

    assert folder.exists()
    assert folder.is_empty()


def test_exists(tmp_path):
    folder = Folder("test_folder")

    assert not folder.exists()

    folder.create(tmp_path)

    assert folder.exists()

    folder.delete()

    assert not folder.exists()


def test_is_empty(tmp_path):
    folder = Folder("test_folder")

    folder.create(tmp_path)

    assert folder.is_empty()

    (folder.path / "test.txt").write_text("Hello!")

    assert not folder.is_empty()

    (folder.path / "test.txt").unlink()

    assert folder.is_empty()


def test_folder_properties(tmp_path):
    folder = Folder("test_folder")

    folder.create(tmp_path)

    assert folder.path == tmp_path / "test_folder"
    assert folder.name == "test_folder"
    assert folder.parent == tmp_path
    assert folder.absolute_path.is_absolute()
    assert folder.created_time is not None
    assert folder.modified_time is not None
    assert folder.accessed_time is not None
    assert folder.is_absolute == tmp_path.joinpath("test_folder").is_absolute()


def test_folder_size(tmp_path):
    folder = Folder("test_folder")

    folder.create(tmp_path)

    (folder.path / "file1.txt").write_text("Hello")
    (folder.path / "file2.txt").write_text("Python!")

    subfolder = folder.path / "subfolder"
    subfolder.mkdir()

    (subfolder / "file3.txt").write_text("Testing")

    assert folder.current_size == 5 + 7
    assert folder.total_size == 5 + 7 + 7