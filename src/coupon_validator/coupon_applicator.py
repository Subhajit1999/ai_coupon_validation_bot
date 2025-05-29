"""Coupon Applicator Module
-----------------------
Handles the application of coupon codes on e-commerce websites.
Enhanced with AI-based element detection for improved accuracy.
"""

import logging
import re
from typing import Dict, Optional, List

# Get logger
logger = logging.getLogger(__name__)


class CouponApplicator:
    """Handles the application of coupon codes and detection of validation results."""
    
    async def apply_coupon(self, browser_engine, platform_info: Dict, coupon_code: str) -> Dict:
        """
        Apply a coupon code and detect validation result.
        
        Args:
            browser_engine: The browser engine instance
            platform_info: Information about the website platform
            coupon_code: The coupon code to apply
            
        Returns:
            Dictionary with success status, validation result, and any error message
        """
        try:
            # Take screenshot before applying coupon
            await browser_engine.take_screenshot('/tmp/before_coupon_application.png')
            
            # Handle platform-specific logic
            if platform_info and 'platform' in platform_info and platform_info['platform'] == 'magento':
                from .magento_coupon_handler import MagentoCouponHandler
                magento_handler = MagentoCouponHandler()
                await magento_handler.find_and_expand_coupon_section(browser_engine)
                
            # Handle platform-specific logic for Skullcandy
            if platform_info and 'platform' in platform_info and platform_info['platform'] == 'skullcandy':
                from .skullcandy_coupon_handler import SkullcandyCouponHandler
                skullcandy_handler = SkullcandyCouponHandler()
                await skullcandy_handler.find_and_expand_coupon_section(browser_engine)
            
            # Check if we have AI-detected elements with high confidence
            ai_confidence_threshold = 0.8
            has_ai_detection = False
            
            if 'ai_confidence_scores' in platform_info and 'coupon_field' in platform_info['ai_confidence_scores']:
                if platform_info['ai_confidence_scores']['coupon_field'] > ai_confidence_threshold:
                    has_ai_detection = True
                    logger.info(f"Using AI-detected coupon field with confidence: {platform_info['ai_confidence_scores']['coupon_field']}")
            
            # Try to find coupon input field using platform-provided selectors
            coupon_field_found = False
            if platform_info and 'platform' in platform_info and platform_info['platform'] != 'unknown':
                if 'coupon_field' in platform_info and platform_info['coupon_field']:
                    for selector in platform_info['coupon_field']:
                        if await browser_engine.is_visible(selector):
                            await browser_engine.fill(selector, coupon_code)
                            logger.info(f"Filled coupon field with {'AI-enhanced' if has_ai_detection else 'platform-specific'} selector: {selector}")
                            coupon_field_found = True
                            break
            
            # If platform-specific selectors didn't work, try common selectors
            if not coupon_field_found:
                # First, try to click on "Have a coupon?" links to reveal the input field
                coupon_toggle_selectors = [
                    'a:has-text("coupon")',
                    'span:has-text("coupon")',
                    'div:has-text("coupon")',
                    '.showcoupon',
                    '#block-discount-heading',
                    '.payment-option-title:has-text("Apply Discount Code")',
                    '.coupon-trigger',
                    '.coupon-code-trigger',
                    '.discount-trigger',
                    '.promo-trigger'
                ]
                
                for selector in coupon_toggle_selectors:
                    if await browser_engine.is_visible(selector):
                        await browser_engine.click(selector)
                        logger.info(f"Clicked coupon toggle: {selector}")
                        # Wait a moment for the coupon field to appear
                        await browser_engine.page.wait_for_timeout(1000)
                        break
                
                # Now try to find the coupon input field
                coupon_field_selectors = [
                    'input[name="coupon_code"]',
                    'input[id="coupon_code"]',
                    'input[name*="coupon"]',
                    'input[id*="coupon"]',
                    'input[placeholder*="coupon"]',
                    'input[placeholder*="Coupon"]',
                    'input[placeholder*="promo"]',
                    'input[placeholder*="Promo"]',
                    'input[placeholder*="discount"]',
                    'input[placeholder*="Discount"]',
                    'input[name="discount_code"]',
                    'input[id="discount_code"]',
                    'input[name*="discount"]',
                    'input[id*="discount"]',
                    'input[name="promo_code"]',
                    'input[id="promo_code"]',
                    'input[name*="promo"]',
                    'input[id*="promo"]',
                    '#checkout-discount-input',
                    '.coupon-code-field input',
                    '.discount-code-field input',
                    '.promo-code-field input'
                ]
                
                for selector in coupon_field_selectors:
                    if await browser_engine.is_visible(selector):
                        await browser_engine.fill(selector, coupon_code)
                        logger.info(f"Filled coupon field with generic selector: {selector}")
                        coupon_field_found = True
                        break
                        
                # Last resort: Try to find any input that might be a coupon field
                if not coupon_field_found:
                    try:
                        # Look for inputs with coupon-related attributes using JavaScript
                        coupon_field_found = await browser_engine.evaluate(f'''
                            (() => {{  
                                const inputs = Array.from(document.querySelectorAll('input'));
                                const couponInput = inputs.find(input => {{  
                                    const placeholder = (input.placeholder || '').toLowerCase();
                                    const name = (input.name || '').toLowerCase();
                                    const id = (input.id || '').toLowerCase();
                                    return placeholder.includes('coupon') || 
                                           placeholder.includes('discount') || 
                                           placeholder.includes('promo') || 
                                           name.includes('coupon') || 
                                           name.includes('discount') || 
                                           name.includes('promo') || 
                                           id.includes('coupon') || 
                                           id.includes('discount') || 
                                           id.includes('promo');
                                }});
                                if (couponInput) {{  
                                    couponInput.value = '{coupon_code}';
                                    couponInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                                    couponInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
                                    return true;
                                }}
                                return false;
                            }})()''')
                        if coupon_field_found:
                            logger.info("Found and filled coupon field using JavaScript")
                    except Exception as e:
                        logger.warning(f"JavaScript coupon field detection failed: {str(e)}")
            
            if not coupon_field_found:
                return {'success': False, 'error': 'Could not find coupon input field'}
            
            # Try to click apply button using platform-provided selectors
            apply_button_clicked = False
            
            # Check if we have AI-detected apply button with high confidence
            ai_confidence_threshold = 0.8
            has_ai_button_detection = False
            
            if 'ai_confidence_scores' in platform_info and 'coupon_button' in platform_info['ai_confidence_scores']:
                if platform_info['ai_confidence_scores']['coupon_button'] > ai_confidence_threshold:
                    has_ai_button_detection = True
                    logger.info(f"Using AI-detected apply button with confidence: {platform_info['ai_confidence_scores']['coupon_button']}")
            
            if platform_info and 'platform' in platform_info and platform_info['platform'] != 'unknown':
                if 'coupon_button' in platform_info and platform_info['coupon_button']:
                    for selector in platform_info['coupon_button']:
                        if await browser_engine.is_visible(selector):
                            await browser_engine.click(selector)
                            logger.info(f"Clicked apply button with {'AI-enhanced' if has_ai_button_detection else 'platform-specific'} selector: {selector}")
                            apply_button_clicked = True
                            break
            
            # If platform-specific selectors didn't work, try common selectors
            if not apply_button_clicked:
                apply_button_selectors = [
                    'button[name="apply_coupon"]',
                    'button[id="apply_coupon"]',
                    'button:has-text("Apply")',
                    'button:has-text("apply")',
                    'button:has-text("Apply Coupon")',
                    'button:has-text("Apply coupon")',
                    'button:has-text("Apply Discount")',
                    'button:has-text("Apply discount")',
                    'button:has-text("Apply Promo")',
                    'button:has-text("Apply promo")',
                    'input[value="Apply"]',
                    'input[value="Apply Coupon"]',
                    'input[value="Apply Discount"]',
                    'input[value="Apply Promo"]',
                    '.apply-coupon',
                    '.apply-discount',
                    '.apply-promo',
                    '#discount-coupon-form .action.primary',
                    '.discount-form .action.primary',
                    '.coupon-form .action.primary',
                    '.promo-form .action.primary'
                ]
                
                for selector in apply_button_selectors:
                    if await browser_engine.is_visible(selector):
                        await browser_engine.click(selector)
                        logger.info(f"Clicked apply button with generic selector: {selector}")
                        apply_button_clicked = True
                        break
                        
                # Last resort: Try to find any button that might be an apply button using JavaScript
                if not apply_button_clicked:
                    try:
                        apply_button_clicked = await browser_engine.evaluate('''
                            (() => {{  
                                const buttons = Array.from(document.querySelectorAll('button, input[type="submit"], input[type="button"]'));
                                const applyButton = buttons.find(button => {{  
                                    const text = (button.textContent || '').toLowerCase();
                                    const value = (button.value || '').toLowerCase();
                                    return text.includes('apply') || 
                                           value.includes('apply') || 
                                           button.classList.contains('coupon-btn') || 
                                           button.classList.contains('apply-coupon');
                                }});
                                if (applyButton) {{  
                                    applyButton.click();
                                    return true;
                                }}
                                return false;
                            }})()''')
                        if apply_button_clicked:
                            logger.info("Found and clicked apply button using JavaScript")
                    except Exception as e:
                        logger.warning(f"JavaScript apply button detection failed: {str(e)}")
            
            # If no apply button was found, try pressing Enter on the coupon field as a fallback
            if not apply_button_clicked:
                coupon_field_selectors = [
                    'input[name="coupon_code"]',
                    'input[id="coupon_code"]',
                    'input[name*="coupon"]',
                    'input[id*="coupon"]',
                    'input[name="discount_code"]',
                    'input[id="discount_code"]',
                    'input[name*="discount"]',
                    'input[id*="discount"]',
                    'input[name="promo_code"]',
                    'input[id="promo_code"]',
                    'input[name*="promo"]',
                    'input[id*="promo"]'
                ]
                
                for selector in coupon_field_selectors:
                    if await browser_engine.is_visible(selector):
                        await browser_engine.press_key(selector, 'Enter')
                        logger.info(f"Pressed Enter on coupon field: {selector}")
                        apply_button_clicked = True
                        break
            
            # Wait for any AJAX requests to complete
            await browser_engine.wait_for_navigation()
            
            # Take screenshot after applying coupon
            await browser_engine.take_screenshot('/tmp/after_coupon_application.png')
            
            # Check validation result
            validation_result = await self._check_validation_result(browser_engine, platform_info)
            
            return {
                'success': True,
                'is_valid': validation_result['is_valid'],
                'discount_amount': validation_result['discount_amount'],
                'success_message': validation_result['success_message'],
                'error_message': validation_result['error_message']
            }
            
        except Exception as e:
            logger.error(f"Error applying coupon: {str(e)}")
            return {'success': False, 'error': f"Error applying coupon: {str(e)}"}
    
    async def _check_validation_result(self, browser_engine, platform_info: Dict) -> Dict:
        """
        Check if the coupon application was successful.
        
        Args:
            browser_engine: The browser engine instance
            platform_info: Information about the website platform
            
        Returns:
            Dictionary with validation result information
        """
        result = {
            'is_valid': False,
            'discount_amount': None,
            'success_message': None,
            'error_message': None
        }
        
        try:
            # Check if we have AI-detected success/error elements with high confidence
            ai_confidence_threshold = 0.8
            has_ai_success_detection = False
            has_ai_error_detection = False
            
            if 'ai_confidence_scores' in platform_info:
                if 'coupon_success' in platform_info['ai_confidence_scores'] and platform_info['ai_confidence_scores']['coupon_success'] > ai_confidence_threshold:
                    has_ai_success_detection = True
                    logger.info(f"Using AI-detected success message with confidence: {platform_info['ai_confidence_scores']['coupon_success']}")
                
                if 'coupon_error' in platform_info['ai_confidence_scores'] and platform_info['ai_confidence_scores']['coupon_error'] > ai_confidence_threshold:
                    has_ai_error_detection = True
                    logger.info(f"Using AI-detected error message with confidence: {platform_info['ai_confidence_scores']['coupon_error']}")
            
            # Check for success messages using platform-specific selectors
            if platform_info and 'platform' in platform_info and platform_info['platform'] != 'unknown':
                if 'coupon_success' in platform_info and platform_info['coupon_success']:
                    for selector in platform_info['coupon_success']:
                        if await browser_engine.is_visible(selector):
                            success_message = await browser_engine.get_text(selector)
                            if success_message:
                                result['success_message'] = success_message
                                result['is_valid'] = True
                                logger.info(f"Found success message with {'AI-enhanced' if has_ai_success_detection else 'platform-specific'} selector: {selector}")
                                break
                
                # Check for error messages using platform-specific selectors
                if 'coupon_error' in platform_info and platform_info['coupon_error']:
                    for selector in platform_info['coupon_error']:
                        if await browser_engine.is_visible(selector):
                            error_message = await browser_engine.get_text(selector)
                            if error_message:
                                result['error_message'] = error_message
                                result['is_valid'] = False
                                logger.info(f"Found error message with {'AI-enhanced' if has_ai_error_detection else 'platform-specific'} selector: {selector}")
                                break
            
            # If platform-specific selectors didn't work, try common selectors
            if result['success_message'] is None and result['error_message'] is None:
                # Check for success messages using common selectors
                success_selectors = [
                    '.success-message',
                    '.alert-success',
                    '.message-success',
                    '.coupon-success',
                    '.discount-success',
                    '.promo-success',
                    'div:has-text("successfully")',
                    'div:has-text("Successfully")',
                    'div:has-text("applied")',
                    'div:has-text("Applied")',
                    'p:has-text("successfully")',
                    'p:has-text("Successfully")',
                    'p:has-text("applied")',
                    'p:has-text("Applied")',
                    'span:has-text("successfully")',
                    'span:has-text("Successfully")',
                    'span:has-text("applied")',
                    'span:has-text("Applied")'
                ]
                
                for selector in success_selectors:
                    if await browser_engine.is_visible(selector):
                        success_message = await browser_engine.get_text(selector)
                        if success_message:
                            result['success_message'] = success_message
                            result['is_valid'] = True
                            break
                
                # Check for error messages using common selectors
                error_selectors = [
                    '.error-message',
                    '.alert-danger',
                    '.message-error',
                    '.coupon-error',
                    '.discount-error',
                    '.promo-error',
                    'div:has-text("invalid")',
                    'div:has-text("Invalid")',
                    'div:has-text("expired")',
                    'div:has-text("Expired")',
                    'div:has-text("not valid")',
                    'div:has-text("Not valid")',
                    'p:has-text("invalid")',
                    'p:has-text("Invalid")',
                    'p:has-text("expired")',
                    'p:has-text("Expired")',
                    'p:has-text("not valid")',
                    'p:has-text("Not valid")',
                    'span:has-text("invalid")',
                    'span:has-text("Invalid")',
                    'span:has-text("expired")',
                    'span:has-text("Expired")',
                    'span:has-text("not valid")',
                    'span:has-text("Not valid")'
                ]
                
                for selector in error_selectors:
                    if await browser_engine.is_visible(selector):
                        error_message = await browser_engine.get_text(selector)
                        if error_message:
                            result['error_message'] = error_message
                            result['is_valid'] = False
                            break
            
            # Try to find discount amount
            discount_amount = await self._extract_discount_amount(browser_engine, platform_info)
            if discount_amount:
                result['discount_amount'] = discount_amount
                # If we found a discount amount but no success message, consider the coupon valid
                if result['success_message'] is None and result['error_message'] is None:
                    result['is_valid'] = True
            
            # If we still don't know if the coupon is valid, check if there's a discount amount
            if result['is_valid'] is False and result['error_message'] is None and discount_amount:
                result['is_valid'] = True
            
            return result
            
        except Exception as e:
            logger.error(f"Error checking validation result: {str(e)}")
            return result
    
    async def _extract_discount_amount(self, browser_engine, platform_info: Dict = None) -> Optional[str]:
        """
        Try to extract the discount amount from the page.
        
        Args:
            browser_engine: The browser engine instance
            platform_info: Optional information about the website platform
            
        Returns:
            Discount amount as string or None if not found
        """
        try:
            # Check if we have AI-detected discount amount element with high confidence
            ai_discount_selectors = []
            has_ai_discount_detection = False
            
            if platform_info and 'ai_confidence_scores' in platform_info:
                if 'discount_amount' in platform_info['ai_confidence_scores']:
                    ai_confidence_threshold = 0.8
                    if platform_info['ai_confidence_scores']['discount_amount'] > ai_confidence_threshold:
                        has_ai_discount_detection = True
                        logger.info(f"Using AI-detected discount amount with confidence: {platform_info['ai_confidence_scores']['discount_amount']}")
                        
                        # If we have platform_info with discount_amount selectors, prioritize them
                        if 'discount_amount' in platform_info and platform_info['discount_amount']:
                            ai_discount_selectors = platform_info['discount_amount']
            
            # Common selectors for discount amount
            discount_selectors = [
                '.discount-amount',
                '.discount',
                '.coupon-discount',
                '.order-discount',
                '.cart-discount',
                '.price-discount',
                '.order-summary__discount',
                '.cart-summary__discount',
                '.discount-total',
                'span:has-text("discount")',
                'div:has-text("discount")',
                'tr:has-text("discount")',
                'td:has-text("discount")',
                'span:has-text("Discount")',
                'div:has-text("Discount")',
                'tr:has-text("Discount")',
                'td:has-text("Discount")'
            ]
            
            # Prioritize AI-detected selectors
            if ai_discount_selectors:
                discount_selectors = ai_discount_selectors + discount_selectors
            
            for selector in discount_selectors:
                if await browser_engine.is_visible(selector):
                    discount_text = await browser_engine.get_text(selector)
                    if discount_text:
                        # Try to extract numeric value using regex
                        numeric_match = re.search(r'[\-\$£€]?\s*[\d,.]+', discount_text)
                        if numeric_match:
                            return numeric_match.group(0).strip()
            
            # If no discount amount found in specific elements, try to extract from the entire page
            html_content = await browser_engine.get_html_content()
            if html_content:
                # Look for common discount patterns in the HTML
                discount_patterns = [
                    r'discount[\s\w]*[:\-]\s*[\$£€]?\s*([\d,.]+)',
                    r'coupon[\s\w]*[:\-]\s*[\$£€]?\s*([\d,.]+)',
                    r'promo[\s\w]*[:\-]\s*[\$£€]?\s*([\d,.]+)',
                    r'[\-\$£€]\s*([\d,.]+)\s*discount',
                    r'[\-\$£€]\s*([\d,.]+)\s*coupon',
                    r'[\-\$£€]\s*([\d,.]+)\s*promo'
                ]
                
                for pattern in discount_patterns:
                    match = re.search(pattern, html_content, re.IGNORECASE)
                    if match:
                        return match.group(0).strip()
            
            return None
            
        except Exception as e:
            logger.error(f"Error extracting discount amount: {str(e)}")
            return None