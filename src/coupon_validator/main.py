"""Main Module
-----------
Main entry point for the coupon validation bot with AI-enhanced website structure detection.
"""

import asyncio
import logging
import os
from datetime import datetime
from typing import Dict, Optional, Tuple

from .browser_engine import BrowserEngine
from .input_handler import InputHandler
from .website_pattern_recognizer import WebsitePatternRecognizer
from .product_selector import ProductSelector
from .cart_navigator import CartNavigator
from .coupon_applicator import CouponApplicator
from .result_reporter import ResultReporter
from .magento_coupon_handler import MagentoCouponHandler
from .ai_website_analyzer import AIWebsiteAnalyzer

# Configure root logger for the entire application
def configure_logging(debug=False):
    """Configure logging for the entire application."""
    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        force=True  # Override any existing configuration
    )

# Set default logging level
configure_logging()
logger = logging.getLogger(__name__)


async def validate_coupon(coupon_code: str, website_url: str, headless: bool = False, 
                         output_dir: str = './output', timeout: int = 60000, debug: bool = False) -> Dict:
    """
    Validate a coupon code on a website.
    
    Args:
        coupon_code: The coupon code to validate
        website_url: The website URL to validate the coupon on
        headless: Whether to run the browser in headless mode
        output_dir: Directory to save results to
        
    Returns:
        Dictionary containing validation result
    """
    # Configure logging based on debug parameter
    configure_logging(debug)
    
    # Initialize components
    input_handler = InputHandler()
    
    try:
        # Input validation
        input_handler.validate_inputs(coupon_code, website_url)
        
        # Initialize components
        browser_engine = BrowserEngine(headless=headless)
        website_recognizer = WebsitePatternRecognizer()
        ai_analyzer = AIWebsiteAnalyzer()
        product_selector = ProductSelector()
        cart_navigator = CartNavigator()
        coupon_applicator = CouponApplicator()
        result_reporter = ResultReporter(output_dir=output_dir)
        
        # Create a MagentoCouponHandler instance
        from .magento_coupon_handler import MagentoCouponHandler
        magento_handler = MagentoCouponHandler()
        
        # Initialize screenshot path variable
        screenshot_path = None
        
        # Start browser and navigate to website
        await browser_engine.start()
        
        # Navigate to the website with retry mechanism
        logger.info(f"Navigating to {website_url}")
        navigation_success = False
        navigation_errors = []
        
        # Try different navigation strategies
        strategies = [
            {'wait_until': 'networkidle', 'timeout': timeout},
            {'wait_until': 'domcontentloaded', 'timeout': timeout},
            {'wait_until': 'load', 'timeout': timeout}
        ]
        
        for strategy in strategies:
            if navigation_success:
                break
                
            try:
                logger.info(f"Trying navigation with strategy: {strategy['wait_until']}")
                navigation_success = await browser_engine.navigate(website_url, wait_until=strategy['wait_until'], timeout=strategy['timeout'])
                
                if navigation_success:
                    logger.info(f"Navigation successful with strategy: {strategy['wait_until']}")
                else:
                    logger.warning(f"Navigation failed with strategy: {strategy['wait_until']}")
                    navigation_errors.append(f"Navigation failed with strategy: {strategy['wait_until']}")
                    
            except Exception as e:
                error_msg = f"Navigation failed with strategy {strategy['wait_until']}: {str(e)}"
                logger.warning(error_msg)
                navigation_errors.append(error_msg)
        
        if not navigation_success:
            return result_reporter.format_result(
                coupon_code=coupon_code,
                website_url=website_url,
                is_valid=False,
                status_message="Navigation failed",
                error_message=f"Failed to navigate to the website after multiple attempts: {'; '.join(navigation_errors)}"
            )
        
        # Identify platform using traditional pattern recognition
        platform_info = await website_recognizer.identify_platform(browser_engine)
        logger.info(f"Identified platform: {platform_info['platform']}")
        
        # Enhance detection with AI analysis
        try:
            logger.info("Enhancing detection with AI analysis...")
            ai_analysis = await ai_analyzer.analyze_website_structure(browser_engine)
            
            # If AI detected elements with high confidence, add them to platform_info
            if 'detected_elements' in ai_analysis and ai_analysis['detected_elements']:
                logger.info(f"AI detected {len(ai_analysis['detected_elements'])} elements")
                
                # For each element type that AI detected
                for element_type, element in ai_analysis['detected_elements'].items():
                    # If this element type exists in platform_info but doesn't have selectors
                    if element_type in platform_info and not platform_info[element_type]:
                        # Generate selectors for this element
                        ai_selectors = await ai_analyzer.get_element_selectors(browser_engine, element_type)
                        if ai_selectors:
                            logger.info(f"Adding AI-generated selectors for {element_type}")
                            # Add AI-generated selectors to the beginning of the list for priority
                            if element_type in platform_info:
                                platform_info[element_type] = ai_selectors + platform_info[element_type]
                            else:
                                platform_info[element_type] = ai_selectors
                
                # Add AI confidence scores to platform info
                platform_info['ai_confidence_scores'] = ai_analysis['confidence_scores']
        except Exception as ai_error:
            logger.warning(f"AI analysis failed: {str(ai_error)}. Continuing with traditional detection.")
            # Continue with traditional detection only
        
        # Select a product
        product_result = await product_selector.find_and_select_product(browser_engine, platform_info)
        if not product_result['success']:
            return result_reporter.format_result(
                coupon_code=coupon_code,
                website_url=website_url,
                is_valid=False,
                status_message="Product selection failed",
                error_message=product_result['error']
            )
        
        # Add product to cart
        cart_result = await product_selector.add_to_cart(browser_engine, platform_info)
        if not cart_result['success']:
            return result_reporter.format_result(
                coupon_code=coupon_code,
                website_url=website_url,
                is_valid=False,
                status_message="Adding to cart failed",
                error_message=cart_result['error']
            )
        
        # Navigate to checkout
        checkout_result = await cart_navigator.navigate_to_checkout(browser_engine, platform_info)
        if not checkout_result['success']:
            return result_reporter.format_result(
                coupon_code=coupon_code,
                website_url=website_url,
                is_valid=False,
                status_message="Checkout navigation failed",
                error_message=checkout_result['error']
            )
        
        # Special handling for Magento sites
        if platform_info['platform'] == 'magento':
            magento_success = await magento_handler.find_and_expand_coupon_section(browser_engine)
            if not magento_success:
                logger.warning("Magento-specific handling failed")
                # Continue with generic approach
        
        # Apply coupon code
        coupon_result = await coupon_applicator.apply_coupon(browser_engine, platform_info, coupon_code)
        
        # Take screenshot of result
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_filename = f"{timestamp_str}_{coupon_code}_result.png"
        screenshot_path = os.path.join(output_dir, screenshot_filename)
        await browser_engine.take_screenshot(screenshot_path)
        
        # Check if coupon application was successful
        if not coupon_result.get('success', False):
            # Handle error in coupon application
            return result_reporter.format_result(
                coupon_code=coupon_code,
                website_url=website_url,
                is_valid=False,
                status_message="Coupon application failed",
                error_message=coupon_result.get('error', 'Unknown error'),
                screenshot_path=screenshot_path
            )
        
        # Format and return result
        result = result_reporter.format_result(
            coupon_code=coupon_code,
            website_url=website_url,
            is_valid=coupon_result.get('is_valid', False),
            status_message="Coupon validation complete",
            error_message=coupon_result.get('error_message'),
            discount_amount=coupon_result.get('discount_amount'),
            screenshot_path=screenshot_path
        )
        
        # Save result to file
        try:
            result_file = result_reporter.save_result(result)
            logger.info(f"Result saved to {result_file}")
            
            # Generate human-readable report
            report_file = result_reporter.generate_report(result)
            logger.info(f"Report generated at {report_file}")
        except Exception as save_error:
            logger.error(f"Failed to save result: {str(save_error)}")
            
        print("validation success")
        return result
        
    except Exception as e:
        logger.error(f"Validation error: {str(e)}")
        # Create a result reporter if it doesn't exist
        if 'result_reporter' not in locals():
            result_reporter = ResultReporter(output_dir=output_dir)
            
        # Format the error result
        result = result_reporter.format_result(
            coupon_code=coupon_code,
            website_url=website_url,
            is_valid=False,
            status_message="Validation error",
            error_message=str(e),
            screenshot_path=screenshot_path if 'screenshot_path' in locals() else None
        )
        
        # Save the error result
        try:
            result_file = result_reporter.save_result(result)
            logger.info(f"Error result saved to {result_file}")
            
            report_file = result_reporter.generate_report(result)
            logger.info(f"Error report generated at {report_file}")
        except Exception as save_error:
            logger.error(f"Failed to save error result: {str(save_error)}")
            
        print("error in validation")
        return result
        
    finally:
        # Always close the browser
        if browser_engine:
            await browser_engine.close()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Validate coupon codes on e-commerce websites")
    parser.add_argument("coupon_code", help="Coupon code to validate")
    parser.add_argument("website_url", help="Website URL to validate the coupon on")
    parser.add_argument("--headless", action="store_true", help="Run in headless mode")
    parser.add_argument("--output-dir", default="./output", help="Directory to save results to")
    parser.add_argument("--timeout", type=int, default=60000, help="Navigation timeout in milliseconds")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode with additional logging")
    
    args = parser.parse_args()
    
    # Set debug logging if requested
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    result = asyncio.run(validate_coupon(
        coupon_code=args.coupon_code,
        website_url=args.website_url,
        headless=args.headless,
        output_dir=args.output_dir,
        timeout=args.timeout
    ))
    
    print("\nValidation Result: [3]")
    print(f"Coupon Code: {result['coupon_code']}")
    print(f"Website: {result['website_url']}")
    print(f"Valid: {'Yes' if result['is_valid'] else 'No'}")
    print(f"Status: {result['status']}")
    
    if 'error_message' in result and result['error_message']:
        print(f"Error: {result['error_message']}")
        
    if 'discount_amount' in result and result['discount_amount']:
        print(f"Discount Amount: {result['discount_amount']}")
        
    if 'screenshot_path' in result and result['screenshot_path']:
        print(f"Screenshot saved to: {result['screenshot_path']}")
        
    print(f"\nDetailed report saved to: {args.output_dir}")