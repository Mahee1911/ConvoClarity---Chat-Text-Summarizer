import os
from box.exceptions import BoxValueError
import yaml
from doc_summarizer.logging import app_logger
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any


@ensure_annotations
def load_yaml_config(config_path: Path) -> ConfigBox:
    """Load YAML file and return as ConfigBox."""
    try:
        with open(config_path) as yaml_fp:
            content = yaml.safe_load(yaml_fp)
            app_logger.info(f"yaml file: {config_path} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as err:
        raise err


@ensure_annotations
def ensure_dirs(path_list: list, verbose=True):
    """Create list of directories."""
    for dir_path in path_list:
        os.makedirs(dir_path, exist_ok=True)
        if verbose:
            app_logger.info(f"created directory at: {dir_path}")


@ensure_annotations
def format_file_size(file_path: Path) -> str:
    """Return file size in KB as string."""
    size_kb = round(os.path.getsize(file_path) / 1024)
    return f"~ {size_kb} KB"

    
