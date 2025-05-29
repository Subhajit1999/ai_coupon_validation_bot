"""Magento Coupon Handler Module
--------------------------
Specialized handler for Magento e-commerce platform coupon application.
"""

import logging
import os
from typing import Dict, Optional

# Get logger
logger = logging.getLogger(__name__)


class MagentoCouponHandler:
    """Specialized handler for Magento e-commerce platform coupon application."""
    
    async def find_and_expand_coupon_section(self, browser_engine) -> bool:
        """
        Find and expand the coupon code section in Magento checkout.
        
        Args:
            browser_engine: The browser engine instance
            
        Returns:
            True if coupon section was found and expanded, False otherwise
        """
        try:
            # Get current URL to determine if we're on cart or checkout
            current_url = await browser_engine.get_current_url()
            if not current_url:
                logger.error("Could not determine current URL")
                return False
            
            # Determine if we're on cart or checkout page
            is_cart = 'cart' in current_url.lower()
            is_checkout = 'checkout' in current_url.lower() or 'onepage' in current_url.lower()
            
            # If we're not on checkout, try to navigate there
            if not is_checkout:
                logger.info("Not on checkout page, attempting to navigate")
                
                # Try to click proceed to checkout buttons
                checkout_selectors = [
                    '#top-cart-btn-checkout',
                    '.action.primary.checkout',
                    'button.checkout',
                    '.checkout-methods-items .action.primary.checkout',
                    '.checkout-methods button.btn-proceed-checkout',
                    '#maincontent .action.primary.checkout'
                ]
                
                for selector in checkout_selectors:
                    if await browser_engine.is_visible(selector):
                        if await browser_engine.click(selector):
                            logger.info(f"Clicked checkout button: {selector}")
                            await browser_engine.wait_for_navigation()
                            break
                
                # If clicking buttons didn't work, try JavaScript navigation
                current_url = await browser_engine.get_current_url()
                is_checkout = 'checkout' in current_url.lower() or 'onepage' in current_url.lower()
                
                if not is_checkout:
                    logger.info("Trying JavaScript navigation to checkout")
                    js_result = await browser_engine.execute_javascript("""
                        // Try to find checkout URLs
                        const checkoutLinks = Array.from(document.querySelectorAll('a')).filter(a => {
                            const href = (a.href || '').toLowerCase();
                            return href.includes('checkout') || href.includes('onepage');
                        });
                        
                        if (checkoutLinks.length > 0) {
                            window.location.href = checkoutLinks[0].href;
                            return true;
                        }
                        
                        return false;
                    """)
                    
                    if js_result:
                        logger.info("Used JavaScript to navigate to checkout")
                        await browser_engine.wait_for_navigation()
            
            # Take screenshot for debugging
            await browser_engine.take_screenshot('/tmp/magento_before_coupon_section.png')
            
            # Get the full HTML content for analysis
            html_content = await browser_engine.get_html_content()
            
            # Save the HTML content to a file for offline analysis
            if html_content:
                # Determine filename based on URL stage
                filename = '/tmp/magento_cart_dom.html'
                if 'checkout' in current_url.lower():
                    filename = '/tmp/magento_checkout_dom.html'
                if 'payment' in current_url.lower():
                    filename = '/tmp/magento_payment_dom.html'
                
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                logger.info(f"Saved HTML content to {filename}")
            
            # For Magento, we may need to navigate to the payment step
            # Try to click on next/continue buttons to get to payment step
            continue_selectors = [
                '.button.action.continue',
                'button.continue',
                'button:has-text("Next")',
                'button:has-text("Continue")',
                'button.action.continue',
                'button[data-role="opc-continue"]',
                '.action.primary.continue',
                '#shipping-method-buttons-container .action.primary',
                '#shipping-method-buttons-container button'
            ]
            
            for selector in continue_selectors:
                if await browser_engine.is_visible(selector):
                    if await browser_engine.click(selector):
                        logger.info(f"Clicked continue button: {selector}")
                        await browser_engine.wait_for_navigation()
                        break
            
            # Now try to find and click the coupon code toggle/expansion element
            coupon_toggle_selectors = [
                '#block-discount-heading',
                '.payment-option-title:has-text("Apply Discount Code")',
                '.payment-option._collapsible:has-text("Apply Discount Code")',
                '.payment-option._collapsible.opc-payment-additional',
                '#opc-payment-method-additional-load .payment-option-title',
                '.discount-code .title',
                '.discount-code .coupon-code-title',
                '.discount-form .title',
                '.discount-form .coupon-code-title',
                'div:has-text("Apply Discount Code")',
                'span:has-text("Apply Discount Code")',
                'div:has-text("Enter coupon code")',
                'span:has-text("Enter coupon code")'
            ]
            
            for selector in coupon_toggle_selectors:
                if await browser_engine.is_visible(selector):
                    if await browser_engine.click(selector):
                        logger.info(f"Clicked coupon toggle: {selector}")
                        # Wait a moment for the coupon field to appear
                        await browser_engine.page.wait_for_timeout(1000)
                        return True
            
            # If no toggle element was found, try using JavaScript to show the coupon section
            js_result = await browser_engine.execute_javascript("""
                // Try to find and click any coupon code toggle elements
                const couponToggles = Array.from(document.querySelectorAll('*')).filter(el => {
                    const text = (el.textContent || '').toLowerCase();
                    return text.includes('coupon') || 
                           text.includes('discount code') || 
                           text.includes('promo code');
                });
                
                if (couponToggles.length > 0) {
                    couponToggles[0].click();
                    return true;
                }
                
                // Try to find any collapsed elements that might contain coupon fields
                const collapsedElements = Array.from(document.querySelectorAll('.payment-option._collapsible:not(._active), .discount-code:not(._active), .coupon-code:not(._active)'));
                
                if (collapsedElements.length > 0) {
                    collapsedElements[0].click();
                    return true;
                }
                
                return false;
            """)
            
            if js_result:
                logger.info("Used JavaScript to expand coupon section")
                # Wait a moment for the coupon field to appear
                await browser_engine.page.wait_for_timeout(1000)
                return True
            
            # If we couldn't find a specific coupon toggle, assume it's already visible
            logger.info("Could not find coupon toggle, assuming coupon field is already visible")
            return True
            
        except Exception as e:
            logger.error(f"Error finding and expanding coupon section: {str(e)}")
            return False