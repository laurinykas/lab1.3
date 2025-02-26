# -*- coding: utf-8 -*-
"""LLM 1.2.2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ZSkfpphGeXOh6UZJrEqY3l78zBqm2c90
"""

# Import required libraries
import google.generativeai as genai  # For accessing Google's Gemini AI
import matplotlib.pyplot as plt      # For data visualization
import numpy as np                   # For numerical operations (not directly used in current implementation)
from google.colab import userdata    # For accessing Colab user secrets

# Configure Gemini AI with API key from Colab secrets
genai.configure(api_key=userdata.get('GOOGLE_API_KEY'))

def clean_response(response_text):
    """Clean AI response to extract only numerical values.
    Removes all characters except digits, commas, and dots."""
    allowed_chars = {'.', ','}
    cleaned_text = ""
    # Iterate through each character in response
    for c in response_text:
        # Keep only digits and allowed punctuation
        if c.isdigit() or c in allowed_chars:
            cleaned_text += c
    return cleaned_text

def parse_numbers(cleaned_text):
    """Convert cleaned comma-separated string to list of floats."""
    numbers = []
    # Split text by commas and convert to float values
    for num in cleaned_text.split(','):
        if num:  # Skip empty strings from potential double commas
            numbers.append(float(num))
    return numbers

# Prompt for generating random numbers (specific format request)
prompt = """Generate 1000 random numbers uniformly distributed between 0 and 1. 
Return them as a single line of numbers separated by commas, 
without writing any code, give full 1000."""

# Generate response from Gemini Flash model
model = genai.GenerativeModel("gemini-2.0-flash")
response = model.generate_content(prompt)

# Clean and parse the AI response
cleaned_text = clean_response(response.text)
random_numbers = parse_numbers(cleaned_text)

# Validate and adjust number count
size = len(random_numbers)
fac = size - 1000
# Truncate if we got more than 1000 numbers (common with LLM outputs)
if size > 1000:
    random_numbers = random_numbers[:-fac]  # Remove excess from end

# Note: This code doesn't handle cases where we get fewer than 1000 numbers

# Create visualization of distribution
plt.hist(random_numbers, bins=100, edgecolor='black', alpha=0.8)
plt.title("Uniform Distribution of 1000 Random Numbers")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.grid(True)
plt.show()  # Added to ensure plot displays in non-notebook environments
