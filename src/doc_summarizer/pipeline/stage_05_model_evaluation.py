from doc_summarizer.config.configuration import ConfigManager
from doc_summarizer.components.model_evaluation import EvaluateModel
from doc_summarizer.logging import app_logger


class EvaluatorPipeline:
    def __init__(self):
        pass

    def execute(self):
        cfg_manager = ConfigManager()
        evaluator_cfg = cfg_manager.get_model_evaluation_config()
        evaluator = EvaluateModel(config=evaluator_cfg)
        evaluator.evaluate()