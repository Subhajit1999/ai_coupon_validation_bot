"""Input Handler Module
------------------
Handles validation and processing of user inputs.
"""

import logging
import re
from typing import Dict
from urllib.parse import urlparse

# Get logger
logger = logging.getLogger(__name__)


class InputHandler:
    """Handles validation and processing of user inputs."""
    
    def validate_inputs(self, coupon_code: str, website_url: str) -> bool:
        """
        Validate the coupon code and website URL inputs.
        
        Args:
            coupon_code: The coupon code to validate
            website_url: The website URL to validate
            
        Returns:
            True if inputs are valid, False otherwise
        """
        # Check for empty inputs
        if not coupon_code or not website_url:
            logger.error("Coupon code and website URL cannot be empty")
            return False
        
        # Validate coupon code length
        if len(coupon_code) < 2 or len(coupon_code) > 50:
            logger.error("Coupon code must be between 2 and 50 characters")
            return False
        
        # Validate website URL format
        parsed_url = urlparse(website_url)
        if not parsed_url.scheme or not parsed_url.netloc:
            logger.error("Invalid website URL format")
            return False
        
        return True
    
    def process_inputs(self, coupon_code: str, website_url: str) -> Dict:
        """
        Process and sanitize the coupon code and website URL inputs.
        
        Args:
            coupon_code: The coupon code to process
            website_url: The website URL to process
            
        Returns:
            Dictionary containing processed inputs
        """
        # Validate inputs first
        if not self.validate_inputs(coupon_code, website_url):
            raise ValueError("Invalid inputs")
        
        # Sanitize coupon code (trim whitespace)
        processed_coupon = coupon_code.strip()
        
        # Ensure website URL has proper scheme
        processed_url = website_url
        if not processed_url.startswith('http://') and not processed_url.startswith('https://'):
            processed_url = 'https://' + processed_url
        
        logger.info(f"Processed inputs: coupon='{processed_coupon}', url='{processed_url}'")
        
        return {
            'coupon_code': processed_coupon,
            'website_url': processed_url
        }