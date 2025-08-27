from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch
import re
import ast
import random
from .schema_utils import SCHEMA

# Default ranges for fallback (for seed-based random fill)
DEFAULTS = {
    "green_area_ratio": (0.1, 0.5),
    "transit_connectivity": (0.0, 1.0),
    "max_building_height": (10, 100),
    "education_access": (0.0, 1.0),
    "housing_affordability": (0.0, 1.0),
    "energy_access": (0.0, 1.0),
    "water_access": (0.0, 1.0),
    "water_bodies": (0, 3),
    "road_network_density": (0.0, 1.0),
    "population_density": (1000, 20000),
    "industrial_zone_ratio": (0.0, 0.3),
    "commercial_zone_ratio": (0.0, 0.3),
    "public_service_access": (0.0, 1.0),
    "waste_management": (0.0, 1.0),
    "healthcare_access": (0.0, 1.0),
    "recreational_zone_ratio": (0.0, 0.3),
    "noise_pollution_level": (0.0, 1.0),
    "air_quality_index": (10, 150),
    "smart_infrastructure": (0.0, 1.0),
    "disaster_resilience": (0.0, 1.0)
}

QUAL_LEVELS = {
    "low": 0.2,
    "medium": 0.5,
    "high": 0.8
}

FACTOR_PATTERNS = {
    "green_area_ratio": ["green area", "parks", "greenery"],
    "transit_connectivity": ["transit", "transport", "connectivity"],
    "max_building_height": ["tall buildings", "high-rises", "building height"],
    "education_access": ["schools", "education"],
    "housing_affordability": ["housing", "affordable housing"],
    "energy_access": ["electricity", "energy"],
    "water_access": ["water access", "running water"],
    "water_bodies": ["lakes", "rivers", "water bodies"],
    "road_network_density": ["roads", "road network"],
    "population_density": ["population density", "crowded", "dense"],
    "industrial_zone_ratio": ["industry", "factories"],
    "commercial_zone_ratio": ["shops", "malls", "commerce"],
    "public_service_access": ["fire station", "police", "public service"],
    "waste_management": ["waste", "garbage", "trash"],
    "healthcare_access": ["hospitals", "healthcare"],
    "recreational_zone_ratio": ["parks", "sports", "recreation"],
    "noise_pollution_level": ["noise", "sound", "quiet"],
    "air_quality_index": ["air", "pollution", "air quality"],
    "smart_infrastructure": ["smart", "tech", "iot"],
    "disaster_resilience": ["disaster", "resilience", "flooding"]
}

def map_level_to_value(level: str, factor: str) -> float:
    level = level.lower()
    base = QUAL_LEVELS.get(level, 0.5)

    if factor in ["air_quality_index", "noise_pollution_level"]:
        return 1.0 - base
    if factor == "max_building_height":
        return {"low": 15.0, "medium": 40.0, "high": 80.0}.get(level, 40.0)
    if factor == "water_bodies":
        return {"low": 0, "medium": 1, "high": 3}.get(level, 1)
    if factor == "population_density":
        return {"low": 3000, "medium": 8000, "high": 15000}.get(level, 8000)
    return base

def regex_fallback(text: str) -> tuple[dict, set]:
    result = {}
    matched = set()

    for factor, keywords in FACTOR_PATTERNS.items():
        for keyword in keywords:
            match = re.search(rf"(low|medium|high)\s+{keyword}", text, re.I)
            if match:
                level = match.group(1).lower()
                result[factor] = map_level_to_value(level, factor)
                matched.add(factor)
                break

        if factor == "max_building_height":
            if re.search(r"no\s+(tall|high)\s+buildings", text, re.I):
                result[factor] = 15.0
                matched.add(factor)
            elif re.search(r"(tall|high)\s+buildings", text, re.I):
                result[factor] = 80.0
                matched.add(factor)

        if factor == "transit_connectivity" and "transit_connectivity" not in result:
            if re.search(r"transit|transport|connectivity", text, re.I):
                result["transit_connectivity"] = 1.0
                matched.add("transit_connectivity")

    return result, matched

def seeded_random_value(key: str) -> float:
    low, high = DEFAULTS.get(key, (0.0, 1.0))
    rnd = random.Random(hash(key) % (2**32))
    return rnd.uniform(low, high)

def fill_missing(parsed: dict, matched: set) -> dict:
    filled = {}
    for key in SCHEMA:
        if key in parsed:
            filled[key] = parsed[key]
        else:
            filled[key] = seeded_random_value(key)
    return filled

class ConstraintParser:
    def __init__(self, model_name="google/flan-t5-small"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    def parse(self, input_text: str) -> dict:
        prompt = (
            "Convert the following text into a Python dictionary with these keys:\n"
            + ", ".join([f"{key} (float)" for key in SCHEMA]) +
            ". Only output the dictionary.\n"
            f"Text: {input_text}\nDictionary:"
        )

        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True)
        outputs = self.model.generate(**inputs, max_new_tokens=256)
        decoded = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        print("Model output:", decoded)

        try:
            parsed = ast.literal_eval(decoded)
            if isinstance(parsed, dict):
                print("Parsed via model")
                return fill_missing(parsed, set(parsed.keys()))
        except Exception:
            pass

        print(" Model parse failed — using regex fallback...")
        fallback_result, matched = regex_fallback(input_text)
        print("Regex matched factors:", matched)
        return fill_missing(fallback_result, matched)
