from enum import Enum
import json
import os

from dacite import from_dict, Config

from data.app_config import USER_DATA_PATH
from core.userprofile import UserProfile  # type: ignore
from core.datamodels import EnhancedJSONEncoder


def save_user_data(user_id: str, user_data: UserProfile) -> None:
    """Save the user data to a JSON file, normalize addresses first"""
    file_path = os.path.join(USER_DATA_PATH, f"{user_id}.json")
    # first try to dump to json
    _ = json.dumps(user_data, indent=4, cls=EnhancedJSONEncoder)
    with open(file_path, "w+") as f:
        json.dump(user_data, f, indent=4, cls=EnhancedJSONEncoder)


def load_user_data(user_id: str) -> UserProfile:
    """Load the user data from a JSON file"""
    file_path = os.path.join(USER_DATA_PATH, f"{user_id}.json")
    if not os.path.exists(file_path):
        return UserProfile(user_id)

    with open(file_path, "r") as f:
        result = json.load(f)

    return from_dict(data_class=UserProfile, data=result, config=Config(cast=[Enum]))  # type: ignore


def get_user_ids() -> list[str]:
    # Get the list of user IDs from the directory
    user_ids = [
        filename.split(".")[0]
        for filename in os.listdir(USER_DATA_PATH)
        if filename.endswith(".json")
    ]
    return user_ids
