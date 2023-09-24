import yaml
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
config_file_path = os.path.join(current_directory, "config.yaml")

# Sử dụng đường dẫn tuyệt đối để đọc file config.yaml
with open(config_file_path, "r") as f:
    config = yaml.safe_load(f)
