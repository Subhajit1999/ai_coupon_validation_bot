# AI-Enhanced Coupon Validator Bot

A Python-based bot for automatically validating coupon codes on e-commerce websites, now enhanced with AI-based website structure detection.

## Features

- **AI-Enhanced Website Analysis**: Uses machine learning to detect website elements and structure
- Automatically navigates e-commerce websites
- Detects platform type (Magento, WooCommerce, Shopify, etc.)
- Selects products and adds them to cart
- Applies coupon codes at checkout
- Detects validation results (success/error messages)
- Extracts discount amounts
- Generates detailed reports

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ai_validation_bot.git
cd ai_validation_bot

# Create and activate a virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
python -m playwright install

# Download AI models (if not included)
mkdir -p models
# The models will be downloaded automatically on first run
```

## Usage

### Command Line

```bash
# Basic usage
python -m src.coupon_validator.main "COUPON10" "https://example-store.com"

# With options
python -m src.coupon_validator.main "FREESHIP" "https://example-store.com" --headless --output-dir ./results
```

### Test Script

Use the test script to run a demonstration of the AI-enhanced validation:

```bash
python test_ai_validation.py COUPON_CODE WEBSITE_URL [--headless] [--output-dir OUTPUT_DIR]
```

### As a Library

```python
import asyncio
from src.coupon_validator.main import validate_coupon

async def main():
    result = await validate_coupon(
        coupon_code="DISCOUNT20",
        website_url="https://example-store.com",
        headless=True,
        output_dir="./results"
    )
    print(f"Coupon valid: {result['is_valid']}")
    if result['is_valid']:
        print(f"Discount amount: {result.get('discount_amount', 'Unknown')}")

# Run the async function
asyncio.run(main())
```

## Project Structure

```
ai_validation_bot/
├── src/
│   ├── coupon_validator/
│   │   ├── __init__.py
│   │   ├── ai_website_analyzer.py    # New AI-based analyzer
│   │   ├── browser_engine.py
│   │   ├── cart_navigator.py
│   │   ├── coupon_applicator.py
│   │   ├── input_handler.py
│   │   ├── magento_coupon_handler.py
│   │   ├── main.py
│   │   ├── product_selector.py
│   │   ├── result_reporter.py
│   │   └── website_pattern_recognizer.py
│   └── __init__.py
├── models/                           # Directory for AI models
│   └── README.md
├── tests/
│   ├── __init__.py
│   └── test_coupon_validator.py
├── test_ai_validation.py             # AI validation test script
├── README.md
├── requirements.txt
└── setup.py
```

## Running Tests

```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/test_coupon_validator.py
```

## AI-Enhanced Detection

The tool uses a pre-trained DistilBERT model to enhance traditional pattern recognition:

- Generates embeddings for common e-commerce elements
- Analyzes HTML content to extract potential elements
- Scores elements based on similarity to known patterns
- Generates CSS selectors for high-confidence matches

This AI enhancement improves detection accuracy, especially on non-standard or custom e-commerce implementations.

## License

<<<<<<< HEAD
MIT
=======
MIT# ai_coupon_validation_bot
>>>>>>> 622d291 (first commit)
