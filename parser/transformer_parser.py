# parser/transformer_parser.py

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch
import ast

class ConstraintParser:
    def __init__(self, model_name="google/flan-t5-small"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    def parse(self, input_text: str) -> dict:
        prompt = f"Extract urban planning constraints from the following request and return as a Python dictionary:\n{input_text}"

        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True)
        outputs = self.model.generate(**inputs, max_new_tokens=128)
        decoded = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        try:
            parsed = ast.literal_eval(decoded)
            if isinstance(parsed, dict):
                return parsed
        except Exception:
            pass

        return {"error": "Could not parse constraints"}
