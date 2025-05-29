"""Website Pattern Recognizer Module
--------------------------------
Detects e-commerce platform and extracts platform-specific selectors.
"""

import logging
import re
from typing import Dict, List, Optional

# Get logger
logger = logging.getLogger(__name__)


class WebsitePatternRecognizer:
    """Detects e-commerce platform and extracts platform-specific selectors."""
    
    def __init__(self):
        """Initialize the website pattern recognizer."""
        # Platform detection patterns
        self.platform_patterns = {
            'magento': [
                r'Magento',
                r'mage/cookies',
                r'magento-version',
                r'Mage.Cookies',
                r'Magento_Ui',
                r'catalog\/product\/view',
                r'checkout\/cart',
                r'requirejs-config'
            ],
            'woocommerce': [
                r'woocommerce',
                r'WooCommerce',
                r'wc-',
                r'wc_',
                r'is-woocommerce-',
                r'woocommerce-',
                r'wp-content'
            ],
            'shopify': [
                r'shopify',
                r'Shopify',
                r'shopify-',
                r'\/cdn\/shop',
                r'shopify.com',
                r'myshopify.com'
            ],
            'opencart': [
                r'opencart',
                r'OpenCart',
                r'route=checkout',
                r'route=product',
                r'catalog\/view'
            ],
            'prestashop': [
                r'prestashop',
                r'PrestaShop',
                r'presta-',
                r'id_product=',
                r'controller=product',
                r'controller=cart'
            ],
            'bigcommerce': [
                r'bigcommerce',
                r'BigCommerce',
                r'bc-',
                r'bigcommerce.com',
                r'data-cart'
            ],
            'skullcandy': [
                r'skullcandy',
                r'Skullcandy',
                r'skullcandy.in',
                r'skullcandy.com',
                r'skull-',
                r'collection\/tws'
            ],
            'custom_ecommerce': [
                r'add-to-cart',
                r'add_to_cart',
                r'cart',
                r'checkout',
                r'product',
                r'collection',
                r'category'
            ]
        }
        
        # Platform-specific selectors
        self.platform_selectors = {
            'magento': {
                'product_grid': [
                    '.products-grid .product-item',
                    '.product-items .product-item',
                    '.products.list .product-item'
                ],
                'add_to_cart': [
                    '#product-addtocart-button',
                    '.action.tocart',
                    '.action.primary.tocart'
                ],
                'cart_link': [
                    '.action.showcart',
                    '.minicart-wrapper .action.showcart',
                    '.action.viewcart'
                ],
                'checkout_button': [
                    '.action.primary.checkout',
                    '#top-cart-btn-checkout',
                    '.checkout-methods-items .action.primary.checkout'
                ],
                'coupon_field': [
                    '#coupon_code',
                    '#discount-code',
                    '#discount-coupon-form #coupon_code'
                ],
            },
            'skullcandy': {
                'product_grid': [
                    '.collection-item',
                    '.product-item',
                    '.grid-item',
                    '.product-card'
                ],
                'add_to_cart': [
                    '.add-to-cart',
                    '.add_to_cart',
                    'button:has-text("Add to Cart")',
                    'button:has-text("Buy Now")',
                    '.product-form__cart-submit'
                ],
                'cart_link': [
                    '.cart-link',
                    '.cart-icon',
                    'a[href*="/cart"]',
                    '.cart-count-bubble'
                ],
                'checkout_button': [
                    '.checkout-button',
                    'button:has-text("Checkout")',
                    'button:has-text("Proceed to Checkout")',
                    'a:has-text("Checkout")'
                ],
                'coupon_field': [
                    '#coupon_code',
                    '#discount-code',
                    'input[name="discount"]',
                    'input[placeholder*="coupon"]',
                    'input[placeholder*="Coupon"]',
                    'input[placeholder*="discount"]',
                    'input[placeholder*="Discount"]',
                    'input[placeholder*="promo"]',
                    'input[placeholder*="Promo"]'
                ],
                'coupon_button': [
                    'button:has-text("Apply")',
                    'button:has-text("Apply Coupon")',
                    'button:has-text("Apply Discount")',
                    'input[value="Apply"]',
                    '.coupon-btn',
                    '.apply-coupon'
                ],
                'coupon_success': [
                    '.coupon-success',
                    '.discount-success',
                    '.success-message',
                    '.alert-success',
                    '.discount-applied'
                ],
                'coupon_error': [
                    '.coupon-error',
                    '.discount-error',
                    '.error-message',
                    '.alert-error',
                    '.alert-danger'
                ],
                'discount_amount': [
                    '.discount-amount',
                    '.cart-discount',
                    '.order-discount',
                    '.discount-total',
                    '.discount-value'
                ]
            },
            'custom_ecommerce': {
                'product_grid': [
                    '.product',
                    '.product-item',
                    '.product-card',
                    '.collection-item',
                    '.grid-item',
                    '.item-card'
                ],
                'add_to_cart': [
                    '.add-to-cart',
                    '.add_to_cart',
                    '#add-to-cart',
                    '#add_to_cart',
                    'button:has-text("Add to Cart")',
                    'button:has-text("Buy Now")'
                ],
                'cart_link': [
                    '.cart',
                    '.cart-link',
                    '.cart-icon',
                    'a[href*="/cart"]',
                    '.cart-count'
                ],
                'checkout_button': [
                    '.checkout',
                    '.checkout-button',
                    'button:has-text("Checkout")',
                    'a:has-text("Checkout")'
                ],
                'coupon_field': [
                     '#coupon_code',
                     '#discount-code',
                     'input[name*="coupon"]',
                     'input[name*="discount"]',
                     'input[placeholder*="coupon"]',
                     'input[placeholder*="discount"]',
                     'input[placeholder*="promo"]'
                 ],
                 'coupon_button': [
                    '.action.apply.primary',
                    'button.action.apply',
                    '#discount-coupon-form .action.primary'
                ],
                'coupon_success': [
                    '.message-success',
                    '.messages .success',
                    '.page.messages .message-success'
                ],
                'coupon_error': [
                    '.message-error',
                    '.messages .error',
                    '.page.messages .message-error'
                ],
                'discount_amount': [
                    '.discount .amount',
                    '.discount-amount',
                    '.totals.discount .amount'
                ]
            },
            'woocommerce': {
                'product_grid': [
                    '.products .product',
                    'ul.products li.product',
                    '.wc-block-grid__products .wc-block-grid__product'
                ],
                'add_to_cart': [
                    '.single_add_to_cart_button',
                    '.add_to_cart_button',
                    'button.alt.add_to_cart'
                ],
                'cart_link': [
                    '.cart-contents',
                    '.woocommerce-cart-link',
                    'a.cart-link'
                ],
                'checkout_button': [
                    '.checkout-button',
                    '.wc-proceed-to-checkout .button',
                    'a.checkout-button.button.alt.wc-forward'
                ],
                'coupon_field': [
                    '#coupon_code',
                    '.coupon #coupon_code',
                    'input[name="coupon_code"]'
                ],
                'coupon_button': [
                    'button[name="apply_coupon"]',
                    '.coupon .button',
                    '.coupon button'
                ],
                'coupon_success': [
                    '.woocommerce-message',
                    '.woocommerce-notice--success',
                    '.woocommerce-info:contains("Coupon")'
                ],
                'coupon_error': [
                    '.woocommerce-error',
                    '.woocommerce-notice--error',
                    '.woocommerce-error li'
                ],
                'discount_amount': [
                    '.cart-discount .amount',
                    '.discount-total',
                    'tr.cart-discount td'
                ]
            },
            'shopify': {
                'product_grid': [
                    '.product-grid .grid__item',
                    '.product-card',
                    '.product-list .product-item'
                ],
                'add_to_cart': [
                    '.add-to-cart',
                    '.product-form__submit',
                    'button[name="add"]'
                ],
                'cart_link': [
                    '.cart-link',
                    '.cart-icon-link',
                    'a[href="/cart"]'
                ],
                'checkout_button': [
                    '.checkout-button',
                    'input[name="checkout"]',
                    'button[name="checkout"]'
                ],
                'coupon_field': [
                    '#checkout_reduction_code',
                    '#discount_input',
                    'input[name="discount"]'
                ],
                'coupon_button': [
                    '#checkout_submit',
                    '.order-summary__section--discount button',
                    'button:contains("Apply")'
                ],
                'coupon_success': [
                    '.reduction-code__text',
                    '.applied-reduction-code__information',
                    '.notice--success'
                ],
                'coupon_error': [
                    '.field__message--error',
                    '.error-message',
                    '.notice--error'
                ],
                'discount_amount': [
                    '.reduction-code__amount',
                    '.total-recap__discount-amount',
                    '.discount-tag'
                ]
            },
            'opencart': {
                'product_grid': [
                    '.product-layout',
                    '.product-grid',
                    '.product-thumb'
                ],
                'add_to_cart': [
                    '#button-cart',
                    '.btn-primary:contains("Add to Cart")',
                    'button[onclick*="cart.add"]'
                ],
                'cart_link': [
                    '#cart',
                    '#cart-total',
                    'a[href*="route=checkout/cart"]'
                ],
                'checkout_button': [
                    '.btn-primary:contains("Checkout")',
                    'a[href*="route=checkout/checkout"]',
                    '#button-checkout'
                ],
                'coupon_field': [
                    '#input-coupon',
                    'input[name="coupon"]',
                    '#collapse-coupon input'
                ],
                'coupon_button': [
                    '#button-coupon',
                    '.btn-primary:contains("Apply Coupon")',
                    'input[type="button"][value="Apply Coupon"]'
                ],
                'coupon_success': [
                    '.alert-success',
                    '.alert.alert-success',
                    '.text-success'
                ],
                'coupon_error': [
                    '.alert-danger',
                    '.alert.alert-danger',
                    '.text-danger'
                ],
                'discount_amount': [
                    '#total_coupon',
                    '.coupon-amount',
                    'tr:contains("Coupon") .text-right'
                ]
            },
            'prestashop': {
                'product_grid': [
                    '.product-miniature',
                    '.products .product',
                    '.product_list .ajax_block_product'
                ],
                'add_to_cart': [
                    '.add-to-cart',
                    '.btn.add-to-cart',
                    '#add-to-cart-or-refresh button'
                ],
                'cart_link': [
                    '.cart-preview',
                    '.blockcart',
                    'a[href*="controller=cart"]'
                ],
                'checkout_button': [
                    '.cart-detailed-actions .btn',
                    '.checkout a',
                    'a[href*="controller=order"]'
                ],
                'coupon_field': [
                    '#promo-code input',
                    'input[name="discount_name"]',
                    '.promo-input'
                ],
                'coupon_button': [
                    '.promo-code button',
                    '.promo-code .btn',
                    'button:contains("Add")'
                ],
                'coupon_success': [
                    '.cart-summary-line.promo-code-line',
                    '.alert.alert-success',
                    '.promo-code-success'
                ],
                'coupon_error': [
                    '.alert.alert-danger',
                    '.promo-code-error',
                    '.js-error-text'
                ],
                'discount_amount': [
                    '.cart-summary-line.cart-total .value',
                    '.discount .value',
                    '.discount-price'
                ]
            },
            'bigcommerce': {
                'product_grid': [
                    '.product',
                    '.card',
                    '.productGrid .product'
                ],
                'add_to_cart': [
                    '#form-action-addToCart',
                    '.add-to-cart',
                    'button[data-button-type="add-cart"]'
                ],
                'cart_link': [
                    '.navUser-item--cart',
                    '.cart-icon',
                    'a[href="/cart.php"]'
                ],
                'checkout_button': [
                    '.checkout-button',
                    '.cart-actions .button--primary',
                    'a[href="/checkout.php"]'
                ],
                'coupon_field': [
                    '#couponcode',
                    'input[name="couponcode"]',
                    '.coupon-code-input'
                ],
                'coupon_button': [
                    '.coupon-code-add',
                    'input[value="Apply Coupon"]',
                    'button:contains("Apply Coupon")'
                ],
                'coupon_success': [
                    '.coupon-applied',
                    '.alert-success',
                    '.coupon-code-success'
                ],
                'coupon_error': [
                    '.coupon-error',
                    '.alert-error',
                    '.error-message'
                ],
                'discount_amount': [
                    '.cart-total-value',
                    '.coupon-discount',
                    '.cart-priceItem--promotion'
                ]
            }
        }
    
    async def identify_platform(self, browser_engine) -> Dict:
        """
        Identify the e-commerce platform of the website.
        
        Args:
            browser_engine: The browser engine instance
            
        Returns:
            Dictionary with platform information and selectors
        """
        try:
            # Get page HTML and URL
            html_content = await browser_engine.page.content()
            current_url = await browser_engine.get_current_url()
            
            # Take screenshot for debugging
            await browser_engine.take_screenshot('/tmp/platform_detection.png')
            
            # Check for platform-specific patterns in HTML and URL
            detected_platform = 'unknown'
            confidence_scores = {}
            
            for platform, patterns in self.platform_patterns.items():
                score = 0
                for pattern in patterns:
                    if re.search(pattern, html_content, re.IGNORECASE) or re.search(pattern, current_url, re.IGNORECASE):
                        score += 1
                confidence_scores[platform] = score
            
            # Find platform with highest confidence score
            if confidence_scores:
                max_score = max(confidence_scores.values())
                if max_score > 0:  # Require at least one match
                    for platform, score in confidence_scores.items():
                        if score == max_score:
                            detected_platform = platform
                            break
            
            logger.info(f"Detected platform: {detected_platform} with confidence scores: {confidence_scores}")
            
            # Get platform-specific selectors
            selectors = {}
            if detected_platform in self.platform_selectors:
                selectors = self.platform_selectors[detected_platform]
            
            # Return platform information
            return {
                'platform': detected_platform,
                'confidence_scores': confidence_scores,
                **selectors  # Include all platform-specific selectors
            }
            
        except Exception as e:
            logger.error(f"Error identifying platform: {str(e)}")
            return {'platform': 'unknown', 'error': str(e)}
    
    async def extract_platform_info(self, browser_engine) -> Dict:
        """
        Extract additional platform-specific information.
        
        Args:
            browser_engine: The browser engine instance
            
        Returns:
            Dictionary with additional platform information
        """
        try:
            # First identify the platform
            platform_info = await self.identify_platform(browser_engine)
            
            # Extract additional information based on platform
            if platform_info['platform'] == 'magento':
                # Extract Magento version if available
                magento_version = await browser_engine.execute_javascript("""
                    if (typeof window.magento !== 'undefined') {
                        return window.magento.version || '';
                    }
                    const versionMeta = document.querySelector('meta[name="magento-version"]');
                    if (versionMeta) {
                        return versionMeta.getAttribute('content') || '';
                    }
                    return '';
                """)
                
                if magento_version:
                    platform_info['version'] = magento_version
                    
                # Check if it's Magento 1 or 2
                is_magento2 = await browser_engine.execute_javascript("""
                    return document.querySelector('script[type="text/x-magento-init"]') !== null;
                """)
                
                if is_magento2:
                    platform_info['magento_version'] = 2
                else:
                    platform_info['magento_version'] = 1
                    
            elif platform_info['platform'] == 'woocommerce':
                # Extract WooCommerce version if available
                woo_version = await browser_engine.execute_javascript("""
                    const versionMeta = document.querySelector('meta[name="generator"]');
                    if (versionMeta) {
                        const content = versionMeta.getAttribute('content') || '';
                        const match = content.match(/WooCommerce ([\d.]+)/);
                        if (match && match[1]) {
                            return match[1];
                        }
                    }
                    return '';
                """)
                
                if woo_version:
                    platform_info['version'] = woo_version
                    
            elif platform_info['platform'] == 'shopify':
                # Check if it's using Shopify Plus
                is_shopify_plus = await browser_engine.execute_javascript("""
                    return window.Shopify && window.Shopify.shop && window.Shopify.shop.includes('.myshopify.com');
                """)
                
                if is_shopify_plus:
                    platform_info['shopify_plus'] = True
                    
            # Return enhanced platform information
            return platform_info
            
        except Exception as e:
            logger.error(f"Error extracting platform info: {str(e)}")
            return {'platform': 'unknown', 'error': str(e)}