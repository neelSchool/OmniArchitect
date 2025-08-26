# parser/transformer_parser.py

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch
import re
import ast

def regex_fallback(text):
    result = {}
    green = re.search(r"(\d{1,2})\s?%.*green", text, re.I)
    if green:
        result["green_area_ratio"] = float(green.group(1)) / 100
    height = re.search(r"under\s(\d+)", text, re.I)
    if height:
        result["max_building_height"] = float(height.group(1))
    # Simple heuristic for transit connectivity
    if re.search(r"transit|connectivity|transport", text, re.I):
        result["transit_connectivity"] = 1.0
    else:
        result["transit_connectivity"] = 0.0
    return result

class ConstraintParser:
    def __init__(self, model_name="google/flan-t5-small"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    def parse(self, input_text: str) -> dict:
        prompt = (
            "Convert the following text into a Python dictionary with these keys: "
            "green_area_ratio (float), transit_connectivity (float), max_building_height (float). "
            "Only output the dictionary.\n"
            f"Text: {input_text}\n"
            "Dictionary:"
        )

        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True)
        outputs = self.model.generate(**inputs, max_new_tokens=128)
        decoded = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        print("Model output:", decoded)

        try:
            parsed = ast.literal_eval(decoded)
            if isinstance(parsed, dict):
                return parsed
        except Exception:
            pass

        # fallback parser
        fallback_result = regex_fallback(decoded)
        print("Fallback parse result:", fallback_result)
        return fallback_result
