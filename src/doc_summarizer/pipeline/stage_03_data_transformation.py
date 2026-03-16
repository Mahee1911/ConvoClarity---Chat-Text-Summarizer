from doc_summarizer.config.configuration import ConfigManager
from doc_summarizer.components.data_transformation import TransformData
from doc_summarizer.logging import app_logger


class TransformPipeline:
    def __init__(self):
        pass

    def execute(self):
        cfg_manager = ConfigManager()
        transform_cfg = cfg_manager.get_data_transformation_config()
        transformer = TransformData(config=transform_cfg)
        transformer.convert()