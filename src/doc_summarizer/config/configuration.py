from doc_summarizer.constants import *
from doc_summarizer.utils.common import load_yaml_config, ensure_dirs
from doc_summarizer.entity import (IngestionConfig,
                                   ValidationConfig,
                                   TransformConfig,
                                   TrainerConfig,
                                   EvaluatorConfig)


class ConfigManager:
    def __init__(
        self,
        config_path=CONFIG_PATH,
        params_path=PARAMS_PATH):
        self.config = load_yaml_config(config_path)
        self.params = load_yaml_config(params_path)
        ensure_dirs([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> IngestionConfig:
        section = self.config.data_ingestion
        ensure_dirs([section.root_dir])
        return IngestionConfig(
            root_dir=section.root_dir,
            source_URL=section.source_URL,
            local_data_file=section.local_data_file,
            unzip_dir=section.unzip_dir
        )

    def get_data_validation_config(self) -> ValidationConfig:
        section = self.config.data_validation
        ensure_dirs([section.root_dir])
        return ValidationConfig(
            root_dir=section.root_dir,
            STATUS_FILE=section.STATUS_FILE,
            ALL_REQUIRED_FILES=section.ALL_REQUIRED_FILES,
        )

    def get_data_transformation_config(self) -> TransformConfig:
        section = self.config.data_transformation
        ensure_dirs([section.root_dir])
        return TransformConfig(
            root_dir=section.root_dir,
            data_path=section.data_path,
            tokenizer_name=section.tokenizer_name
        )

    def get_model_trainer_config(self) -> TrainerConfig:
        section = self.config.model_trainer
        training_params = self.params.TrainingArguments
        ensure_dirs([section.root_dir])
        return TrainerConfig(
            root_dir=section.root_dir,
            data_path=section.data_path,
            model_ckpt=section.model_ckpt,
            num_train_epochs=training_params.num_train_epochs,
            warmup_steps=training_params.warmup_steps,
            per_device_train_batch_size=training_params.per_device_train_batch_size,
            weight_decay=training_params.weight_decay,
            logging_steps=training_params.logging_steps,
            evaluation_strategy=training_params.evaluation_strategy,
            eval_steps=training_params.evaluation_strategy,
            save_steps=training_params.save_steps,
            gradient_accumulation_steps=training_params.gradient_accumulation_steps
        )

    def get_model_evaluation_config(self) -> EvaluatorConfig:
        section = self.config.model_evaluation
        ensure_dirs([section.root_dir])
        return EvaluatorConfig(
            root_dir=section.root_dir,
            data_path=section.data_path,
            model_path=section.model_path,
            tokenizer_path=section.tokenizer_path,
            metric_file_name=section.metric_file_name
        )
