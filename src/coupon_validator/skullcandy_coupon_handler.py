import logging
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)

class SkullcandyCouponHandler:
    """Special handler for Skullcandy website coupon application"""
    
    def __init__(self):
        self.coupon_section_selectors = [
            '.discount-trigger',
            '.coupon-trigger',
            '.promo-trigger',
            'button:has-text("Apply Coupon")',
            'button:has-text("Apply Discount")',
            'button:has-text("Apply Promo")',
            'a:has-text("Apply Coupon")',
            'a:has-text("Apply Discount")',
            'a:has-text("Apply Promo")'
        ]
        
        self.cart_link_selectors = [
            '.cart-link',
            '.cart-icon',
            'a[href*="/cart"]',
            '.cart-count-bubble'
        ]
    
    async def find_and_expand_coupon_section(self, browser_engine):
        """Find and expand the coupon code section if it's collapsed"""
        try:
            # Check if we're on the cart page, if not navigate to it
            current_url = browser_engine.page.url
            if '/cart' not in current_url:
                for selector in self.cart_link_selectors:
                    if await self._is_element_visible(browser_engine, selector):
                        logger.info(f"Clicking cart link: {selector}")
                        await browser_engine.click(selector)
                        await browser_engine.page.wait_for_load_state('networkidle')
                        break
            
            # Look for coupon/discount section toggle if it's collapsed
            for selector in self.coupon_section_selectors:
                if await self._is_element_visible(browser_engine, selector):
                    logger.info(f"Expanding coupon section: {selector}")
                    await browser_engine.click(selector)
                    await browser_engine.page.wait_for_timeout(1000)  # Wait for animation
                    break
            
            # If we can't find a specific toggle, try to look for any element that might reveal the coupon field
            await browser_engine.evaluate('''
                (() => {
                    const possibleTriggers = Array.from(document.querySelectorAll('button, a, .coupon, .discount, .promo'));
                    const trigger = possibleTriggers.find(el => {
                        const text = (el.textContent || '').toLowerCase();
                        return text.includes('coupon') || 
                               text.includes('discount') || 
                               text.includes('promo') || 
                               text.includes('code');
                    });
                    if (trigger) {
                        trigger.click();
                        return true;
                    }
                    return false;
                })()
            ''')
            
        except Exception as e:
            logger.warning(f"Error expanding Skullcandy coupon section: {e}")
    
    async def _is_element_visible(self, browser_engine, selector):
        """Check if an element is visible on the page"""
        try:
            element = await browser_engine.page.query_selector(selector)
            if element:
                return await element.is_visible()
            return False
        except Exception:
            return False