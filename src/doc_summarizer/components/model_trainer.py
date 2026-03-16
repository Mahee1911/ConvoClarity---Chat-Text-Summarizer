import os
import torch
from transformers import TrainingArguments, Trainer, DataCollatorForSeq2Seq
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from datasets import load_from_disk
from doc_summarizer.entity import TrainerConfig


class TrainModel:
    def __init__(self, config: TrainerConfig):
        self.config = config

    def train(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        tok = AutoTokenizer.from_pretrained(self.config.model_ckpt)
        seq2seq_model = AutoModelForSeq2SeqLM.from_pretrained(self.config.model_ckpt).to(device)
        data_collator = DataCollatorForSeq2Seq(tok, model=seq2seq_model)
        train_dataset = load_from_disk(self.config.data_path)

        training_args = TrainingArguments(
            output_dir=self.config.root_dir, num_train_epochs=1, warmup_steps=500,
            per_device_train_batch_size=1, per_device_eval_batch_size=1,
            weight_decay=0.01, logging_steps=10,
            eval_strategy='steps', eval_steps=500, save_steps=1e6,
            gradient_accumulation_steps=16,
            use_cpu=True
        )

        trainer = Trainer(
            model=seq2seq_model, args=training_args,
            tokenizer=tok, data_collator=data_collator,
            train_dataset=train_dataset["train"],
            eval_dataset=train_dataset["validation"]
        )
        trainer.train()

        seq2seq_model.save_pretrained(os.path.join(self.config.root_dir, "pegasus-samsum-model"))
        tok.save_pretrained(os.path.join(self.config.root_dir, "tokenizer"))
