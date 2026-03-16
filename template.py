import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')


app_package_name = "doc_summarizer"

file_list = [
    ".github/workflows/.gitkeep",
    f"src/{app_package_name}/__init__.py",
    f"src/{app_package_name}/components/__init__.py",
    f"src/{app_package_name}/utils/__init__.py",
    f"src/{app_package_name}/utils/common.py",
    f"src/{app_package_name}/logging/__init__.py",
    f"src/{app_package_name}/config/__init__.py",
    f"src/{app_package_name}/config/configuration.py",
    f"src/{app_package_name}/pipeline/__init__.py",
    f"src/{app_package_name}/entity/__init__.py",
    f"src/{app_package_name}/constants/__init__.py",
    "config/config.yaml",
    "params.yaml",
    "app.py",
    "main.py",
    "Dockerfile",
    "requirements.txt",
    "setup.py",
    "research/trials.ipynb",

]


for target_path in file_list:
    target_path = Path(target_path)
    parent_dir, file_name = os.path.split(target_path)

    if parent_dir != "":
        os.makedirs(parent_dir, exist_ok=True)
        logging.info(f"Creating directory:{parent_dir} for the file {file_name}")

    
    if (not os.path.exists(target_path)) or (os.path.getsize(target_path) == 0):
        with open(target_path,'w') as f:
            pass
            logging.info(f"Creating empty file: {target_path}")


    
    else:
        logging.info(f"{file_name} is already exists")

