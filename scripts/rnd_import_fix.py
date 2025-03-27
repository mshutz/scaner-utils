from lxml import etree
import argparse

def main():

    tree = etree.parse(input)
    root = tree.getroot()

    intersections = root.findall('Network/SubNetworks/SubNetwork/RoadNetwork/Intersections/')
    tracks = root.findall('Network/SubNetworks/SubNetwork/RoadNetwork/Tracks/')

    # Remove all authorizations in all intersections
    for intersection in intersections:
        banned_links = intersection.find('BannedLinks')
        for lane_pair in banned_links.findall('LanePair'):
            banned_links.remove(lane_pair)

    # Name lanes
    for track in tracks:
        for portion in track.findall('Portions/Portion'):
            for profile in portion.findall('Profile'):
                lane_name_counter = 1
                for lane in profile.findall('Lane'):
                    lane.attrib['name'] = f'Lane {lane_name_counter}'
                    lane_name_counter += 1

    # Save updated xml
    tree.write(output, encoding='utf-8', xml_declaration=True, pretty_print=True)

parser = argparse.ArgumentParser(description="Terrain file lane naming and removal of links in intersections.")
parser.add_argument("--input", required=True, type=str, help="Input .rnd file path.")
parser.add_argument("--output", required=False, type=str, help="Output .rnd file path (defaults to input filename).")
args = parser.parse_args()

input = args.input
output = args.output if args.output else args.input

if __name__ == "__main__":    
    main()