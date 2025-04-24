from lxml import etree
import argparse

def name_portions(input_path, output_path):
    """
    Assign unique names (IDs) to all portions in the tracks of a Terrain (.rnd) file.

    Args:
        input_path (str): Path to the input .rnd file.
        output_path (str): Path to the output .rnd file.
    """
    try:
        # Parse the input .rnd file
        tree = etree.parse(input_path)
        root = tree.getroot()

        portion_id = 0
        tracks = root.findall('Network/SubNetworks/SubNetwork/RoadNetwork/Tracks/')

        # Name portions in each track
        for track in tracks:
            for portion in track.findall('Portions/Portion'):
                portion.attrib['name'] = str(portion_id)
                portion_id += 1

        # Save the updated .rnd file
        tree.write(output_path, encoding='utf-8', xml_declaration=True, pretty_print=True)
        print(f"Successfully named portions and saved to {output_path}")

    except Exception as e:
        print(f"Error processing file: {e}")

def main():
    parser = argparse.ArgumentParser(description="Terrain file portion naming.")
    parser.add_argument("--input", required=True, type=str, help="Input .rnd file path.")
    parser.add_argument("--output", required=False, type=str, help="Output .rnd file path (defaults to input filename).")
    args = parser.parse_args()

    input = args.input
    output = args.output if args.output else args.input

    name_portions(input, output)

if __name__ == "__main__":
    main()