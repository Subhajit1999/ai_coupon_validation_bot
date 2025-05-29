"""Cart and Checkout Navigator
-------------------------
Navigates through cart and checkout process.
"""

import logging
import re
from typing import Dict, Optional

# Get logger
logger = logging.getLogger(__name__)


class CartNavigator:
    """Navigates through cart and checkout process."""
    
    async def navigate_to_checkout(self, browser_engine, platform_info: Dict) -> Dict:
        """
        Navigate from cart to checkout page.
        
        Args:
            browser_engine: The browser engine instance
            platform_info: Information about the website platform
            
        Returns:
            Dictionary with success status and any error message
        """
        try:
            # Get current URL to determine if we're already on checkout
            current_url = await browser_engine.get_current_url()
            if not current_url:
                return {'success': False, 'error': 'Could not determine current URL'}
            
            # Check if we're already on a checkout page
            if 'checkout' in current_url.lower() or 'onepage' in current_url.lower():
                logger.info("Already on checkout page")
                return {'success': True}
            
            # Take screenshot before attempting checkout navigation
            await browser_engine.take_screenshot('/tmp/before_checkout_navigation.png')
            
            # Try platform-specific selectors first if available
            if platform_info and 'platform' in platform_info and platform_info['platform'] != 'unknown':
                if platform_info['platform'] == 'magento':
                    # For Magento, try to use the proceed to checkout button
                    magento_selectors = [
                        '#top-cart-btn-checkout',
                        '.action.primary.checkout',
                        'button.checkout',
                        '.checkout-methods-items .action.primary.checkout',
                        '.checkout-methods button.btn-proceed-checkout',
                        '#maincontent .action.primary.checkout'
                    ]
                    
                    for selector in magento_selectors:
                        if await browser_engine.is_visible(selector):
                            if await browser_engine.click(selector):
                                logger.info(f"Clicked Magento checkout button: {selector}")
                                await browser_engine.wait_for_navigation()
                                
                                # Check if we need to handle guest checkout
                                await self._handle_guest_checkout(browser_engine)
                                
                                # Fill minimum required fields to proceed
                                await self._fill_minimum_required_fields(browser_engine)
                                
                                return {'success': True}
                
                # Try platform-specific checkout selectors
                if 'checkout_button' in platform_info and platform_info['checkout_button']:
                    for selector in platform_info['checkout_button']:
                        if await browser_engine.is_visible(selector):
                            if await browser_engine.click(selector):
                                logger.info(f"Clicked platform-specific checkout button: {selector}")
                                await browser_engine.wait_for_navigation()
                                
                                # Check if we need to handle guest checkout
                                await self._handle_guest_checkout(browser_engine)
                                
                                # Fill minimum required fields to proceed
                                await self._fill_minimum_required_fields(browser_engine)
                                
                                return {'success': True}
            
            # Try JavaScript-based navigation
            js_result = await browser_engine.execute_javascript("""
                // Try to find and click checkout buttons
                const checkoutButtons = Array.from(document.querySelectorAll('a, button, input[type="submit"]')).filter(el => {
                    const text = el.textContent.toLowerCase();
                    const value = (el.value || '').toLowerCase();
                    const id = (el.id || '').toLowerCase();
                    const className = (el.className || '').toLowerCase();
                    
                    return text.includes('checkout') || 
                           text.includes('proceed to') || 
                           value.includes('checkout') || 
                           id.includes('checkout') || 
                           className.includes('checkout');
                });
                
                if (checkoutButtons.length > 0) {
                    checkoutButtons[0].click();
                    return true;
                }
                
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
                
                # Check if we need to handle guest checkout
                await self._handle_guest_checkout(browser_engine)
                
                # Fill minimum required fields to proceed
                await self._fill_minimum_required_fields(browser_engine)
                
                return {'success': True}
            
            # Try common checkout button selectors as a fallback
            checkout_selectors = [
                '.checkout-button',
                '#checkout',
                '.checkout',
                'button:has-text("Checkout")',
                'a:has-text("Checkout")',
                'input[value*="Checkout"]',
                'button:has-text("Proceed to")',
                'a:has-text("Proceed to")',
                '#proceed_to_checkout',
                '.proceed-to-checkout',
                '.cart-checkout',
                '.btn-checkout',
                '.button-checkout',
                '#button-confirm',
                '.button-confirm',
                'button.btn-primary:has-text("Continue")',
                'button.action.primary.checkout',
                '.action.primary.checkout',
                '.btn-proceed-checkout',
                '#top-cart-btn-checkout'
            ]
            
            for selector in checkout_selectors:
                if await browser_engine.is_visible(selector):
                    if await browser_engine.click(selector):
                        logger.info(f"Clicked generic checkout button: {selector}")
                        await browser_engine.wait_for_navigation()
                        
                        # Check if we need to handle guest checkout
                        await self._handle_guest_checkout(browser_engine)
                        
                        # Fill minimum required fields to proceed
                        await self._fill_minimum_required_fields(browser_engine)
                        
                        return {'success': True}
            
            # Take screenshot after failed checkout navigation
            await browser_engine.take_screenshot('/tmp/failed_checkout_navigation.png')
            
            return {'success': False, 'error': 'Could not find checkout button'}
            
        except Exception as e:
            logger.error(f"Error navigating to checkout: {str(e)}")
            return {'success': False, 'error': f"Error navigating to checkout: {str(e)}"}
    
    async def _handle_guest_checkout(self, browser_engine) -> None:
        """
        Handle guest checkout options if present.
        
        Args:
            browser_engine: The browser engine instance
        """
        try:
            # Common guest checkout selectors
            guest_checkout_selectors = [
                '#checkout-guest',  # Common guest checkout radio
                'input[value="guest"]',  # Guest radio button
                '#guest',  # Guest checkbox
                'button:has-text("Guest Checkout")',  # Guest checkout button
                'a:has-text("Guest Checkout")',  # Guest checkout link
                '#onepage-guest-register-button',  # Magento guest button
                '.action-guest',  # Guest action button
                'input[id*="guest"]',  # Input with guest in ID
                'label:has-text("Guest") input',  # Label with guest text
                'input[name="account"][value="guest"]'  # Account type input
            ]
            
            # Try to select guest checkout option
            for selector in guest_checkout_selectors:
                if await browser_engine.is_visible(selector):
                    await browser_engine.click(selector)
                    logger.info(f"Selected guest checkout option: {selector}")
                    break
            
            # Try to click continue buttons after selecting guest checkout
            continue_selectors = [
                '#button-account',  # Common continue button
                '#button-guest',  # Guest continue button
                'button:has-text("Continue")',  # Continue text button
                'input[value="Continue"]',  # Continue input button
                '.action-continue',  # Continue action
                '#onepage-guest-register-button',  # Magento register button
                '.action.primary.continue',  # Primary continue action
                'button.btn-primary',  # Primary button
                'button.action.continue',  # Continue action button
                'button[type="submit"]'  # Any submit button
            ]
            
            for selector in continue_selectors:
                if await browser_engine.is_visible(selector):
                    await browser_engine.click(selector)
                    logger.info(f"Clicked continue after guest selection: {selector}")
                    await browser_engine.wait_for_navigation()
                    break
                    
        except Exception as e:
            logger.warning(f"Error handling guest checkout (non-critical): {str(e)}")
    
    async def _fill_minimum_required_fields(self, browser_engine) -> None:
        """
        Fill minimum required fields to proceed with checkout.
        
        Args:
            browser_engine: The browser engine instance
        """
        try:
            # Common checkout fields with multiple possible selectors and default values
            checkout_fields = {
                'email': {
                    'selectors': [
                        '#customer-email',
                        'input[type="email"]',
                        'input[name="email"]',
                        'input[id*="email"]',
                        'input[placeholder*="email"]',
                        '#checkout-step-login input[type="email"]'
                    ],
                    'value': 'test@example.com'
                },
                'first_name': {
                    'selectors': [
                        'input[name="firstname"]',
                        'input[name="billing[firstname]"]',
                        'input[id*="firstname"]',
                        'input[name*="first_name"]',
                        'input[name*="firstName"]',
                        'input[placeholder*="First Name"]',
                        '#billing-new input[id*="firstname"]'
                    ],
                    'value': 'Test'
                },
                'last_name': {
                    'selectors': [
                        'input[name="lastname"]',
                        'input[name="billing[lastname]"]',
                        'input[id*="lastname"]',
                        'input[name*="last_name"]',
                        'input[name*="lastName"]',
                        'input[placeholder*="Last Name"]',
                        '#billing-new input[id*="lastname"]'
                    ],
                    'value': 'User'
                },
                'address': {
                    'selectors': [
                        'input[name="street[0]"]',
                        'input[name="billing[street][0]"]',
                        'input[name*="address"]',
                        'input[name*="street"]',
                        'input[id*="address"]',
                        'input[placeholder*="Address"]',
                        'textarea[name*="address"]',
                        '#billing-new input[id*="address"]'
                    ],
                    'value': '123 Test Street'
                },
                'city': {
                    'selectors': [
                        'input[name="city"]',
                        'input[name="billing[city]"]',
                        'input[id*="city"]',
                        'input[name*="city"]',
                        'input[placeholder*="City"]',
                        '#billing-new input[id*="city"]'
                    ],
                    'value': 'Test City'
                },
                'zip': {
                    'selectors': [
                        'input[name="postcode"]',
                        'input[name="billing[postcode]"]',
                        'input[id*="postcode"]',
                        'input[name*="zip"]',
                        'input[name*="postal"]',
                        'input[placeholder*="Zip"]',
                        'input[placeholder*="Postal"]',
                        '#billing-new input[id*="postcode"]'
                    ],
                    'value': '12345'
                },
                'phone': {
                    'selectors': [
                        'input[name="telephone"]',
                        'input[name="billing[telephone]"]',
                        'input[id*="telephone"]',
                        'input[name*="phone"]',
                        'input[placeholder*="Phone"]',
                        '#billing-new input[id*="telephone"]'
                    ],
                    'value': '1234567890'
                }
            }
            
            # Try to fill each field
            for field_name, field_info in checkout_fields.items():
                for selector in field_info['selectors']:
                    if await browser_engine.is_visible(selector):
                        await browser_engine.fill(selector, field_info['value'])
                        logger.info(f"Filled {field_name} field: {selector}")
                        break
            
            # Handle country selection (usually a select element)
            country_selectors = [
                'select[name="country_id"]',
                'select[name="billing[country_id]"]',
                'select[id*="country"]',
                'select[name*="country"]',
                '#billing-new select[id*="country"]'
            ]
            
            for selector in country_selectors:
                if await browser_engine.is_visible(selector):
                    # Check if it's a select element
                    is_select = await browser_engine.execute_javascript("""
                        return document.querySelector(arguments[0]).tagName.toLowerCase() === 'select';
                    """, selector)
                    
                    if is_select:
                        # Select US as default country
                        await browser_engine.execute_javascript("""
                            const select = document.querySelector(arguments[0]);
                            const usOption = Array.from(select.options).find(option => 
                                option.value === 'US' || 
                                option.textContent.includes('United States'));
                            
                            if (usOption) {
                                select.value = usOption.value;
                                select.dispatchEvent(new Event('change', { bubbles: true }));
                            }
                        """, selector)
                        logger.info(f"Selected US as country in: {selector}")
                    else:
                        # If not a select, try to fill it as a text field
                        await browser_engine.fill(selector, "United States")
                    break
            
            # Handle state/region selection
            state_selectors = [
                'select[name="region_id"]',
                'select[name="billing[region_id]"]',
                'select[id*="region"]',
                'select[name*="state"]',
                'select[name*="province"]',
                '#billing-new select[id*="region"]'
            ]
            
            for selector in state_selectors:
                if await browser_engine.is_visible(selector):
                    # Check if it's a select element
                    is_select = await browser_engine.execute_javascript("""
                        return document.querySelector(arguments[0]).tagName.toLowerCase() === 'select';
                    """, selector)
                    
                    if is_select:
                        # Select the first option as default state
                        await browser_engine.execute_javascript("""
                            const select = document.querySelector(arguments[0]);
                            if (select.options.length > 0) {
                                // Skip the first option if it's a placeholder
                                const startIndex = select.options[0].value ? 0 : 1;
                                if (select.options.length > startIndex) {
                                    select.value = select.options[startIndex].value;
                                    select.dispatchEvent(new Event('change', { bubbles: true }));
                                }
                            }
                        """, selector)
                        logger.info(f"Selected first available state/region in: {selector}")
                    else:
                        # If not a select, try to fill it as a text field
                        await browser_engine.fill(selector, "CA")
                    break
            
            # Try to click continue/next buttons
            continue_selectors = [
                'button.continue',
                'button:has-text("Continue")',
                'button.action.continue',
                'button.action.primary.continue',
                'button[data-role="opc-continue"]',
                'button.button.btn-continue',
                'input[value="Continue"]',
                'button.btn-primary',
                'button[type="submit"]'
            ]
            
            for selector in continue_selectors:
                if await browser_engine.is_visible(selector):
                    await browser_engine.click(selector)
                    logger.info(f"Clicked continue after filling fields: {selector}")
                    await browser_engine.wait_for_navigation()
                    break
                    
        except Exception as e:
            logger.warning(f"Error filling minimum required fields (non-critical): {str(e)}")
            # Continue even if some fields couldn't be filled