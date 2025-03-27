from lxml import etree
import argparse
import json

def get_track_connections(tracks):
    track_connections = dict()

    for track in tracks:
        track_name = track.attrib['name']
        if track_name not in track_connections:
            track_connections[track_name] = {'endNode': track.attrib['endNode'], 'startNode': track.attrib['startNode']}
    
    return track_connections

def main():

    tree = etree.parse(input)
    root = tree.getroot()

    tracks = root.findall('Network/SubNetworks/SubNetwork/RoadNetwork/Tracks/Track')
    track_connections = get_track_connections(tracks)

    data = dict()
    portion_id = 0

    for track in tracks:

        track_name = track.attrib['name']
        track_length = 0
        portions = track.findall('Portions/Portion')

        # Handle Abscissa orientation
        connected_intersection = track_connections[track_name]['startNode']
        connected_tracks = [track for track, c in track_connections.items() if c['endNode'] == connected_intersection]

        last_portion_abscissa = 0
        portions_data = dict()
        
        for portion in portions:
            portion_enddistance = float(portion.attrib['endDistance'])
            portion_length = portion_enddistance - last_portion_abscissa
            last_portion_abscissa = portion_enddistance
            track_length += portion_length

            portion_lanes = portion.find('Profile').findall('Lane')
            portion_laneborder_distances = [float(laneborder.attrib['distance']) for laneborder in portion.find('Profile').findall('LaneBorder')]

            lane_centers = [(portion_laneborder_distances[i] + portion_laneborder_distances[i+1]) / 2 for i in range(len(portion_laneborder_distances) - 1)]

            lanes = dict()
            for l in range(len(portion_lanes)):
                if portion_lanes[l].attrib['type'] not in lane_types:
                    continue
                lanes[l] = {
                    "type": portion_lanes[l].attrib['type'],
                    "vehicle_types" : portion_lanes[l].find('VehicleType').attrib['categories'].split(","),
                    "circulationWay": portion_lanes[l].attrib['circulationWay'],
                    "speedLimit": round(float(portion_lanes[l].attrib['speedLimit']), 2),
                    "center": round(lane_centers[l], 2)
                }

            portions_data[portion_id] = {
                "length": round(portion_length, 2),
                "abscissa": round(portion_enddistance, 2),
                "lanes": lanes
            }
            
            portion_id += 1

        data[track_name] = {
            "connected_to": connected_tracks,
            "length": round(track_length, 2),
            "portions": portions_data
        }

    with open(output, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

default_lane_types = [
    'paved express',
    'paved entry',
    'paved',
    'emergency'
    ]

parser = argparse.ArgumentParser(description="Terrain file data extraction script.")
parser.add_argument("--input", required=True, type=str, help="Input .rnd file path.")
parser.add_argument("--output", required=False, type=str, help="Output .json file path (defaults to input filename with .json extension).")
parser.add_argument("--lane_types", required=False, nargs='+', type=str, help="List of lane types to generate positions on (e.g., 'paved express' 'paved entry'). Default: paved express, paved entry, paved, emergency")
args = parser.parse_args()

input = args.input
output = args.output if args.output else input.replace(".rnd", ".json")
lane_types = args.lane_types if args.lane_types else default_lane_types

if __name__ == "__main__":    
    main()