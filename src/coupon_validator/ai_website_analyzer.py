"""AI Website Analyzer Module
--------------------------------
Uses machine learning to analyze website structure and improve coupon validation.
"""

import logging
import numpy as np
from transformers import AutoTokenizer, AutoModel
from typing import Dict, List, Optional, Tuple, Any
import re
import os
import torch

# Configure logging
logger = logging.getLogger(__name__)

class AIWebsiteAnalyzer:
    """Uses machine learning to analyze website structure and improve coupon validation."""
    
    def __init__(self):
        """Initialize the AI website analyzer."""
        self.model_loaded = False
        self.tokenizer = None
        self.model = None
        self.element_embeddings = {}
        self.platform_embeddings = {}
        
        # Common element types to detect
        self.element_types = [
            'coupon_field',
            'coupon_button',
            'checkout_button',
            'cart_link',
            'add_to_cart',
            'product_grid',
            'coupon_success',
            'coupon_error',
            'discount_amount'
        ]
        
        # Initialize model directory
        self.model_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'models')
        os.makedirs(self.model_dir, exist_ok=True)
    
    async def load_model(self):
        """Load the pre-trained model for element detection."""
        try:
            if self.model_loaded:
                return True
                
            logger.info("Loading AI model for website analysis...")
            
            # Use a smaller, more efficient model for deployment
            model_name = "distilbert-base-uncased"
            
            # Load tokenizer and model
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModel.from_pretrained(model_name)
            
            # Initialize element embeddings
            self._initialize_embeddings()
            
            self.model_loaded = True
            logger.info("AI model loaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error loading AI model: {str(e)}")
            return False
    
    def _initialize_embeddings(self):
        """Initialize embeddings for common e-commerce elements."""
        # Generate embeddings for common element types
        for element_type in self.element_types:
            # Convert element type to descriptive text
            element_desc = element_type.replace('_', ' ')
            
            # Generate embedding
            embedding = self._generate_embedding(element_desc)
            self.element_embeddings[element_type] = embedding
        
        # Generate embeddings for common e-commerce platforms
        platforms = ['magento', 'woocommerce', 'shopify', 'opencart', 'prestashop', 'bigcommerce']
        for platform in platforms:
            embedding = self._generate_embedding(platform)
            self.platform_embeddings[platform] = embedding
    
    def _generate_embedding(self, text: str) -> np.ndarray:
        """Generate embedding for a text description."""
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=128)
        with torch.no_grad():
            outputs = self.model(**inputs)[0]
        
        # Use mean pooling to get a fixed-size representation
        embedding = torch.mean(outputs, dim=1)
        return embedding.numpy()[0]
    
    async def analyze_website_structure(self, browser_engine, html_content: str = None) -> Dict:
        """Analyze website structure using AI to identify elements and platform.
        
        Args:
            browser_engine: The browser engine instance
            html_content: Optional HTML content (if None, will be fetched from browser)
            
        Returns:
            Dictionary with AI-detected elements and confidence scores
        """
        try:
            # Ensure model is loaded
            if not self.model_loaded:
                await self.load_model()
            
            # Get HTML content if not provided
            if html_content is None:
                html_content = await browser_engine.get_html_content()
            
            # Extract elements from HTML
            elements = self._extract_elements(html_content)
            
            # Analyze elements using AI
            ai_results = self._analyze_elements(elements)
            
            # Take screenshot for debugging
            await browser_engine.take_screenshot('/tmp/ai_analysis.png')
            
            logger.info(f"AI analysis completed with {len(ai_results['detected_elements'])} elements detected")
            return ai_results
            
        except Exception as e:
            logger.error(f"Error in AI website analysis: {str(e)}")
            return {'error': str(e), 'detected_elements': {}}
    
    def _extract_elements(self, html_content: str) -> List[Dict]:
        """Extract potential elements from HTML content."""
        elements = []
        
        # Extract input fields
        input_pattern = r'<input[^>]*>'
        for match in re.finditer(input_pattern, html_content):
            input_html = match.group(0)
            element = {
                'html': input_html,
                'type': 'input',
                'id': self._extract_attribute(input_html, 'id'),
                'name': self._extract_attribute(input_html, 'name'),
                'class': self._extract_attribute(input_html, 'class'),
                'placeholder': self._extract_attribute(input_html, 'placeholder')
            }
            elements.append(element)
        
        # Extract buttons
        button_pattern = r'<button[^>]*>.*?</button>'
        for match in re.finditer(button_pattern, html_content, re.DOTALL):
            button_html = match.group(0)
            element = {
                'html': button_html,
                'type': 'button',
                'id': self._extract_attribute(button_html, 'id'),
                'name': self._extract_attribute(button_html, 'name'),
                'class': self._extract_attribute(button_html, 'class'),
                'text': self._extract_text(button_html)
            }
            elements.append(element)
        
        # Extract links
        link_pattern = r'<a[^>]*>.*?</a>'
        for match in re.finditer(link_pattern, html_content, re.DOTALL):
            link_html = match.group(0)
            element = {
                'html': link_html,
                'type': 'link',
                'id': self._extract_attribute(link_html, 'id'),
                'href': self._extract_attribute(link_html, 'href'),
                'class': self._extract_attribute(link_html, 'class'),
                'text': self._extract_text(link_html)
            }
            elements.append(element)
        
        return elements
    
    def _extract_attribute(self, html: str, attribute: str) -> str:
        """Extract attribute value from HTML element."""
        pattern = f'{attribute}=["\']([^"\']*)["\']'
        match = re.search(pattern, html)
        return match.group(1) if match else ""
    
    def _extract_text(self, html: str) -> str:
        """Extract text content from HTML element."""
        # Remove HTML tags
        text = re.sub(r'<[^>]*>', '', html)
        return text.strip()
    
    def _analyze_elements(self, elements: List[Dict]) -> Dict:
        """Analyze extracted elements using AI model."""
        results = {
            'detected_elements': {},
            'confidence_scores': {}
        }
        
        for element_type in self.element_types:
            best_match = None
            best_score = 0
            
            for element in elements:
                # Create a description of the element
                element_desc = f"{element['type']} "
                if element.get('id'):
                    element_desc += f"id={element['id']} "
                if element.get('class'):
                    element_desc += f"class={element['class']} "
                if element.get('name'):
                    element_desc += f"name={element['name']} "
                if element.get('placeholder'):
                    element_desc += f"placeholder={element['placeholder']} "
                if element.get('text'):
                    element_desc += f"text={element['text']} "
                
                # Generate embedding for this element
                element_embedding = self._generate_embedding(element_desc)
                
                # Calculate similarity with target element type
                target_embedding = self.element_embeddings[element_type]
                similarity = self._calculate_similarity(element_embedding, target_embedding)
                
                if similarity > best_score:
                    best_score = similarity
                    best_match = element
            
            # Only include if confidence is above threshold
            if best_score > 0.7 and best_match is not None:
                results['detected_elements'][element_type] = best_match
                results['confidence_scores'][element_type] = float(best_score)
        
        return results
    
    def _calculate_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """Calculate cosine similarity between two embeddings."""
        # Normalize embeddings
        norm1 = np.linalg.norm(embedding1)
        norm2 = np.linalg.norm(embedding2)
        
        if norm1 == 0 or norm2 == 0:
            return 0
        
        # Calculate cosine similarity
        return np.dot(embedding1, embedding2) / (norm1 * norm2)
    
    async def get_element_selectors(self, browser_engine, element_type: str) -> List[str]:
        """Get CSS selectors for a specific element type using AI analysis.
        
        Args:
            browser_engine: The browser engine instance
            element_type: Type of element to find selectors for
            
        Returns:
            List of CSS selectors for the element type
        """
        try:
            # Analyze website structure
            analysis = await self.analyze_website_structure(browser_engine)
            
            if element_type not in analysis['detected_elements']:
                logger.warning(f"Element type '{element_type}' not detected by AI")
                return []
            
            element = analysis['detected_elements'][element_type]
            selectors = []
            
            # Generate CSS selectors based on element attributes
            if element.get('id'):
                selectors.append(f"#{element['id']}")
            
            if element.get('class'):
                class_names = element['class'].split()
                if len(class_names) > 0:
                    selectors.append(f".{class_names[0]}")
                    if len(class_names) > 1:
                        selectors.append(f".{class_names[0]}.{class_names[1]}")
            
            if element.get('name'):
                selectors.append(f"{element['type']}[name='{element['name']}']")
            
            if element.get('placeholder'):
                selectors.append(f"{element['type']}[placeholder*='{element['placeholder']}']")
            
            if element.get('text') and len(element.get('text', '')) < 50:  # Only use text if it's reasonably short
                text = element['text'].strip()
                if text:
                    selectors.append(f"{element['type']}:contains('{text}')")
            
            logger.info(f"AI generated {len(selectors)} selectors for {element_type}")
            return selectors
            
        except Exception as e:
            logger.error(f"Error generating selectors: {str(e)}")
            return []
