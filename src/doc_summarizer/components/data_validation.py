import os
from doc_summarizer.logging import app_logger
from doc_summarizer.entity import ValidationConfig


class ValidateData:
    def __init__(self, config: ValidationConfig):
        self.config = config

    def validate_all_files_exist(self) -> bool:
        try:
            is_valid = None
            base_path = os.path.join("artifacts", "data_ingestion", "samsum_dataset")
            dir_entries = os.listdir(base_path)
            for entry in dir_entries:
                if entry not in self.config.ALL_REQUIRED_FILES:
                    is_valid = False
                    with open(self.config.STATUS_FILE, 'w') as fp:
                        fp.write(f"Validation status: {is_valid}")
                else:
                    is_valid = True
                    with open(self.config.STATUS_FILE, 'w') as fp:
                        fp.write(f"Validation status: {is_valid}")
            return is_valid
        except Exception as err:
            raise err
