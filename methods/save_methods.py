import json, logging, pathlib

def save_in_big_dict(main_dict: dict, dict: dict):
    for key, value in dict.items():
        main_dict[key] = value

def save_json(data_dict: dict, filename: str):

    current_dir = pathlib.Path(__file__).parent.resolve()
    root = current_dir.parent
    target_dir = root / "examples" / "jsons"
    file_path = target_dir / filename

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data_dict, fp=f, indent=4)

        logging.info(f"File {filename} currently saved")

    except Exception as e:
        logging.error(f"Error to save file {filename} because: {e}")

def save_dict(filename: str):

    current_dir = pathlib.Path(__file__).parent.resolve()
    root = current_dir.parent
    target_dir = root / "examples" / "jsons"
    file_path = target_dir / filename

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data_dict = json.load(f)

        # for key, value in data_dict.items():
        #     data_dict[key] = value[0]

        logging.info(f"file {filename} was currently read")

        return data_dict
    
    except Exception as e:
        logging.error(f"Error to create {filename} to dict: {e}")

        return None
