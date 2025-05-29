#!/usr/bin/env python3

"""
Test script for the coupon validation bot.
Tests the bot on sample e-commerce websites with test coupon codes.
"""

import asyncio
import sys
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('/tmp/coupon_validator_test.log')
    ]
)
logger = logging.getLogger(__name__)

# Import from the package
from src.coupon_validator.main import validate_coupon

# Test cases
TEST_CASES = [
    {
        'name': 'Demo Store',
        'coupon_code': 'FREESHIP',
        'website_url': 'https://demo.opencart.com/',
        'expected_result': None  # Unknown, will be determined during testing
    },
    {
        'name': 'Magento Demo Store',
        'coupon_code': 'DISCOUNT10',
        'website_url': 'https://magento.softwaretestingboard.com/',
        'expected_result': None  # Unknown, will be determined during testing
    }
]


async def run_tests():
    """Run all test cases and record results."""
    results = []
    
    for test_case in TEST_CASES:
        logger.info(f"Testing {test_case['name']} with coupon code {test_case['coupon_code']}")
        
        try:
            # Run test with headless browser for compatibility with sandbox environment
            result = await validate_coupon(
                coupon_code=test_case['coupon_code'],
                website_url=test_case['website_url'],
                headless=True  # Using headless mode for sandbox compatibility
            )
            
            # Record result
            test_result = {
                'test_case': test_case,
                'result': result,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'success': result.get('success', False)
            }
            
            results.append(test_result)
            
            # Log result
            if result.get('success', False):
                formatted_result = result.get('result', {})
                is_valid = formatted_result.get('is_valid', False)
                logger.info(f"Test completed. Coupon is {'valid' if is_valid else 'invalid'}")
            else:
                logger.error(f"Test failed: {result.get('error', 'Unknown error')}")
            
            # Wait between tests to avoid rate limiting
            await asyncio.sleep(2)
            
        except Exception as e:
            logger.error(f"Error running test case {test_case['name']}: {str(e)}")
            results.append({
                'test_case': test_case,
                'error': str(e),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'success': False
            })
    
    return results


async def main():
    """Main entry point for test script."""
    logger.info("Starting coupon validation bot tests")
    
    results = await run_tests()
    
    # Print summary
    print("\n" + "=" * 50)
    print("Coupon Validation Bot Test Results")
    print("=" * 50)
    
    for result in results:
        test_case = result['test_case']
        print(f"\nTest: {test_case['name']}")
        print(f"Coupon: {test_case['coupon_code']}")
        print(f"Website: {test_case['website_url']}")
        
        if result.get('success', False):
            formatted_result = result.get('result', {}).get('result', {})
            is_valid = formatted_result.get('is_valid', False)
            print(f"Result: {'✅ Valid' if is_valid else '❌ Invalid'}")
            
            if is_valid:
                if formatted_result.get('details', {}).get('success_message'):
                    print(f"Success Message: {formatted_result['details']['success_message']}")
                if formatted_result.get('details', {}).get('discount_amount'):
                    print(f"Discount Amount: {formatted_result['details']['discount_amount']}")
            else:
                if formatted_result.get('details', {}).get('error_message'):
                    print(f"Error Message: {formatted_result['details']['error_message']}")
        else:
            print(f"Result: ❌ Test Failed")
            print(f"Error: {result.get('error', 'Unknown error')}")
    
    print("\n" + "=" * 50)
    logger.info("Coupon validation bot tests completed")


if __name__ == "__main__":
    asyncio.run(main())
