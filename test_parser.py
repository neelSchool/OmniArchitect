from parser.transformer_parser import ConstraintParser
from parser.schema_utils import SCHEMA

def test_parser_detailed():
    parser = ConstraintParser()

    test_input = (
        "I want a city with medium transit, low air pollution, access to education, "
        "no tall buildings, lots of schools, quiet areas, and strong disaster resilience."
    )

    result = parser.parse(test_input)

    print("\nFinal Parsed Configuration:\n")
    for key in SCHEMA:
        val = result[key]
        print(f"{key:30s}: {val:.3f}")

    assert isinstance(result, dict), "Output must be a dictionary"
    assert all(k in result for k in SCHEMA), "All keys must be present"
    assert all(isinstance(result[k], (float, int)) for k in result), "All values must be numbers"

    print("\nTest passed: All 20 factors successfully parsed or inferred.")

if __name__ == "__main__":
    test_parser_detailed()
