import torch
import pandas as pd
from tqdm import tqdm
import evaluate
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from datasets import load_from_disk
from doc_summarizer.entity import EvaluatorConfig


class EvaluateModel:
    def __init__(self, config: EvaluatorConfig):
        self.config = config

    def generate_batch_sized_chunks(self, elements_list, batch_size):
        """Yield successive batch-sized chunks from elements_list."""
        for idx in range(0, len(elements_list), batch_size):
            yield elements_list[idx : idx + batch_size]

    def calculate_metric_on_test_ds(self, dataset, rouge_metric, model, tokenizer,
                                    batch_size=16, device="cuda" if torch.cuda.is_available() else "cpu",
                                    column_text="article", column_summary="highlights"):
        text_batches = list(self.generate_batch_sized_chunks(dataset[column_text], batch_size))
        ref_batches = list(self.generate_batch_sized_chunks(dataset[column_summary], batch_size))
        for text_batch, ref_batch in tqdm(zip(text_batches, ref_batches), total=len(text_batches)):
            inputs = tokenizer(text_batch, max_length=1024, truncation=True,
                              padding="max_length", return_tensors="pt")
            summaries = model.generate(
                input_ids=inputs["input_ids"].to(device),
                attention_mask=inputs["attention_mask"].to(device),
                length_penalty=0.8, num_beams=8, max_length=128
            )
            decoded = [tokenizer.decode(s, skip_special_tokens=True, clean_up_tokenization_spaces=True)
                       for s in summaries]
            decoded = [d.replace("", " ") for d in decoded]
            rouge_metric.add_batch(predictions=decoded, references=ref_batch)
        return rouge_metric.compute()

    def evaluate(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        tok = AutoTokenizer.from_pretrained(self.config.tokenizer_path)
        seq2seq_model = AutoModelForSeq2SeqLM.from_pretrained(self.config.model_path).to(device)
        encoded_ds = load_from_disk(self.config.data_path)
        rouge_metric = evaluate.load("rouge")
        score = self.calculate_metric_on_test_ds(
            encoded_ds['test'][0:10],
            rouge_metric,
            seq2seq_model,
            tok,
            batch_size=2,
            column_text='dialogue',
            column_summary='summary'
        )
        rouge_names = ["rouge1", "rouge2", "rougeL", "rougeLsum"]
        score_dict = dict((name, float(score[name])) for name in rouge_names)
        results_df = pd.DataFrame(score_dict, index=['pegasus'])
        results_df.to_csv(self.config.metric_file_name, index=False)

            

