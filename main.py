from doc_summarizer.pipeline.stage_01_data_ingestion import IngestionPipeline
from doc_summarizer.pipeline.stage_02_data_validation import ValidationPipeline
from doc_summarizer.pipeline.stage_03_data_transformation import TransformPipeline
from doc_summarizer.pipeline.stage_04_model_trainer import TrainerPipeline
from doc_summarizer.pipeline.stage_05_model_evaluation import EvaluatorPipeline
from doc_summarizer.logging import app_logger


STAGE_LABEL = "Data Ingestion stage"
try:
   app_logger.info(f">>>>>> stage {STAGE_LABEL} started <<<<<<") 
   ingestion_step = IngestionPipeline()
   ingestion_step.execute()
   app_logger.info(f">>>>>> stage {STAGE_LABEL} completed <<<<<<\n\nx==========x")
except Exception as err:
        app_logger.exception(err)
        raise err




STAGE_LABEL = "Data Validation stage"
try:
   app_logger.info(f">>>>>> stage {STAGE_LABEL} started <<<<<<") 
   validation_step = ValidationPipeline()
   validation_step.execute()
   app_logger.info(f">>>>>> stage {STAGE_LABEL} completed <<<<<<\n\nx==========x")
except Exception as err:
        app_logger.exception(err)
        raise err



STAGE_LABEL = "Data Transformation stage"
try:
   app_logger.info(f">>>>>> stage {STAGE_LABEL} started <<<<<<") 
   transform_step = TransformPipeline()
   transform_step.execute()
   app_logger.info(f">>>>>> stage {STAGE_LABEL} completed <<<<<<\n\nx==========x")
except Exception as err:
        app_logger.exception(err)
        raise err



STAGE_LABEL = "Model Trainer stage"
try: 
   app_logger.info(f"*******************")
   app_logger.info(f">>>>>> stage {STAGE_LABEL} started <<<<<<")
   trainer_step = TrainerPipeline()
   trainer_step.execute()
   app_logger.info(f">>>>>> stage {STAGE_LABEL} completed <<<<<<\n\nx==========x")
except Exception as err:
        app_logger.exception(err)
        raise err




STAGE_LABEL = "Model Evaluation stage"
try: 
   app_logger.info(f"*******************")
   app_logger.info(f">>>>>> stage {STAGE_LABEL} started <<<<<<")
   evaluator_step = EvaluatorPipeline()
   evaluator_step.execute()
   app_logger.info(f">>>>>> stage {STAGE_LABEL} completed <<<<<<\n\nx==========x")
except Exception as err:
        app_logger.exception(err)
        raise err





