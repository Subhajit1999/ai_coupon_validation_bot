"""Result Reporter Module
----------------------
Handles formatting and reporting validation results.
"""

import json
import logging
import os
from datetime import datetime
from typing import Dict, Optional

# Get logger
logger = logging.getLogger(__name__)


class ResultReporter:
    """Handles formatting and reporting validation results."""
    
    def __init__(self, output_dir: str = './output'):
        """
        Initialize the result reporter.
        
        Args:
            output_dir: Directory to save results to
        """
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            logger.info(f"Created output directory: {output_dir}")
    
    def format_result(self, coupon_code: str, website_url: str, is_valid: bool, 
                      status_message: str, error_message: Optional[str] = None,
                      discount_amount: Optional[str] = None, screenshot_path: Optional[str] = None) -> Dict:
        """
        Format the validation result.
        
        Args:
            coupon_code: The coupon code that was validated
            website_url: The website URL where validation was attempted
            is_valid: Whether the coupon code is valid
            status_message: Status message describing the result
            error_message: Error message if validation failed
            discount_amount: Amount of discount if coupon is valid
            screenshot_path: Path to screenshot of validation result
            
        Returns:
            Dictionary containing formatted result
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        result = {
            "coupon_code": coupon_code,
            "website_url": website_url,
            "timestamp": timestamp,
            "is_valid": is_valid,
            "status": status_message
        }
        
        if error_message:
            result["error_message"] = error_message
            
        if discount_amount:
            result["discount_amount"] = discount_amount
            
        if screenshot_path:
            result["screenshot_path"] = screenshot_path
            
        return result
    
    def save_result(self, result: Dict) -> str:
        """
        Save the formatted result to a file.
        
        Args:
            result: Formatted result dictionary
            
        Returns:
            Path to saved result file
        """
        try:
            # Create a unique filename based on timestamp and coupon code
            timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            coupon_code = result.get("coupon_code", "unknown").replace(" ", "_")
            filename = f"{timestamp_str}_{coupon_code}.json"
            file_path = os.path.join(self.output_dir, filename)
            
            # Save result as JSON
            with open(file_path, 'w') as f:
                json.dump(result, f, indent=4)
                
            logger.info(f"Saved result to {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Error saving result: {str(e)}")
            return ""
    
    def generate_report(self, result: Dict) -> str:
        """
        Generate a human-readable report from the result.
        
        Args:
            result: Formatted result dictionary
            
        Returns:
            Path to saved report file
        """
        try:
            # Extract details from result
            coupon_code = result.get("coupon_code", "unknown")
            website_url = result.get("website_url", "unknown")
            timestamp = result.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            is_valid = result.get("is_valid", False)
            status = result.get("status", "")
            error_message = result.get("error_message", "")
            discount_amount = result.get("discount_amount", "")
            
            # Create report content
            report_content = [
                "Coupon Validation Report",
                "=======================",
                "",
                f"Coupon Code: {coupon_code}",
                f"Website: {website_url}",
                f"Timestamp: {timestamp}",
                f"Valid: {'Yes' if is_valid else 'No'}",
                f"Status: {status}"
            ]
            
            if error_message:
                report_content.append(f"Error: {error_message}")
                
            if discount_amount:
                report_content.append(f"Discount Amount: {discount_amount}")
                
            if "screenshot_path" in result:
                report_content.append(f"Screenshot: {result['screenshot_path']}")
                
            # Create a unique filename for the report
            timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            coupon_code_clean = coupon_code.replace(" ", "_")
            filename = f"{timestamp_str}_{coupon_code_clean}_report.txt"
            file_path = os.path.join(self.output_dir, filename)
            
            # Save report to file
            with open(file_path, 'w') as f:
                f.write("\n".join(report_content))
                
            logger.info(f"Generated report at {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
            return ""
