import os
from transformers import AutoTokenizer
from datasets import load_from_disk
from doc_summarizer.entity import TransformConfig


class TransformData:
    def __init__(self, config: TransformConfig):
        self.config = config
        self.tokenizer = AutoTokenizer.from_pretrained(config.tokenizer_name)

    def convert_examples_to_features(self, example_batch):
        input_encodings = self.tokenizer(example_batch['dialogue'], max_length=1024, truncation=True)
        with self.tokenizer.as_target_tokenizer():
            target_encodings = self.tokenizer(example_batch['summary'], max_length=128, truncation=True)
        return {
            'input_ids': input_encodings['input_ids'],
            'attention_mask': input_encodings['attention_mask'],
            'labels': target_encodings['input_ids']
        }

    def convert(self):
        raw_dataset = load_from_disk(self.config.data_path)
        encoded_dataset = raw_dataset.map(self.convert_examples_to_features, batched=True)
        encoded_dataset.save_to_disk(os.path.join(self.config.root_dir, "samsum_dataset"))


