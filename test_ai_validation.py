#!/usr/bin/env python3
"""
Test script for AI Coupon Validation Bot
"""

import asyncio
import sys
import argparse
from src.coupon_validator.main import validate_coupon

async def test_validation():
    """Test the coupon validation system"""
    
    # Test cases
    test_cases = [
        {
            'coupon_code': 'TEST10',
            'website_url': 'https://demo.opencart.com/',
            'description': 'OpenCart Demo Store'
        },
        {
            'coupon_code': 'SAVE20',
            'website_url': 'https://magento2-demo.nexcess.net/',
            'description': 'Magento Demo Store'
        }
    ]
    
    print("Starting AI Coupon Validation Tests...")
    print("="*60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['description']}")
        print(f"Coupon: {test_case['coupon_code']}")
        print(f"URL: {test_case['website_url']}")
        print("-" * 40)
        
        try:
            result = await validate_coupon(
                coupon_code=test_case['coupon_code'],
                website_url=test_case['website_url'],
                headless=True,
                output_dir=f"./test_results/test_{i}"
            )
            
            # Print results
            print(f"Platform Detected: {result['platform']}")
            print(f"Validation Result: {'✓ VALID' if result['is_valid'] else '✗ INVALID'}")
            
            if result['message']:
                print(f"Message: {result['message']}")
            
            if result['discount_amount']:
                print(f"Discount Amount: ${result['discount_amount']:.2f}")
            
            print(f"Steps Completed: {sum(1 for step in result['execution_steps'] if step['success'])}/{len(result['execution_steps'])}")
            
            if result['error']:
                print(f"Error: {result['error']}")
            
        except Exception as e:
            print(f"Test failed with error: {e}")
        
        print("-" * 40)
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Test AI Coupon Validation Bot')
    parser.add_argument('coupon_code', nargs='?', help='Specific coupon code to test')
    parser.add_argument('website_url', nargs='?', help='Specific website URL to test')
    parser.add_argument('--headless', action='store_true', default=True,
                       help='Run browser in headless mode')
    parser.add_argument('--output-dir', default='./test_results',
                       help='Output directory for test results')
    
    args = parser.parse_args()
    
    if args.coupon_code and args.website_url:
        # Single test mode
        print(f"Testing coupon '{args.coupon_code}' on '{args.website_url}'")
        result = asyncio.run(validate_coupon(
            args.coupon_code,
            args.website_url,
            args.headless,
            args.output_dir
        ))
        
        print("\nTest Results:")
        print(f"Valid: {'✓ YES' if result['is_valid'] else '✗ NO'}")
        if result['message']:
            print(f"Message: {result['message']}")
        if result['discount_amount']:
            print(f"Discount: ${result['discount_amount']:.2f}")
    else:
        # Run all tests
        asyncio.run(test_validation())