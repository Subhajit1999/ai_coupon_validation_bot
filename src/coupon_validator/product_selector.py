"""Product Selection Module
----------------------
Handles finding and selecting products on e-commerce websites.
"""

import logging
import random
from typing import Dict, List, Optional

# Get logger
logger = logging.getLogger(__name__)


class ProductSelector:
    """Handles finding and selecting products on e-commerce websites."""
    
    async def find_and_select_product(self, browser_engine, platform_info: Dict) -> Dict:
        """
        Find and select a product on the website.
        
        Args:
            browser_engine: The browser engine instance
            platform_info: Information about the website platform
            
        Returns:
            Dictionary with success status and any error message
        """
        try:
            # Take screenshot before product selection
            await browser_engine.take_screenshot('/tmp/before_product_selection.png')
            
            # Check if we're already on a product page
            is_product_page = await self._check_if_product_page(browser_engine)
            if is_product_page:
                logger.info("Already on a product page, no need to select a product")
                return {'success': True}
            
            # Try to find product grid using platform-specific selectors
            product_elements = []
            if platform_info and 'platform' in platform_info and platform_info['platform'] != 'unknown':
                if 'product_grid' in platform_info and platform_info['product_grid']:
                    for selector in platform_info['product_grid']:
                        # Try to find all product elements using this selector
                        elements = await browser_engine.page.query_selector_all(selector)
                        if elements and len(elements) > 0:
                            product_elements = elements
                            logger.info(f"Found {len(elements)} products using platform-specific selector: {selector}")
                            break
            
            # If platform-specific selectors didn't work, try common selectors
            if not product_elements:
                common_product_selectors = [
                    '.product',
                    '.product-item',
                    '.product-card',
                    '.product-grid-item',
                    '.product-list-item',
                    '.item.product',
                    '.card.product',
                    'li.product',
                    'div.product',
                    '.product-container',
                    '.product-wrapper',
                    '.product-box',
                    '.product-block',
                    '.product-cell',
                    '.product-thumbnail',
                    '.product-teaser',
                    '.product-preview',
                    '.product-tile',
                    '.catalog-product',
                    '.shop-product',
                    # Additional selectors for more sites
                    '.collection-item',
                    '.item-card',
                    '.product-item-info',
                    '.product-thumb',
                    '.product-layout',
                    '.grid-item',
                    '.grid-product',
                    '.grid__item',
                    '.collection-grid-item',
                    '.product-collection',
                    '.product-single',
                    '.product-miniature',
                    '.thumbnail-container',
                    '.card-product',
                    '.product-miniature'
                ]
                
                for selector in common_product_selectors:
                    elements = await browser_engine.page.query_selector_all(selector)
                    if elements and len(elements) > 0:
                        product_elements = elements
                        logger.info(f"Found {len(elements)} products using generic selector: {selector}")
                        break
            
            # If we still don't have product elements, try to find product links
            if not product_elements:
                # Try to find links that might be products
                js_result = await browser_engine.execute_javascript(r"""
                    // Find all links that might be product links
                    const productLinks = Array.from(document.querySelectorAll('a')).filter(a => {
                        const href = (a.href || '').toLowerCase();
                        const text = (a.textContent || '').toLowerCase();
                        const hasProductImage = a.querySelector('img') !== null;
                        
                        // Check URL patterns
                        const urlPatterns = href.includes('product') || 
                                           href.includes('item') || 
                                           href.includes('detail') || 
                                           href.match(/\/p\/\d+/) || 
                                           href.match(/\/products\/[\w-]+/) ||
                                           href.includes('collection') ||
                                           href.includes('category');
                                           
                        // Check if it looks like a product card
                        const hasPrice = text.includes('$') || 
                                        text.includes('price') || 
                                        text.includes('rs.') || 
                                        text.includes('inr') ||
                                        text.match(/\d+\.\d+/);
                                        
                        return (urlPatterns || hasPrice) && hasProductImage;
                    });
                    
                    return productLinks.length;
                """)
                
                if js_result and js_result > 0:
                    logger.info(f"Found {js_result} potential product links using JavaScript")
                    
                    # Click on a random product link
                    random_index = random.randint(0, min(js_result - 1, 9))  # Limit to first 10 products
                    js_click_result = await browser_engine.execute_javascript(r"""
                        // Find all links that might be product links
                        const productLinks = Array.from(document.querySelectorAll('a')).filter(a => {
                            const href = (a.href || '').toLowerCase();
                            const text = (a.textContent || '').toLowerCase();
                            const hasProductImage = a.querySelector('img') !== null;
                            
                            // Check URL patterns
                            const urlPatterns = href.includes('product') || 
                                               href.includes('item') || 
                                               href.includes('detail') || 
                                               href.match(/\/p\/\d+/) || 
                                               href.match(/\/products\/[\w-]+/) ||
                                               href.includes('collection') ||
                                               href.includes('category');
                                               
                            // Check if it looks like a product card
                            const hasPrice = text.includes('$') || 
                                            text.includes('price') || 
                                            text.includes('rs.') || 
                                            text.includes('inr') ||
                                            text.match(/\d+\.\d+/);
                                            
                            return (urlPatterns || hasPrice) && hasProductImage;
                        });
                        
                        if (productLinks.length > arguments[0]) {
                            productLinks[arguments[0]].click();
                            return true;
                        }
                        
                        return false;
                    """, random_index)
                    
                    if js_click_result:
                        logger.info(f"Clicked on product link at index {random_index} using JavaScript")
                        await browser_engine.wait_for_navigation()
                        return {'success': True}
            
            # If we have product elements, select a random one and click it
            if product_elements and len(product_elements) > 0:
                # Select a random product (limited to first 10 to avoid pagination issues)
                random_index = random.randint(0, min(len(product_elements) - 1, 9))
                selected_product = product_elements[random_index]
                
                # Try to find a link within the product element
                product_link = await selected_product.query_selector('a')
                if product_link:
                    await product_link.click()
                    logger.info(f"Clicked on product link at index {random_index}")
                else:
                    # If no link found, click the product element itself
                    await selected_product.click()
                    logger.info(f"Clicked on product element at index {random_index}")
                
                await browser_engine.wait_for_navigation()
                return {'success': True}
            
            # Last resort: try to find any clickable element that might be a product
            last_resort_result = await self._last_resort_product_selection(browser_engine)
            if last_resort_result['success']:
                return last_resort_result
            
            # If we couldn't find any products, return an error
            return {'success': False, 'error': 'Could not find any products on the page'}
            
        except Exception as e:
            logger.error(f"Error finding and selecting product: {str(e)}")
            return {'success': False, 'error': f"Error finding and selecting product: {str(e)}"}
    
    async def _check_if_product_page(self, browser_engine) -> bool:
        """
        Check if we're already on a product page by looking for common product page elements.
        
        Args:
            browser_engine: The browser engine instance
            
        Returns:
            True if current page appears to be a product page, False otherwise
        """
        try:
            # Check for common product page indicators
            product_page_indicators = [
                # Add to cart buttons
                '.add-to-cart',
                '.add_to_cart',
                '#add-to-cart',
                '#add_to_cart',
                'button:has-text("Add to Cart")',
                'button:has-text("Add to cart")',
                'button:has-text("Add to Bag")',
                'button:has-text("Buy Now")',
                
                # Product details elements
                '.product-details',
                '.product-info',
                '.product-description',
                '.product_description',
                '.product-title',
                '.product_title',
                '.product-price',
                '.product_price',
                
                # Product image gallery
                '.product-gallery',
                '.product-image-gallery',
                '.product-images',
                '.product_images'
            ]
            
            for selector in product_page_indicators:
                if await browser_engine.is_visible(selector):
                    logger.info(f"Detected product page indicator: {selector}")
                    return True
            
            # Check URL patterns
            url_check = await browser_engine.execute_javascript("""
                const url = window.location.href.toLowerCase();
                return url.includes('product') || 
                       url.includes('/p/') || 
                       url.includes('/products/') || 
                       url.includes('item') || 
                       url.includes('detail');
            """)
            
            if url_check:
                logger.info("URL pattern suggests we're on a product page")
                return True
                
            return False
            
        except Exception as e:
            logger.warning(f"Error checking if on product page: {str(e)}")
            return False
    
    async def _last_resort_product_selection(self, browser_engine) -> Dict:
        """
        Last resort method to find and click on anything that might be a product.
        
        Args:
            browser_engine: The browser engine instance
            
        Returns:
            Dictionary with success status and any error message
        """
        try:
            # Look for any image with a parent link that might be a product
            js_result = await browser_engine.execute_javascript("""
                // Find all images that are inside links
                const imgLinks = Array.from(document.querySelectorAll('a > img, a img'));
                if (imgLinks.length > 0) {
                    // Click on a random image link
                    const randomIndex = Math.floor(Math.random() * Math.min(imgLinks.length, 10));
                    const imgLink = imgLinks[randomIndex].closest('a');
                    if (imgLink) {
                        imgLink.click();
                        return true;
                    }
                }
                return false;
            """)
            
            if js_result:
                logger.info("Clicked on a random image link as last resort")
                await browser_engine.wait_for_navigation()
                return {'success': True}
            
            # Try clicking on any element with 'product' in its class or id
            js_result = await browser_engine.execute_javascript("""
                // Find elements with 'product' in class or id
                const productElements = Array.from(document.querySelectorAll('*')).filter(el => {
                    return (el.className && el.className.includes('product')) || 
                           (el.id && el.id.includes('product'));
                });
                
                if (productElements.length > 0) {
                    // Click on a random product element
                    const randomIndex = Math.floor(Math.random() * Math.min(productElements.length, 10));
                    productElements[randomIndex].click();
                    return true;
                }
                return false;
            """)
            
            if js_result:
                logger.info("Clicked on an element with 'product' in class/id as last resort")
                await browser_engine.wait_for_navigation()
                return {'success': True}
            
            return {'success': False, 'error': 'Last resort product selection failed'}
            
        except Exception as e:
            logger.warning(f"Error in last resort product selection: {str(e)}")
            return {'success': False, 'error': f"Last resort selection error: {str(e)}"}
    
    async def add_to_cart(self, browser_engine, platform_info: Dict) -> Dict:
        """
        Add the current product to the cart.
        
        Args:
            browser_engine: The browser engine instance
            platform_info: Information about the website platform
            
        Returns:
            Dictionary with success status and any error message
        """
        try:
            # Take screenshot before adding to cart
            await browser_engine.take_screenshot('/tmp/before_add_to_cart.png')
            
            # Handle required product options/variations if present
            await self._handle_product_options(browser_engine)
            
            # Try to find add to cart button using platform-specific selectors
            if platform_info and 'platform' in platform_info and platform_info['platform'] != 'unknown':
                if 'add_to_cart' in platform_info and platform_info['add_to_cart']:
                    for selector in platform_info['add_to_cart']:
                        if await browser_engine.is_visible(selector):
                            if await browser_engine.click(selector):
                                logger.info(f"Clicked add to cart button with platform-specific selector: {selector}")
                                # Wait for any AJAX requests to complete
                                await browser_engine.wait_for_navigation()
                                
                                # Check if we need to navigate to cart
                                await self._navigate_to_cart_if_needed(browser_engine)
                                
                                return {'success': True}
            
            # If platform-specific selectors didn't work, try common selectors
            add_to_cart_selectors = [
                '#product-addtocart-button',
                '.add-to-cart-button',
                '.add-to-cart',
                '.add_to_cart',
                '#add-to-cart',
                '#add_to_cart',
                'button:has-text("Add to Cart")',
                'button:has-text("Add to cart")',
                'button:has-text("Add to Bag")',
                'button:has-text("Add to bag")',
                'button:has-text("Add to Basket")',
                'button:has-text("Add to basket")',
                'button:has-text("Buy Now")',
                'button:has-text("Buy now")',
                'input[value="Add to Cart"]',
                'input[value="Add to cart"]',
                'a:has-text("Add to Cart")',
                'a:has-text("Add to cart")',
                '.btn-cart',
                '.btn-add-to-cart',
                '.button-add-to-cart',
                '.product-add-to-cart',
                '.product-add-form button',
                '.product-info-button button',
                '.product-actions button'
            ]
            
            for selector in add_to_cart_selectors:
                if await browser_engine.is_visible(selector):
                    if await browser_engine.click(selector):
                        logger.info(f"Clicked add to cart button with generic selector: {selector}")
                        # Wait for any AJAX requests to complete
                        await browser_engine.wait_for_navigation()
                        
                        # Check if we need to navigate to cart
                        await self._navigate_to_cart_if_needed(browser_engine)
                        
                        return {'success': True}
            
            # If no add to cart button was found, try using JavaScript
            js_result = await browser_engine.execute_javascript("""
                // Try to find and click add to cart buttons
                const addToCartButtons = Array.from(document.querySelectorAll('button, input[type="submit"], a')).filter(el => {
                    const text = (el.textContent || '').toLowerCase();
                    const value = (el.value || '').toLowerCase();
                    const id = (el.id || '').toLowerCase();
                    const className = (el.className || '').toLowerCase();
                    
                    return text.includes('add to cart') || 
                           text.includes('add to bag') || 
                           text.includes('add to basket') || 
                           value.includes('add to cart') || 
                           id.includes('add-to-cart') || 
                           id.includes('addtocart') || 
                           className.includes('add-to-cart') || 
                           className.includes('addtocart');
                });
                
                if (addToCartButtons.length > 0) {
                    addToCartButtons[0].click();
                    return true;
                }
                
                return false;
            """)
            
            if js_result:
                logger.info("Used JavaScript to click add to cart button")
                # Wait for any AJAX requests to complete
                await browser_engine.wait_for_navigation()
                
                # Check if we need to navigate to cart
                await self._navigate_to_cart_if_needed(browser_engine)
                
                return {'success': True}
            
            # Take screenshot after failed add to cart
            await browser_engine.take_screenshot('/tmp/failed_add_to_cart.png')
            
            return {'success': False, 'error': 'Could not find add to cart button'}
            
        except Exception as e:
            logger.error(f"Error adding product to cart: {str(e)}")
            return {'success': False, 'error': f"Error adding product to cart: {str(e)}"}
    
    async def _handle_product_options(self, browser_engine) -> None:
        """
        Handle required product options/variations if present.
        
        Args:
            browser_engine: The browser engine instance
        """
        try:
            # Check for size options
            size_selectors = [
                'select[id*="size"]',
                'select[name*="size"]',
                'select[id*="Size"]',
                'select[name*="Size"]',
                '.size-options select',
                '.size-selector select',
                '.size-dropdown',
                '.swatch-attribute-size select',
                '#attribute92',  # Common Magento size attribute
                '#attribute180'  # Another common Magento size attribute
            ]
            
            for selector in size_selectors:
                if await browser_engine.is_visible(selector):
                    # If it's a select element
                    is_select = await browser_engine.execute_javascript("""
                        return document.querySelector(arguments[0]).tagName.toLowerCase() === 'select';
                    """, selector)
                    
                    if is_select:
                        # Select a random option (skipping the first if it's a placeholder)
                        await browser_engine.execute_javascript("""
                            const select = document.querySelector(arguments[0]);
                            if (select.options.length > 0) {
                                // Skip the first option if it's a placeholder
                                const startIndex = select.options[0].value ? 0 : 1;
                                if (select.options.length > startIndex) {
                                    // Select a random option
                                    const randomIndex = startIndex + Math.floor(Math.random() * (select.options.length - startIndex));
                                    select.value = select.options[randomIndex].value;
                                    select.dispatchEvent(new Event('change', { bubbles: true }));
                                }
                            }
                        """, selector)
                        logger.info(f"Selected random size option from: {selector}")
                    else:
                        # If not a select, it might be a list of options (like swatches)
                        # Try to click a random option
                        await browser_engine.execute_javascript("""
                            const container = document.querySelector(arguments[0]);
                            const options = container.querySelectorAll('li, div, a, span');
                            if (options.length > 0) {
                                const randomIndex = Math.floor(Math.random() * options.length);
                                options[randomIndex].click();
                            }
                        """, selector)
                    break
            
            # Check for color options
            color_selectors = [
                'select[id*="color"]',
                'select[name*="color"]',
                'select[id*="Color"]',
                'select[name*="Color"]',
                '.color-options select',
                '.color-selector select',
                '.color-dropdown',
                '.swatch-attribute-color select',
                '#attribute93',  # Common Magento color attribute
                '#attribute92'   # Another common Magento color attribute
            ]
            
            for selector in color_selectors:
                if await browser_engine.is_visible(selector):
                    # If it's a select element
                    is_select = await browser_engine.execute_javascript("""
                        return document.querySelector(arguments[0]).tagName.toLowerCase() === 'select';
                    """, selector)
                    
                    if is_select:
                        # Select a random option (skipping the first if it's a placeholder)
                        await browser_engine.execute_javascript("""
                            const select = document.querySelector(arguments[0]);
                            if (select.options.length > 0) {
                                // Skip the first option if it's a placeholder
                                const startIndex = select.options[0].value ? 0 : 1;
                                if (select.options.length > startIndex) {
                                    // Select a random option
                                    const randomIndex = startIndex + Math.floor(Math.random() * (select.options.length - startIndex));
                                    select.value = select.options[randomIndex].value;
                                    select.dispatchEvent(new Event('change', { bubbles: true }));
                                }
                            }
                        """, selector)
                        logger.info(f"Selected random color option from: {selector}")
                    else:
                        # If not a select, it might be a list of options (like swatches)
                        # Try to click a random option
                        await browser_engine.execute_javascript("""
                            const container = document.querySelector(arguments[0]);
                            const options = container.querySelectorAll('li, div, a, span');
                            if (options.length > 0) {
                                const randomIndex = Math.floor(Math.random() * options.length);
                                options[randomIndex].click();
                            }
                        """, selector)
                    break
            
            # Check for quantity input
            quantity_selectors = [
                'input[name="qty"]',
                'input[id="qty"]',
                'input[name*="quantity"]',
                'input[id*="quantity"]',
                'input[name*="Quantity"]',
                'input[id*="Quantity"]',
                '.quantity input',
                '.qty-input',
                '.quantity-selector input',
                '.quantity-field'
            ]
            
            for selector in quantity_selectors:
                if await browser_engine.is_visible(selector):
                    # Set quantity to 1
                    await browser_engine.fill(selector, "1")
                    logger.info(f"Set quantity to 1 in: {selector}")
                    break
                    
        except Exception as e:
            logger.warning(f"Error handling product options (non-critical): {str(e)}")
            # Continue even if options couldn't be selected
    
    async def _navigate_to_cart_if_needed(self, browser_engine) -> None:
        """
        Navigate to cart page if needed after adding product.
        
        Args:
            browser_engine: The browser engine instance
        """
        try:
            # Check if we're already on cart page
            current_url = await browser_engine.get_current_url()
            if current_url and 'cart' in current_url.lower():
                logger.info("Already on cart page")
                return
            
            # Check for "View Cart" or "Go to Cart" buttons that might appear after adding to cart
            cart_navigation_selectors = [
                'a:has-text("View Cart")',
                'a:has-text("View cart")',
                'a:has-text("Go to Cart")',
                'a:has-text("Go to cart")',
                'button:has-text("View Cart")',
                'button:has-text("View cart")',
                'button:has-text("Go to Cart")',
                'button:has-text("Go to cart")',
                '.view-cart',
                '.view-cart-button',
                '.go-to-cart',
                '.go-to-cart-button',
                '.cart-link',
                '.cart-button',
                '#top-cart',
                '.minicart-wrapper .action.showcart',
                '.minicart-wrapper a.action.viewcart'
            ]
            
            for selector in cart_navigation_selectors:
                if await browser_engine.is_visible(selector):
                    if await browser_engine.click(selector):
                        logger.info(f"Clicked cart navigation button: {selector}")
                        await browser_engine.wait_for_navigation()
                        return
            
            # If no specific button was found, try to find cart link in the header/navigation
            js_result = await browser_engine.execute_javascript("""
                // Try to find and click cart links
                const cartLinks = Array.from(document.querySelectorAll('a')).filter(a => {
                    const href = (a.href || '').toLowerCase();
                    const text = (a.textContent || '').toLowerCase();
                    return href.includes('cart') || text.includes('cart') || 
                           href.includes('basket') || text.includes('basket') || 
                           href.includes('bag') || text.includes('bag');
                });
                
                if (cartLinks.length > 0) {
                    cartLinks[0].click();
                    return true;
                }
                
                // Try to find cart icons
                const cartIcons = Array.from(document.querySelectorAll('a, button, span, div')).filter(el => {
                    const className = (el.className || '').toLowerCase();
                    return className.includes('cart') || className.includes('basket') || 
                           className.includes('bag') || className.includes('minicart');
                });
                
                if (cartIcons.length > 0) {
                    cartIcons[0].click();
                    return true;
                }
                
                return false;
            """)
            
            if js_result:
                logger.info("Used JavaScript to navigate to cart")
                await browser_engine.wait_for_navigation()
                return
            
            # If all else fails, try to navigate directly to /cart URL
            current_url = await browser_engine.get_current_url()
            if current_url:
                parsed_url = current_url.split('/')
                base_url = parsed_url[0] + '//' + parsed_url[2]  # http(s)://domain.com
                
                cart_urls = [
                    base_url + '/cart',
                    base_url + '/basket',
                    base_url + '/bag',
                    base_url + '/checkout/cart',
                    base_url + '/shop/cart',
                    base_url + '/shopping-cart'
                ]
                
                for cart_url in cart_urls:
                    if await browser_engine.navigate(cart_url):
                        logger.info(f"Navigated directly to cart URL: {cart_url}")
                        return
                        
        except Exception as e:
            logger.warning(f"Error navigating to cart (non-critical): {str(e)}")
            # Continue even if navigation to cart failed
