from files import File


def test_create(tmp_path):
    file = File(tmp_path / "test.txt")

    file.create()

    assert file.exists()
    assert file.is_empty()


def test_str(tmp_path):
    file = File(tmp_path / "test.txt")

    assert str(file) == str(tmp_path / "test.txt")


def test_delete(tmp_path):
    file = File(tmp_path / "test.txt")

    file.create()
    file.delete()

    assert not file.exists()


def test_rename(tmp_path):
    file = File(tmp_path / "old.txt")

    file.create()
    file.rename("new.txt")

    assert file.name == "new.txt"
    assert file.exists()
    assert not (tmp_path / "old.txt").exists()


def test_copy(tmp_path):
    file = File(tmp_path / "original.txt")

    file.create()
    file.write("Hello, pytest!")

    destination = tmp_path / "copies"
    destination.mkdir()

    file.copy(destination)

    copied_file = destination / "original.txt"

    assert file.exists()
    assert copied_file.exists()
    assert copied_file.read_text() == "Hello, pytest!"


def test_move(tmp_path):
    file = File(tmp_path / "test.txt")

    file.create()
    file.write("Hello, move!")

    destination = tmp_path / "moved"
    destination.mkdir()

    file.move(destination)

    moved_file = destination / "test.txt"

    assert not (tmp_path / "test.txt").exists()
    assert moved_file.exists()
    assert file.path == moved_file
    assert file.read() == "Hello, move!"


def test_exists(tmp_path):
    file = File(tmp_path / "test.txt")

    assert not file.exists()

    file.create()

    assert file.exists()

    file.delete()

    assert not file.exists()


def test_is_empty(tmp_path):
    file = File(tmp_path / "test.txt")

    file.create()

    assert file.is_empty()

    file.write("Hello, pytest!")

    assert not file.is_empty()


def test_read_write_append(tmp_path):
    file = File(tmp_path / "test.txt")

    file.create()
    file.write("Hello")

    assert file.read() == "Hello"

    file.append(" World")

    assert file.read() == "Hello World"

    file.write("New text")

    assert file.read() == "New text"


def test_file_properties(tmp_path):
    file = File(tmp_path / "test.txt")

    file.create()
    file.write("Hello")

    assert file.path == tmp_path / "test.txt"
    assert file.name == "test.txt"
    assert file.stem == "test"
    assert file.suffix == ".txt"
    assert file.size == 5
    assert file.parent == tmp_path
    assert file.absolute_path.is_absolute()
    assert file.created_time is not None
    assert file.modified_time is not None
    assert file.accessed_time is not None