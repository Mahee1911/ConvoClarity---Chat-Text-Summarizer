from doc_summarizer.config.configuration import ConfigManager
from doc_summarizer.components.data_validation import ValidateData
from doc_summarizer.logging import app_logger


class ValidationPipeline:
    def __init__(self):
        pass

    def execute(self):
        cfg_manager = ConfigManager()
        validation_cfg = cfg_manager.get_data_validation_config()
        validator = ValidateData(config=validation_cfg)
        validator.validate_all_files_exist()