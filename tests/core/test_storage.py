from pathlib import Path
from unittest.mock import patch
from core import storage


def test_get_user_ids_with_multiple_files(tmp_path: Path):
    user_data_path = tmp_path / "users"
    user_data_path.mkdir(exist_ok=True, parents=True)
    user_data_path.joinpath("abc.json").touch()
    user_data_path.joinpath("def.json").touch()
    expected_user_ids = ["abc", "def"]

    # Call the function
    with patch("core.storage.USER_DATA_PATH", str(user_data_path)):
        user_ids = storage.get_user_ids()
        assert isinstance(user_ids, list)
        assert len(user_ids) > 0
        assert all(isinstance(user_id, str) for user_id in user_ids)
        assert set(expected_user_ids) == set(expected_user_ids)


def test_get_user_ids_with_no_files(tmp_path: Path):
    user_data_path = tmp_path / "users"
    user_data_path.mkdir(exist_ok=True, parents=True)

    # Call the function
    with patch("core.storage.USER_DATA_PATH", str(user_data_path)):
        user_ids = storage.get_user_ids()
        assert isinstance(user_ids, list)
        assert len(user_ids) == 0
        assert user_ids == []
