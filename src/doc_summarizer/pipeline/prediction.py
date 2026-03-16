from doc_summarizer.config.configuration import ConfigManager
from transformers import AutoTokenizer
from transformers import pipeline


class InferencePipeline:
    def __init__(self):
        self.settings = ConfigManager().get_model_evaluation_config()

    def run_prediction(self, input_text):
        tok = AutoTokenizer.from_pretrained(self.settings.tokenizer_path)
        gen_opts = {"length_penalty": 0.8, "num_beams": 8, "max_length": 128}
        summarizer_pipe = pipeline("summarization", model=self.settings.model_path, tokenizer=tok)
        print("Dialogue:")
        print(input_text)
        summary = summarizer_pipe(input_text, **gen_opts)[0]["summary_text"]
        print("\nModel Summary:")
        print(summary)
        return summary