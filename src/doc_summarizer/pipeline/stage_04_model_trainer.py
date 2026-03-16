from doc_summarizer.config.configuration import ConfigManager
from doc_summarizer.components.model_trainer import TrainModel
from doc_summarizer.logging import app_logger


class TrainerPipeline:
    def __init__(self):
        pass

    def execute(self):
        cfg_manager = ConfigManager()
        trainer_cfg = cfg_manager.get_model_trainer_config()
        trainer = TrainModel(config=trainer_cfg)
        trainer.train()