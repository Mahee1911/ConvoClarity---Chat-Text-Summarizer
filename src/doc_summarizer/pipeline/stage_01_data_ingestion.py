from doc_summarizer.config.configuration import ConfigManager
from doc_summarizer.components.data_ingestion import IngestData
from doc_summarizer.logging import app_logger


class IngestionPipeline:
    def __init__(self):
        pass

    def execute(self):
        cfg_manager = ConfigManager()
        ingestion_cfg = cfg_manager.get_data_ingestion_config()
        ingester = IngestData(config=ingestion_cfg)
        ingester.download_file()
        ingester.extract_zip_file()
