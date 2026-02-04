from collections import defaultdict
from lxml import etree
import argparse
from typing import Optional, DefaultDict

from utils import (
    load_xml_tree,
    format_xml_output,
    save_xml
)

def get_identifier_tag(element: etree._Element, identifier_tags: tuple = ('name', 'id')) -> Optional[str]:
    """
    Determine which identifier tag ('name' or 'id') the element uses.
    
    Args:
        element: Element to check
        identifier_tags: Tuple of possible identifier tags
        
    Returns:
        Identifier tag name if found, None otherwise
    """
    return next((tag for tag in identifier_tags if element.find(tag) is not None), None)

def is_element_identifiable(element: etree._Element, identifier_tags: tuple = ('name', 'id')) -> bool:
    """
    Check if element has an identifier child (name or id).
    
    Args:
        element: Element to check
        identifier_tags: Tuple of possible identifier tags
        
    Returns:
        True if element has an identifier, False otherwise
    """
    return get_identifier_tag(element, identifier_tags) is not None

def get_element_path(element: etree._Element, root: etree._Element) -> str:
    """
    Build XPath-like path usable with root.find()/findall().
    
    Args:
        element: Element to build path for
        root: Root element to build path relative to
        
    Returns:
        Path string like './Scenario/Vehicle' (root tag omitted)
    """
    parts = []
    current = element
    
    while current is not None and isinstance(current, etree._Element):
        parts.append(current.tag)
        if current is root:
            break
        current = current.getparent()
    
    parts.reverse()
    
    # Remove root tag from path
    if parts and parts[0] == root.tag:
        parts = parts[1:]
    
    return f"./{'/'.join(parts)}" if parts else "."

def update_scenario_element(
    config_element: etree._Element,
    scenario_element: etree._Element,
    identifier_tag: str,
    tag_stats: Optional[DefaultDict[str, int]],
    verbose: bool = True
) -> int:
    """
    Update scenario element's children with values from config element.

    The update runs recursively so nested elements (e.g. Flow/distribution) are
    also synchronized.
    
    Args:
        config_element: Source element from configuration
        scenario_element: Target element in scenario
        identifier_tag: Tag name of the identifier (to skip updating at root)
        tag_stats: Accumulator for tag update counts (path -> count)
        verbose: Whether to print update information
        
    Returns:
        Number of elements updated
    """

    skip_tags = {identifier_tag} if identifier_tag else set()
    return _update_element_recursive(
        config_element,
        scenario_element,
        skip_tags,
        tag_stats,
        verbose,
        config_element.tag,
        depth=0
    )


def _update_element_recursive(
    config_element: etree._Element,
    scenario_element: etree._Element,
    skip_tags: set,
    tag_stats: Optional[DefaultDict[str, int]],
    verbose: bool,
    path: str,
    depth: int
) -> int:
    """Recursively copy text values from config_element into scenario_element."""

    updated_count = 0

    for config_child in config_element:
        if not isinstance(config_child, etree._Element):
            continue

        if depth == 0 and config_child.tag in skip_tags:
            continue

        scenario_child = scenario_element.find(config_child.tag)

        if scenario_child is None:
            continue

        child_path = f"{path}/{config_child.tag}" if path else config_child.tag

        has_element_children = any(isinstance(sub_child, etree._Element) for sub_child in config_child)

        if has_element_children:
            updated_count += _update_element_recursive(
                config_child,
                scenario_child,
                skip_tags,
                tag_stats,
                verbose,
                child_path,
                depth + 1
            )
            continue

        old_text = scenario_child.text
        scenario_child.text = config_child.text
        updated_count += 1

        if tag_stats is not None:
            tag_stats[child_path] += 1

        if verbose:
            print(f"{child_path}: {old_text} -> {config_child.text}\n")

    return updated_count

