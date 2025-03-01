# -*- coding: utf-8 -*-
"""LLM 1.2.2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ZSkfpphGeXOh6UZJrEqY3l78zBqm2c90
"""

import re
import google.generativeai as genai
import matplotlib.pyplot as plt
from google.colab import userdata
from typing import List

# Constants
EXPECTED_NUMBERS = 1000
PROMPT = """Generate 1000 random numbers uniformly distributed between 0 and 1. 
Return them as a single line of numbers separated by commas, using only digits (0-9), commas, 
and decimal points. No additional text or formatting."""

def configure_gemini() -> None:
    """Configure Gemini AI with API key from secure storage."""
    genai.configure(api_key=userdata.get('GOOGLE_API_KEY'))

def clean_response(response_text: str) -> str:
    """Sanitize AI response using regular expressions for efficiency."""
    return re.sub(r'[^\d.,]', '', response_text)

def parse_numbers(cleaned_text: str) -> List[float]:
    """Optimized parsing with list comprehension and input validation."""
    return [float(num_str) for num_str in filter(None, cleaned_text.split(','))]

def validate_numbers(numbers: List[float]) -> List[float]:
    """Enhanced validation with range checking and truncation."""
    if len(numbers) < EXPECTED_NUMBERS:
        raise ValueError(
            f"API returned only {len(numbers)} numbers. Expected {EXPECTED_NUMBERS}."
        )
    
    # Validate number range
    invalid = [num for num in numbers if not (0 <= num <= 1)]
    if invalid:
        raise ValueError(f"Found {len(invalid)} numbers outside [0,1] range")
    
    return numbers[:EXPECTED_NUMBERS]

def plot_distribution(numbers: List[float]) -> None:
    """Optimized plotting with fixed figure size and style."""
    plt.figure(figsize=(10, 6))
    plt.hist(numbers, bins=100, density=True, edgecolor='black', alpha=0.8)
    plt.title(f"Uniform Distribution of {EXPECTED_NUMBERS} Random Numbers\n(Gemini AI Generated)")
    plt.xlabel("Value")
    plt.ylabel("Probability Density")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def main() -> None:
    """Main execution flow with error handling."""
    configure_gemini()
    
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(PROMPT)
        
        processed_numbers = validate_numbers(
            parse_numbers(clean_response(response.text))
        )
        
        plot_distribution(processed_numbers)
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    main()
   
