"""Utility functions for XML processing and manipulation."""

from pathlib import Path
from lxml import etree
import re

def load_xml_tree(file_path: str) -> tuple[etree._ElementTree, etree._Element]:
    """
    Load and parse an XML file.
    
    Args:
        file_path: Path to the XML file
        
    Returns:
        Tuple of (tree, root) elements
        
    Raises:
        FileNotFoundError: If file doesn't exist
        etree.XMLSyntaxError: If XML is malformed
    """
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"XML file not found: {file_path}")
    
    try:
        tree = etree.parse(str(path))
        root = tree.getroot()
        return tree, root
    except etree.XMLSyntaxError as e:
        raise etree.XMLSyntaxError(f"Invalid XML in {file_path}: {e}")

def format_xml_output(xml_text: str, self_closing_exceptions: list) -> str:
    """
    Format XML output with custom rules.
    
    Args:
        xml_text: XML string to format
        self_closing_exceptions: List of tags that should remain self-closing
        
    Returns:
        Formatted XML string
    """
    # Reorder attributes: version before xmlns:xsi
    xml_text = re.sub(
        r'<sce\s+xmlns:xsi="([^"]+)"\s+version="([^"]+)">',
        r'<sce version="\2" xmlns:xsi="\1">',
        xml_text,
        count=1
    )
    
    # Convert self-closing tags to full tags (except for exceptions)
    exceptions_pattern = '|'.join(re.escape(tag) for tag in self_closing_exceptions)
    xml_text = re.sub(
        rf"<(?!{exceptions_pattern}\b)([A-Za-z_][\w:.-]*)(\s[^<>]*?)?\/>",
        lambda m: f"<{m.group(1)}{m.group(2) or ''}></{m.group(1)}>",
        xml_text
    )
    
    return xml_text

def save_xml(content: str, file_path: str, declaration: str, encoding: str = 'UTF-8') -> None:
    """
    Save XML content to file with custom declaration.
    
    Args:
        content: XML content string
        file_path: Output file path
        declaration: XML declaration string
        encoding: File encoding
        
    Raises:
        IOError: If file cannot be written
    """
    try:
        output_path = Path(file_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding=encoding, newline='\n') as f:
            f.write(declaration)
            f.write(content)
            
        print(f"Saved to: {file_path}")
    except IOError as e:
        raise IOError(f"Failed to write output file {file_path}: {e}")
