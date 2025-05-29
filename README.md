<<<<<<< HEAD
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
=======
# AI Coupon Validation Bot

An advanced Python-based bot that automatically validates coupon codes on e-commerce websites using AI-enhanced website structure detection.

## Features

- **AI-Enhanced Website Analysis**: Uses DistilBERT to detect website elements and structure
- **Multi-Platform Support**: Works with Shopify, Magento, WooCommerce, and generic e-commerce sites
- **Automated Navigation**: Automatically navigates websites, selects products, and applies coupons
- **Smart Element Detection**: AI-powered detection of cart buttons, coupon inputs, and pricing elements
- **Comprehensive Reporting**: Generates detailed JSON reports and human-readable summaries
- **Screenshot Evidence**: Captures screenshots for validation evidence
- **Error Handling**: Robust error handling with fallback strategies

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/Subhajit1999/ai_coupon_validation_bot.git
cd ai_coupon_validation_bot
```

2. **Create virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Install Playwright browsers**
```bash
python -m playwright install
>>>>>>> a5576d4 (changed the code)
```

## Usage

<<<<<<< HEAD
### Command Line
=======
### Command Line Usage
>>>>>>> a5576d4 (changed the code)

```bash
# Basic usage
python -m src.coupon_validator.main "COUPON10" "https://example-store.com"

# With options
python -m src.coupon_validator.main "FREESHIP" "https://example-store.com" --headless --output-dir ./results
```

<<<<<<< HEAD
### Test Script

Use the test script to run a demonstration of the AI-enhanced validation:

```bash
python test_ai_validation.py COUPON_CODE WEBSITE_URL [--headless] [--output-dir OUTPUT_DIR]
```

### As a Library
=======
### Python API Usage
>>>>>>> a5576d4 (changed the code)

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
<<<<<<< HEAD
    print(f"Coupon valid: {result['is_valid']}")
    if result['is_valid']:
        print(f"Discount amount: {result.get('discount_amount', 'Unknown')}")
=======
    
    print(f"Coupon valid: {result['is_valid']}")
    if result['is_valid']:
        print(f"Discount amount: ${result.get('discount_amount', 'Unknown')}")
>>>>>>> a5576d4 (changed the code)

# Run the async function
asyncio.run(main())
```

<<<<<<< HEAD
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
=======
### Testing

Use the test script to run demonstrations:

```bash
# Test with specific coupon and website
python test_ai_validation.py COUPON_CODE WEBSITE_URL [--headless] [--output-dir OUTPUT_DIR]

# Run all predefined tests
python test_ai_validation.py
```

## Project Structure

```
ai_coupon_validation_bot/
├── src/
│   └── coupon_validator/
│       ├── __init__.py
│       ├── ai_website_analyzer.py    # AI-based website analysis
│       ├── browser_engine.py         # Browser automation
│       ├── cart_navigator.py         # Cart navigation logic
│       ├── coupon_applicator.py      # Coupon application logic
│       ├── product_selector.py       # Product selection logic
│       ├── result_reporter.py        # Report generation
│       └── main.py                   # Main validation logic
├── tests/
│   ├── __init__.py
│   └── test_coupon_validator.py
├── test_ai_validation.py             # Test script
├── requirements.txt
├── setup.py
└── README.md
```

## How It Works

### AI-Enhanced Analysis

The bot uses a pre-trained DistilBERT model to enhance traditional pattern recognition:

1. **Embedding Generation**: Creates embeddings for common e-commerce elements
2. **Content Analysis**: Analyzes HTML content to extract potential elements
3. **Similarity Scoring**: Scores elements based on similarity to known patterns
4. **Selector Generation**: Generates CSS selectors for high-confidence matches

### Validation Process

1. **Website Navigation**: Opens the target e-commerce website
2. **AI Analysis**: Analyzes page structure and detects platform type
3. **Product Selection**: Finds and selects a product to add to cart
4. **Cart Navigation**: Navigates to the shopping cart page
5. **Coupon Application**: Applies the coupon code and detects results
6. **Result Analysis**: Determines if the coupon is valid and extracts discount information
7. **Report Generation**: Creates detailed reports with screenshots

## Supported Platforms

- **Shopify**: Full support with platform-specific optimizations
- **Magento**: Advanced support for Magento-specific elements
- **WooCommerce**: WordPress/WooCommerce integration
- **OpenCart**: Support for OpenCart stores
- **Generic**: Fallback support for custom e-commerce implementations

## Testing

Run the test suite:
>>>>>>> a5576d4 (changed the code)

```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/test_coupon_validator.py
<<<<<<< HEAD
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
=======

# Run with verbose output
python -m pytest -v
```

## Configuration

The bot can be configured through environment variables or by modifying the configuration in the source files:

- **Browser Settings**: Headless mode, viewport size, timeouts
- **AI Model Settings**: Model selection, confidence thresholds
- **Output Settings**: Report format, screenshot settings
- **Platform Settings**: Platform-specific selectors and logic

## Troubleshooting

### Common Issues

1. **Browser Installation**: Make sure Playwright browsers are installed
2. **Model Loading**: Ensure internet connection for downloading AI models
3. **Website Compatibility**: Some websites may have anti-bot measures
4. **Element Detection**: Websites with custom implementations may require tweaking

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is for educational and testing purposes only. Always respect website terms of service and rate limits. Use responsibly and in accordance with applicable laws and regulations.
>>>>>>> a5576d4 (changed the code)
