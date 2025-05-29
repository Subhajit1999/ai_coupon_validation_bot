#!/usr/bin/env python3

"""
Entry point script for the coupon validation bot.
This script provides a convenient way to run the bot from the command line.
"""

import asyncio
import argparse
from src.coupon_validator.main import validate_coupon


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Validate coupon codes on e-commerce websites")
    parser.add_argument("coupon_code", help="Coupon code to validate")
    parser.add_argument("website_url", help="Website URL to validate the coupon on")
    parser.add_argument("--headless", action="store_true", help="Run in headless mode")
    parser.add_argument("--output-dir", default="./output", help="Directory to save results to")
    parser.add_argument("--timeout", type=int, default=60000, help="Navigation timeout in milliseconds")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode with additional logging")
    
    return parser.parse_args()


async def main():
    """Main entry point."""
    args = parse_args()
    
    print(f"Validating coupon code '{args.coupon_code}' on {args.website_url}...")
    print(f"Headless mode: {'Enabled' if args.headless else 'Disabled'}")
    print(f"Output directory: {args.output_dir}")
    print(f"Timeout: {args.timeout}ms")
    print(f"Debug mode: {'Enabled' if args.debug else 'Disabled'}")
    
    result = await validate_coupon(
        coupon_code=args.coupon_code,
        website_url=args.website_url,
        headless=args.headless,
        output_dir=args.output_dir,
        timeout=args.timeout,
        debug=args.debug
    )
    
    print("\nValidation Result: [1]")
    print(f"Coupon Code: {result['coupon_code']}")
    print(f"Website: {result['website_url']}")
    print(f"Valid: {'Yes' if result['is_valid'] else 'No'}")
    print(f"Status: {result['status']}")
    # print(f"StackTrace: {result}")
    
    if 'error_message' in result and result['error_message']:
        print(f"Error: {result['error_message']}")
        
    if 'discount_amount' in result and result['discount_amount']:
        print(f"Discount Amount: {result['discount_amount']}")
        
    if 'screenshot_path' in result and result['screenshot_path']:
        print(f"Screenshot saved to: {result['screenshot_path']}")
        
    print(f"\nDetailed report saved to: {args.output_dir}")


if __name__ == "__main__":
    asyncio.run(main())