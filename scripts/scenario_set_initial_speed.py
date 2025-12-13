from lxml import etree
import argparse


def set_initial_speed(input_file, output_file, initial_speed, swarm_only, verbose):
    """
    Set initial speed for vehicles in a scenario file.
    
    Args:
        input_file: Path to input .sce file
        output_file: Path to output .sce file
        initial_speed: Initial speed value in km/h
        swarm_only: If True, only modify swarm vehicles (vehicles with "[" in name)
        verbose: If True, print detailed information about changes
    """
    tree = etree.parse(input_file)
    root = tree.getroot()

    vehicles = root.findall('Scenario/Vehicle')
    vehicles_changed_counter = 0

    for vehicle in vehicles:
        vehicle_name = vehicle.find('name').text
        vehicle_initial_speed = vehicle.find('initialSpeed')

        if swarm_only and "[" in vehicle_name:
            continue

        if not swarm_only and "[" in vehicle_name:
            continue

        if vehicle_initial_speed is not None:
            vehicle_initial_speed_value = float(vehicle_initial_speed.text) * 3.6
            vehicle_initial_speed.text = str(initial_speed / 3.6)
            vehicles_changed_counter += 1

            if verbose:
                print(f"{vehicle_initial_speed_value:.2f} > {initial_speed} {vehicle_name}")

    print(f"\nTotal vehicles with initial speed set: {vehicles_changed_counter}")

    tree.write(output_file, encoding='utf-8', xml_declaration=True, pretty_print=True)


def main():
    parser = argparse.ArgumentParser(description="Set initial speed for vehicles in a scenario file.")
    parser.add_argument("-i", "--input", required=True, type=str, help="Input .sce file path.")
    parser.add_argument("-o", "--output", required=False, type=str, help="Output .sce file path (defaults to input filename with _initial_speed_set suffix).")
    parser.add_argument("-s", "--speed", required=True, type=float, help="Initial speed value in km/h.")
    parser.add_argument("-w", "--swarm_only", action='store_true', help="Only modify non-swarm vehicles (exclude vehicles with '[' in name).")
    parser.add_argument("-v", "--verbose", action='store_true', help="Print detailed information about changes.")
    args = parser.parse_args()

    input_file = args.input
    output_file = args.output if args.output else input_file.replace(".sce", "_initial_speed_set.sce")
    
    set_initial_speed(input_file, output_file, args.speed, args.swarm_only, args.verbose)


if __name__ == "__main__":
    main()