def merge_configuration_to_scenario(configuration_file: str, scenario_input_file: str, scenario_output_file: str, verbose: bool = True) -> None:
    """
    Merge configuration XML into scenario XML.
    
    Args:
        configuration_file: Path to configuration XML file
        scenario_input_file: Path to input scenario file
        scenario_output_file: Path to output scenario file
        verbose: Whether to print detailed information
        
    Raises:
        Various exceptions from helper functions
    """

    # Configuration constants
    identifier_tags = ('name', 'id')
    self_closing_exceptions = ['Simple', 'Model', 'ScanerNetRecorder', 'UserDataList', 'CustomData', 'Intermediate']
    xml_declaration = '<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>\n'
    encoding = 'UTF-8'
    
    try:
        print(f"Configuration: {configuration_file}")
        _, config_root = load_xml_tree(configuration_file)
        
        print(f"Scenario: {scenario_input_file}")
        _, scenario_root = load_xml_tree(scenario_input_file)
        
        # Process elements
        elements_processed = 0
        elements_updated = 0
        tag_update_counts: DefaultDict[str, int] = defaultdict(int)
        
        print("\nProcessing elements...\n")
        
        for element in config_root.iter():
            
            # Skip non-identifiable elements
            if not is_element_identifiable(element, identifier_tags):
                continue
            
            elements_processed += 1
            element_tag = element.tag
            element_path = get_element_path(element, scenario_root)
            
            # Ground
            if element_tag == 'Ground':
                try:
                    ground_element = scenario_root.find(element_path)
                    if ground_element is not None:
                        ground_element_name = ground_element.find('name')
                        if ground_element_name is not None:
                            ground_element_name_old = ground_element_name.text
                            ground_element_name.text = element.find('name').text
                            elements_updated += 1
                            if verbose:
                                print(f"Ground")
                                print(f"name:{ground_element_name_old} -> {element.find('name').text}\n")
                except AttributeError as e:
                    print(f"Warning: Failed to update Ground element: {e}")
                continue
            
            # Elements in scenario template
            scenario_elements = scenario_root.findall(element_path)
            if not scenario_elements:
                print(f"Warning: No matching elements found in scenario for path: {element_path}")
                continue
            
            # Identifier type
            identifier_tag = get_identifier_tag(element, identifier_tags)
            identifier_value = element.find(identifier_tag).text
            
            # Find by identifier and update
            for scenario_element in scenario_elements:
                scenario_identifier = scenario_element.find(identifier_tag)
                
                if scenario_identifier is None or scenario_identifier.text != identifier_value:
                    continue

                if verbose:
                    print(f"{element_tag}({identifier_tag}={identifier_value})")
                
                children_updated = update_scenario_element(
                    element,
                    scenario_element,
                    identifier_tag,
                    tag_update_counts,
                    verbose
                )
                
                if children_updated > 0:
                    elements_updated += 1
                
                break
        
        # Summary
        print(f"Elements processed: {elements_processed}")
        print(f"Elements updated: {elements_updated}")

        total_field_updates = sum(tag_update_counts.values())
        print(f"Field updates: {total_field_updates}")

        if tag_update_counts:
            print("\nUpdated tag summary:")
            for tag_path in sorted(tag_update_counts):
                print(f"- {tag_path}: {tag_update_counts[tag_path]}")

        # Serialize and format XML
        print("\nSerializing XML...")
        xml_text = etree.tostring(
            scenario_root,
            encoding="unicode",
            xml_declaration=False,
            pretty_print=True
        )
        
        xml_text = format_xml_output(xml_text, self_closing_exceptions)
        
        # Save output
        save_xml(xml_text, scenario_output_file, xml_declaration, encoding)
        
    except Exception as e:
        print(f"Error during processing: {type(e).__name__}: {e}")
        raise


def main():
    parser = argparse.ArgumentParser(description="Merge configuration XML into scenario XML file.")
    parser.add_argument("-c", "--config", required=True, type=str, help="Configuration XML file path.")
    parser.add_argument("-i", "--input", required=True, type=str, help="Input scenario .sce file path.")
    parser.add_argument("-o", "--output", required=False, type=str, help="Output scenario .sce file path (defaults to input filename with _generated suffix).")
    parser.add_argument("-v", "--verbose", action='store_true', help="Print detailed information about changes.")
    
    args = parser.parse_args()
    
    input_file = args.input
    output_file = args.output if args.output else input_file.replace(".sce", "_generated.sce")
    
    try:
        merge_configuration_to_scenario(args.config, input_file, output_file, args.verbose)
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
