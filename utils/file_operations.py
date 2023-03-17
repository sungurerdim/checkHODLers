from .common import DataFrame, read_csv, path, getcwd
from .common import List
from .colorization import *

def read_csv_file(input_file: str) -> List[List[str]]:
    return read_csv(input_file).values.tolist()

def save_list_as_csv(source_list: List[List[str]], target_filename: str) -> str:
    df = DataFrame(source_list).convert_dtypes()
    full_path = path.abspath(target_filename)
    df.to_csv(full_path, index=False, header=False)
    return full_path

def save_list_as_xlsx(source_list: List[List[str]], target_filename: str, sheet_name: str = "Sheet1") -> str:
    df = DataFrame(source_list).convert_dtypes()
    full_path = path.abspath(target_filename)
    df.to_excel(full_path, sheet_name=sheet_name, index=False, header=False)
    return full_path

def file_exists(target_path: str) -> bool:
    if not path.exists(target_path):
        # raise FileNotFoundError(f"'{target_path}' does not exist. Please create it or specify a different path.")
        print()
        print(redLight(f"'{target_path}' does not exist. Please create it or specify a different path."))
        print(yellowLight(f"Current directory: {getcwd()}"))

        return False

    if path.isdir(target_path):
        # raise IsADirectoryError(f"'{target_path}' is a directory. Please specify a file path.")
        print()
        print(redLight(f"'{target_path}' is a directory. Please specify a file path."))
        return False

    if not path.isfile(target_path):
        # raise ValueError(f"'{target_path}' exists but is not a file.")
        print()
        print(redLight(f"'{target_path}' exists but is not a file."))
        print(yellowLight(f"Current directory: {getcwd()}"))
        return False

    return True