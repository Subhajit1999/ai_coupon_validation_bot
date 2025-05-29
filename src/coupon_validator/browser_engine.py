"""Browser Automation Engine
------------------------
Controls browser interactions using Playwright.
"""

import asyncio
import logging
from typing import Dict, Optional, List, Tuple
from playwright.async_api import async_playwright, Browser, Page, BrowserContext, TimeoutError

# Get logger
logger = logging.getLogger(__name__)


class BrowserEngine:
    """Handles browser automation for the coupon validation process."""
    
    def __init__(self, headless: bool = True, timeout: int = 60000):
        """
        Initialize the browser engine.
        
        Args:
            headless: Whether to run browser in headless mode
            timeout: Default timeout for navigation in milliseconds (default: 60000 ms = 60 seconds)
        """
        self.headless = headless
        self.timeout = timeout
        self.browser = None
        self.context = None
        self.page = None
        self.playwright = None
        self.navigation_attempts = 0
        self.max_navigation_attempts = 3
    
    async def start(self) -> bool:
        """
        Start the browser instance with advanced bot detection evasion.
        
        Returns:
            True if browser started successfully, False otherwise
        """
        try:
            self.playwright = await async_playwright().start()
            
            # Enhanced launch settings with randomized fingerprint
            self.browser = await self.playwright.chromium.launch(
                headless=self.headless,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-features=IsolateOrigins,site-per-process',
                    '--disable-site-isolation-trials',
                    '--disable-web-security',
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-gpu',
                    '--disable-software-rasterizer',
                    '--disable-notifications',
                    '--disable-popup-blocking',
                    '--disable-extensions'
                ],
                executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
            )
            
            # Randomized browser fingerprint
            import random
            viewports = [
                {'width': 1366, 'height': 768},
                {'width': 1920, 'height': 1080},
                {'width': 1440, 'height': 900}
            ]
            user_agents = [
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/115.0'
            ]
            timezones = ['America/New_York', 'America/Chicago', 'America/Los_Angeles']
            
            self.context = await self.browser.new_context(
                viewport=random.choice(viewports),
                user_agent=random.choice(user_agents),
                locale='en-US',
                timezone_id=random.choice(timezones),
                has_touch=False,
                java_script_enabled=True,
                ignore_https_errors=True,
                color_scheme='light',
                reduced_motion='reduce',
                permissions=['clipboard-read', 'clipboard-write']
            )
            
            # Enhanced fingerprint randomization script
            await self.context.add_init_script('''
            // Override navigator properties
            // Override multiple browser properties to evade detection
            Object.defineProperty(navigator, 'webdriver', { get: () => false });
            Object.defineProperty(navigator, 'plugins', { 
                get: () => [{
                    name: 'Chrome PDF Viewer',
                    filename: 'internal-pdf-viewer',
                    description: 'Portable Document Format'
                }, {
                    name: 'Chromium PDF Viewer',
                    filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai',
                    description: 'Portable Document Format'
                }]
            });
            Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
            Object.defineProperty(window, 'chrome', { get: () => true });
            
            // Randomize screen properties
            Object.defineProperty(screen, 'width', { get: () => 1920 + Math.floor(Math.random() * 100) });
            Object.defineProperty(screen, 'height', { get: () => 1080 + Math.floor(Math.random() * 100) });
            Object.defineProperty(screen, 'availWidth', { get: () => 1920 + Math.floor(Math.random() * 100) });
            Object.defineProperty(screen, 'availHeight', { get: () => 1080 + Math.floor(Math.random() * 100) });
            
            // Override timing functions
            const originalRandom = Math.random;
            Math.random = () => {
                const base = originalRandom();
                return base > 0.5 ? base - 0.1 : base + 0.1;
            };
                    name: 'Chrome PDF Viewer',
                    filename: 'internal-pdf-viewer',
                    description: 'Portable Document Format'
                }, {
                    name: 'Chromium PDF Viewer',
                    filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai',
                    description: 'Portable Document Format'
                }, {
                    name: 'Microsoft Edge PDF Viewer',
                    filename: 'internal-pdf-viewer',
                    description: 'Portable Document Format'
                }]
            });
            Object.defineProperty(navigator, 'languages', { 
                get: () => ['en-US', 'en'] 
            });
            Object.defineProperty(navigator, 'deviceMemory', { 
                get: () => 8 
            });
            Object.defineProperty(navigator, 'hardwareConcurrency', { 
                get: () => 4 
            });
            
            // Override screen properties
            Object.defineProperty(screen, 'width', { get: () => window.screen.width });
            Object.defineProperty(screen, 'height', { get: () => window.screen.height });
            Object.defineProperty(screen, 'availWidth', { get: () => window.screen.availWidth });
            Object.defineProperty(screen, 'availHeight', { get: () => window.screen.availHeight });
            Object.defineProperty(screen, 'colorDepth', { get: () => 24 });
            Object.defineProperty(screen, 'pixelDepth', { get: () => 24 });
            
            // Override other common detection points
            window.chrome = {
                app: {
                    isInstalled: false,
                },
                webstore: {
                    onInstallStageChanged: {},
                    onDownloadProgress: {},
                },
                runtime: {
                    PlatformOs: {
                        MAC: 'mac',
                        WIN: 'win',
                        ANDROID: 'android',
                        CROS: 'cros',
                        LINUX: 'linux',
                        OPENBSD: 'openbsd',
                    },
                    PlatformArch: {
                        ARM: 'arm',
                        X86_32: 'x86-32',
                        X86_64: 'x86-64',
                    },
                    PlatformNaclArch: {
                        ARM: 'arm',
                        X86_32: 'x86-32',
                        X86_64: 'x86-64',
                    },
                    RequestUpdateCheckStatus: {
                        THROTTLED: 'throttled',
                        NO_UPDATE: 'no_update',
                        UPDATE_AVAILABLE: 'update_available',
                    },
                    OnInstalledReason: {
                        INSTALL: 'install',
                        UPDATE: 'update',
                        CHROME_UPDATE: 'chrome_update',
                        SHARED_MODULE_UPDATE: 'shared_module_update',
                    },
                    OnRestartRequiredReason: {
                        APP_UPDATE: 'app_update',
                        OS_UPDATE: 'os_update',
                        PERIODIC: 'periodic',
                    },
                },
            };
            
            // Randomize Math.random seed
            Math.random = function() {
                const seed = Date.now() % 1000000;
                return function() {
                    seed = (seed * 9301 + 49297) % 233280;
                    return seed / 233280;
                };
            }();
            ''')
            
            self.page = await self.context.new_page()
            await self.page.set_default_timeout(self.timeout)
            
            # Set up event listeners for console messages
            self.page.on("console", lambda msg: logger.debug(f"Browser console {msg.type}: {msg.text}"))
            
            logger.info("Browser started successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to start browser: {str(e)}")
            return False
    
    async def navigate(self, url: str, wait_until='networkidle', timeout=None) -> bool:
        """
        Navigate to a URL with advanced retry logic and bot detection handling.
        
        Args:
            url: The URL to navigate to
            wait_until: When to consider navigation succeeded
                        One of: 'load', 'domcontentloaded', 'networkidle'
            timeout: Timeout for this specific navigation in milliseconds
            
        Returns:
            True if navigation was successful, False otherwise
        """
        if not self.page:
            logger.error("Browser not started. Call start() first.")
            return False
            
        if timeout is None:
            timeout = self.timeout
        
        # Ensure the URL has a protocol
        if not url.startswith('http'):
            url = 'https://' + url
            
        # Enhanced navigation strategies with exponential backoff and varied approaches
        strategies = [
            {'wait_until': wait_until, 'timeout': timeout, 'delay': 0, 'method': 'normal'},
            {'wait_until': 'domcontentloaded', 'timeout': timeout, 'delay': 2, 'method': 'normal'},
            {'wait_until': 'load', 'timeout': timeout, 'delay': 4, 'method': 'normal'},
            {'wait_until': None, 'timeout': timeout, 'delay': 8, 'method': 'reload'},
            {'wait_until': None, 'timeout': timeout * 2, 'delay': 16, 'method': 'new_tab'}
        ]
        
        # Track navigation metrics
        navigation_metrics = {
            'attempts': 0,
            'success': False,
            'errors': [],
            'response_status': None,
            'content_checks': []
        }
        
        for i, strategy in enumerate(strategies):
            navigation_metrics['attempts'] += 1
            current_wait = strategy['wait_until']
            current_timeout = strategy['timeout']
            
            try:
                logger.info(f"Navigation attempt {i+1}/{len(strategies)} to {url}" + 
                          (f" with strategy: {current_wait}" if current_wait else " with no wait_until strategy") +
                          f" using method: {strategy['method']}")
                
                # Simulate human-like behavior with randomized delays
                if strategy['delay'] > 0:
                    delay = strategy['delay'] + random.uniform(-1, 1)
                    await asyncio.sleep(delay)
                
                # Random mouse movement before navigation
                await self.page.mouse.move(
                    random.randint(0, 100),
                    random.randint(0, 100)
                )
                
                # Try different navigation methods based on strategy
                response = None
                if strategy['method'] == 'normal':
                    response = await self.page.goto(
                        url,
                        wait_until=current_wait,
                        timeout=current_timeout,
                        referer='https://www.google.com/'
                    )
                elif strategy['method'] == 'reload':
                    # First try normal navigation
                    try:
                        response = await self.page.goto(url, timeout=current_timeout)
                    except:
                        pass
                    # Then reload with different options
                    response = await self.page.reload(wait_until=current_wait, timeout=current_timeout)
                elif strategy['method'] == 'new_tab':
                    # Open new tab and close old one
                    new_page = await self.context.new_page()
                    await self.page.close()
                    self.page = new_page
                    response = await self.page.goto(url, timeout=current_timeout)
                
                # Store response status
                navigation_metrics['response_status'] = response.status if response else None
                
                if response and response.status >= 400:
                    logger.warning(f"Navigation attempt {i+1} failed with status: {response.status}")
                    navigation_metrics['errors'].append(f"HTTP {response.status}")
                    continue
                
                # Wait for page to stabilize with randomized delay
                await asyncio.sleep(3 + random.uniform(0, 2))
                
                # Enhanced content verification with more lenient thresholds
                content_check = await self.execute_javascript("""
                    return {
                        bodyExists: !!document.body,
                        contentLength: document.body ? document.body.innerHTML.length : 0,
                        hasLinks: document.querySelectorAll('a').length > 0,
                        hasImages: document.querySelectorAll('img').length > 0,
                        hasForms: document.querySelectorAll('form').length > 0,
                        title: document.title,
                        isVisible: document.visibilityState === 'visible',
                        isInteractive: document.readyState === 'complete'
                    }
                """)
                navigation_metrics['content_checks'].append(content_check)
                
                if not content_check.get('bodyExists') or content_check.get('contentLength', 0) < 100:
                    logger.warning(f"Page content appears insufficient on attempt {i+1}")
                    navigation_metrics['errors'].append("Insufficient content")
                    continue
                
                # Advanced bot detection checks with more comprehensive detection
                bot_check = await self.execute_javascript("""
                    return {
                        hasCaptcha: document.body.innerHTML.includes('captcha') || 
                                   document.querySelector('[aria-label*="captcha"]') ||
                                   document.querySelector('iframe[src*="recaptcha"]'),
                        hasAccessDenied: document.body.innerHTML.includes('access denied') ||
                                        document.querySelector('h1:contains("Access Denied")') ||
                                        document.querySelector('h1:contains("Blocked")'),
                        hasCloudflare: document.querySelector('#cf-challenge-wrapper') ||
                                       document.querySelector('.cf-browser-verification') ||
                                       document.querySelector('.ray_id'),
                        hasBotDetection: document.querySelector('meta[name="robots"]')?.content === 'noindex,nofollow' ||
                                         document.querySelector('meta[name="googlebot"]')?.content === 'noindex,nofollow' ||
                                         document.querySelector('meta[name="security"]')
                    }
                """)
                
                if any(bot_check.values()):
                    logger.warning(f"Bot detection encountered on attempt {i+1}: {bot_check}")
                    navigation_metrics['errors'].append("Bot detection triggered")
                    
                    # Try to bypass simple bot detection
                    if bot_check.get('hasCloudflare'):
                        await self._handle_cloudflare_challenge()
                        continue
                    
                    if bot_check.get('hasCaptcha'):
                        await self._handle_captcha_challenge()
                        continue
                    
                    continue
                
                logger.info(f"Successfully navigated to {url} on attempt {i+1}")
                navigation_metrics['success'] = True
                return True
                
            except Exception as e:
                error_msg = f"Navigation attempt {i+1} failed: {str(e)}"
                logger.warning(error_msg)
                navigation_metrics['errors'].append(error_msg)
                
        logger.error(f"All navigation attempts to {url} failed. Metrics: {navigation_metrics}")
        return False
    
    async def click(self, selector: str, timeout: int = None, force: bool = False, retry: bool = True) -> bool:
        """
        Click on an element with retry logic.
        
        Args:
            selector: CSS selector for the element to click
            timeout: Optional timeout override in milliseconds
            force: Whether to force the click regardless of element state
            retry: Whether to retry the click if it fails
            
        Returns:
            True if click was successful, False otherwise
        """
        if not self.page:
            logger.error("Browser not started. Call start() first.")
            return False
        
        try:
            if timeout is None:
                timeout = self.timeout
                
            # First try to wait for the element to be visible
            await self.page.wait_for_selector(selector, state='visible', timeout=timeout)
            
            # Then click it
            await self.page.click(selector, force=force, timeout=timeout)
            
            # Wait a bit for any resulting page changes
            await asyncio.sleep(1)
            
            logger.info(f"Successfully clicked element: {selector}")
            return True
        except Exception as e:
            logger.warning(f"Standard click failed on {selector}: {str(e)}")
            
            if not retry:
                return False
                
            # Try alternative click methods
            try:
                # Try to scroll element into view first
                await self.execute_javascript(f'''
                    (() => {{  
                        const element = document.querySelector('{selector}');
                        if (element) {{  
                            element.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
                            return true;
                        }}
                        return false;
                    }})()''')
                
                # Wait a moment for scroll to complete
                await asyncio.sleep(0.5)
                
                # Try clicking again
                await self.page.click(selector, timeout=timeout, force=True)
                return True
            except Exception as e2:
                logger.warning(f"Retry click failed on {selector}: {str(e2)}")
                
                # Last resort: Try JavaScript click
                try:
                    await self.execute_javascript(f'''
                        (() => {{  
                            const element = document.querySelector('{selector}');
                            if (element) {{  
                                element.click();
                                return true;
                            }}
                            return false;
                        }})()''')
                    
                    # Check if click had an effect (page changed or new elements appeared)
                    await asyncio.sleep(1)
                    return True
                except Exception as e3:
                    logger.error(f"All click methods failed on {selector}: {str(e3)}")
                    return False
    
    async def fill(self, selector: str, value: str, timeout: int = None, retry: bool = True) -> bool:
        """
        Fill a form field with retry logic.
        
        Args:
            selector: CSS selector for the input field
            value: Value to fill in the field
            timeout: Optional timeout override in milliseconds
            retry: Whether to retry with alternative methods if standard fill fails
            
        Returns:
            True if fill was successful, False otherwise
        """
        if not self.page:
            logger.error("Browser not started. Call start() first.")
            return False
        
        try:
            if timeout is None:
                timeout = self.timeout
                
            # First try to wait for the element to be visible
            await self.page.wait_for_selector(selector, state='visible', timeout=timeout)
            
            # Clear the field first
            await self.page.fill(selector, "", timeout=timeout)
            
            # Then fill it
            await self.page.fill(selector, value, timeout=timeout)
            
            logger.info(f"Successfully filled field {selector} with value {value}")
            return True
        except Exception as e:
            logger.warning(f"Standard fill failed on {selector}: {str(e)}")
            
            if not retry:
                return False
                
            # Try alternative fill methods
            try:
                # Try to scroll element into view first
                await self.execute_javascript(f'''
                    (() => {{  
                        const element = document.querySelector('{selector}');
                        if (element) {{  
                            element.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
                            return true;
                        }}
                        return false;
                    }})()''')
                
                # Wait a moment for scroll to complete
                await asyncio.sleep(0.5)
                
                # Try filling again
                await self.page.fill(selector, value, timeout=timeout)
                return True
            except Exception as e2:
                logger.warning(f"Retry fill failed on {selector}: {str(e2)}")
                
                # Last resort: Try JavaScript to set value
                try:
                    escaped_value = value.replace("'", "\\'").replace('"', '\\"')
                    await self.execute_javascript(f'''
                        (() => {{  
                            const element = document.querySelector('{selector}');
                            if (element) {{  
                                element.value = '{escaped_value}';
                                element.dispatchEvent(new Event('input', {{ bubbles: true }}));
                                element.dispatchEvent(new Event('change', {{ bubbles: true }}));
                                return true;
                            }}
                            return false;
                        }})()''')
                    
                    return True
                except Exception as e3:
                    logger.error(f"All fill methods failed on {selector}: {str(e3)}")
                    return False
    
    async def press_key(self, selector: str, key: str, timeout: int = None) -> bool:
        """
        Press a key on an element.
        
        Args:
            selector: CSS selector for the element
            key: Key to press (e.g., 'Enter')
            timeout: Optional timeout override in milliseconds
            
        Returns:
            True if key press was successful, False otherwise
        """
        if not self.page:
            logger.error("Browser not started. Call start() first.")
            return False
        
        try:
            if timeout is None:
                timeout = self.timeout
                
            # First try to wait for the element to be visible
            await self.page.wait_for_selector(selector, state='visible', timeout=timeout)
            
            # Focus the element
            await self.page.focus(selector, timeout=timeout)
            
            # Press the key
            await self.page.press(selector, key, timeout=timeout)
            
            # Wait a bit for any resulting page changes
            await asyncio.sleep(1)
            
            logger.info(f"Successfully pressed {key} on element {selector}")
            return True
        except Exception as e:
            logger.error(f"Failed to press {key} on element {selector}: {str(e)}")
            return False
    
    async def get_text(self, selector: str, timeout: int = None) -> Optional[str]:
        """
        Get text content of an element.
        
        Args:
            selector: CSS selector for the element
            timeout: Optional timeout override in milliseconds
            
        Returns:
            Text content of the element or None if not found
        """
        if not self.page:
            logger.error("Browser not started. Call start() first.")
            return None
        
        try:
            if timeout is None:
                timeout = self.timeout
                
            # Wait for the element to be visible
            await self.page.wait_for_selector(selector, state='visible', timeout=timeout)
            
            # Get the text content
            text = await self.page.text_content(selector, timeout=timeout)
            
            logger.info(f"Successfully got text from element {selector}: {text}")
            return text
        except Exception as e:
            logger.error(f"Failed to get text from element {selector}: {str(e)}")
            return None
    
    async def is_visible(self, selector: str, timeout: int = 5000) -> bool:
        """
        Check if an element is visible.
        
        Args:
            selector: CSS selector for the element
            timeout: Timeout in milliseconds (shorter than default for efficiency)
            
        Returns:
            True if element is visible, False otherwise
        """
        if not self.page:
            logger.error("Browser not started. Call start() first.")
            return False
        
        try:
            # Use a shorter timeout for visibility checks
            await self.page.wait_for_selector(selector, state='visible', timeout=timeout)
            return True
        except Exception:
            return False
    
    async def get_current_url(self) -> Optional[str]:
        """
        Get the current page URL.
        
        Returns:
            Current URL or None if browser not started
        """
        if not self.page:
            logger.error("Browser not started. Call start() first.")
            return None
        
        return self.page.url
    
    async def execute_javascript(self, script: str, *args, retry: bool = True) -> Optional[any]:
        """
        Execute JavaScript in the page context with retry logic.
        
        Args:
            script: JavaScript code to execute
            *args: Arguments to pass to the script
            retry: Whether to retry with a delay if evaluation fails
            
        Returns:
            Result of the script execution or None if failed
        """
        if not self.page:
            logger.error("Browser not started. Call start() first.")
            return None
        
        try:
            result = await self.page.evaluate(script, *args)
            return result
        except Exception as e:
            if not retry:
                logger.error(f"Failed to execute JavaScript: {str(e)}")
                return None
                
            # Wait a moment and retry once
            try:
                logger.warning(f"JavaScript evaluation failed, retrying: {str(e)}")
                await asyncio.sleep(1)
                result = await self.page.evaluate(script, *args)
                return result
            except Exception as e2:
                logger.error(f"JavaScript evaluation retry failed: {str(e2)}")
                return None
    
    async def take_screenshot(self, path: str) -> bool:
        """
        Take a screenshot of the current page.
        
        Args:
            path: File path to save the screenshot
            
        Returns:
            True if screenshot was taken successfully, False otherwise
        """
        if not self.page:
            logger.error("Browser not started. Call start() first.")
            return False
        
        try:
            await self.page.screenshot(path=path, full_page=True)
            logger.info(f"Screenshot saved to {path}")
            return True
        except Exception as e:
            logger.error(f"Failed to take screenshot: {str(e)}")
            return False
    
    async def get_html_content(self) -> Optional[str]:
        """
        Get the full HTML content of the current page.
        
        Returns:
            HTML content as string or None if failed
        """
        if not self.page:
            logger.error("Browser not started. Call start() first.")
            return None
        
        try:
            content = await self.page.content()
            return content
        except Exception as e:
            logger.error(f"Failed to get HTML content: {str(e)}")
            return None
    
    async def wait_for_navigation(self, timeout: int = None) -> bool:
        """
        Wait for navigation to complete.
        
        Args:
            timeout: Optional timeout override in milliseconds
            
        Returns:
            True if navigation completed, False if timed out
        """
        if not self.page:
            logger.error("Browser not started. Call start() first.")
            return False
        
        try:
            if timeout is None:
                timeout = self.timeout
                
            await self.page.wait_for_load_state('networkidle', timeout=timeout)
            return True
        except Exception as e:
            logger.error(f"Navigation timeout: {str(e)}")
            return False
    
    async def close(self):
        """
        Close the browser and clean up resources.
        """
        try:
            if self.page:
                await self.page.close()
                self.page = None
                
            if self.context:
                await self.context.close()
                self.context = None
                
            if self.browser:
                await self.browser.close()
                self.browser = None
                
            if self.playwright:
                await self.playwright.stop()
                self.playwright = None
                
            logger.info("Browser closed successfully")
        except Exception as e:
            logger.error(f"Error closing browser: {str(e)}")