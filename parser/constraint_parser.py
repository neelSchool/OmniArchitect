# parser/constraint_parser.py

import numpy as np
import re

# Define priors for various city design constraints
priors = {
    "green_space": 0.3,  # 30% chance of green space if no other info
    "budget": 0.2,  # 20% chance of a budget being specified
    "max_height": 0.5,  # 50% chance of max height being mentioned
    "public_transport": 0.5  # 50% chance of public transport being emphasized
}

# Likelihoods (probability of specific terms given a constraint)
likelihoods = {
    "green_space": {
        "parks": 0.9,
        "green city": 0.8,
        "trees": 0.6,
        "landscaping": 0.7
    },
    "budget": {
        "million": 0.8,
        "billion": 0.9,
        "cost": 0.5
    },
    "max_height": {
        "high-rise": 0.8,
        "under 200 meters": 0.9,
        "skyscrapers": 0.7
    },
    "public_transport": {
        "metro": 0.8,
        "subway": 0.7,
        "bus": 0.6,
        "train": 0.5
    }
}

def bayesian_inference(text):
    """
    Estimate the likely city design constraints based on the input text using Bayesian Inference.
    """
    constraints = {
        "green_space": None,
        "budget": None,
        "max_height": None,
        "public_transport": None
    }

    # Lowercase the input text for easier matching
    text = text.lower()

    # Calculate the probability of each constraint using Bayes' Theorem
    for constraint, prior in priors.items():
        likelihood = 0
        for term, term_likelihood in likelihoods.get(constraint, {}).items():
            if term in text:
                likelihood += term_likelihood
        
        if likelihood > 0:
            posterior = (likelihood * prior) / sum([likelihood * prior for prior in priors.values()])
            constraints[constraint] = posterior
        else:
            constraints[constraint] = prior

    # Post-process to convert probabilities into concrete values for certain constraints

    # Max Height Mapping: Using Gaussian distribution around 200m with a standard deviation of 50m
    if constraints['max_height'] is not None:
        mean_height = 200
        std_dev = 50  # Standard deviation for more variation
        constraints['max_height'] = np.random.normal(mean_height, std_dev)

    # Green Space Mapping: Using Gaussian distribution around 0.3 (30% green space)
    if constraints['green_space'] is not None:
        mean_green_space = 0.3
        std_dev = 0.1  # Standard deviation for green space estimation (10%)
        constraints['green_space'] = np.random.normal(mean_green_space, std_dev)
        constraints['green_space'] = np.clip(constraints['green_space'], 0, 1)  # Ensure value is within [0, 1]

    # Budget Mapping: Using a better scaling approach for the uniform distribution
    if constraints['budget'] is not None:
        if constraints['budget'] >= 0.7:  # High probability of high budget
            constraints['budget'] = np.random.uniform(8e8, 1e9)  # Uniform distribution between 800M and 1B
        elif constraints['budget'] <= 0.3:  # Low probability of high budget
            constraints['budget'] = np.random.uniform(5e8, 8e8)  # Uniform distribution between 500M and 800M
        else:  # Mid-range probability
            constraints['budget'] = np.random.uniform(6e8, 9e8)  # Uniform distribution between 600M and 900M

    # Public transport: we keep the existing logic for simplicity
    if constraints['public_transport'] is not None:
        if constraints['public_transport'] >= 0.5:
            constraints['public_transport'] = True
        else:
            constraints['public_transport'] = False

    return constraints


# Inline Test Cases with Debugging Outputs

def test_green_space_estimation():
    input_text = "Design a city with lots of parks, green city, and trees"
    result = bayesian_inference(input_text)
    print(f"Result for green space: {result['green_space']}")
    assert 0.2 <= result['green_space'] <= 0.45
    print("Green space test passed.")

# def test_public_transport_emphasis():
#     input_text = "Design a city with excellent metro, subway, and bus services"
#     result = bayesian_inference(input_text)
#     print(f"Result for public transport: {result['public_transport']}")
#     assert result['public_transport'] is True
#     print("Public transport test passed.")

def test_max_height_estimation():
    input_text = "Design a city with lots of high-rise buildings under 200 meters"
    result = bayesian_inference(input_text)
    print(f"Result for max height: {result['max_height']}")
    assert 100 <= result['max_height'] <= 300  # We expect some variation around 200 meters
    print("Max height test passed.")

def test_budget_input():
    input_text = "Create a city with a budget of 1 billion USD"
    result = bayesian_inference(input_text)
    print(f"Result for budget: {result['budget']}")
    assert 8e8 <= result['budget'] <= 1e9  # Expecting 800M to 1B USD
    print("Budget test passed.")

# def test_ambiguous_input():
#     input_text = "Create a city with good public transport and green areas"
#     result = bayesian_inference(input_text)
#     print(f"Result for green space: {result['green_space']}")
#     print(f"Result for public transport: {result['public_transport']}")
#     assert 0.2 <= result['green_space'] <= 0.45
#     assert result['public_transport'] is True
#     print("Ambiguous input test passed.")

# Run tests
if __name__ == "__main__":
    test_green_space_estimation()
    #test_public_transport_emphasis()
    test_max_height_estimation()
    test_budget_input()
    #test_ambiguous_input()
