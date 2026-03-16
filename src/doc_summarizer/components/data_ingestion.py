import os
import urllib.request as request
import zipfile
from pathlib import Path
from doc_summarizer.logging import app_logger
from doc_summarizer.utils.common import format_file_size
from doc_summarizer.entity import IngestionConfig


class IngestData:
    def __init__(self, config: IngestionConfig):
        self.config = config

    def download_file(self):
        if not os.path.exists(self.config.local_data_file):
            dest_path, resp_headers = request.urlretrieve(
                url=self.config.source_URL,
                filename=self.config.local_data_file
            )
            app_logger.info(f"{dest_path} download! with following info: \n{resp_headers}")
        else:
            app_logger.info(f"File already exists of size: {format_file_size(Path(self.config.local_data_file))}")

    def extract_zip_file(self):
        """Extract the zip file into the data directory."""
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)