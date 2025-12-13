# SCANeR Utility Scripts

## Terrain File Fix

`rnd_import_fix.py`

Fix broken intersections after OSM import.

- Removes all authorizations in intersections
- Names all lanes in tracks (Lane 1, Lane 2, Lane 3, ...)

Open repaired file in SCANeR and save it - SCANeR will automatically add (default) intersection authorizations.

**Arguments:**

- `--input`: Input Terrain (.rnd) file path.
- `--output`: Output Terrain (.rnd) file path. Defaults to input file name.

**Example usage:**

```bash
python scripts/rnd_import_fix.py --input btc_lrn.rnd --output btc_lrn_fixed.rnd
```

## Terrain File Data Extraction

`rnd_extract_connections.py`

Extract track info (connected tracks, length, portions, lanes, ...) in the defined JSON structure that is needed by custom swarm.

**Arguments:**

- `--input`: Input Terrain (.rnd) file path.
- `--output`: Output JSON file path (defaults to input filename with .json extension).
- `--lane_types`: List of SCANeR lane types to generate positions on (e.g., 'paved express' 'paved entry'). Default: paved express, paved entry, paved, emergency

**Example usage:**

```bash
python scripts/rnd_extract_connections.py --input btc_lrn.rnd --output btc_lrn.json --lane_types "paved express" "paved entry" paved
```

## Terrain File Portion Naming

`rnd_name_portions.py`

Assign unique names to all portions in the tracks of a Terrain (.rnd) file.

- Iterates through all tracks and assigns a unique name (incremental ID) to each portion.

Open repaired file in SCANeR and save it.

**Arguments:**

- `--input`: Input Terrain (.rnd) file path.
- `--output`: Output Terrain (.rnd) file path. Defaults to input file name.

**Example usage:**

```bash
python scripts/rnd_name_portions.py --input za_driver_evaluation_highway_lrn.rnd --output za_driver_evaluation_highway_lrn_named.rnd
```

## Scenario File Initial Speed Setup

`scenario_set_initial_speed.py`

Set initial speed for (swarm) vehicles in a scenario file.

**Arguments:**

- `-i`, `--input`: Input Scenario (.sce) file path (required)
- `-o`, `--output`: Output Scenario (.sce) file path. Defaults to input filename with _initial_speed_set suffix
- `-s`, `--speed`: Initial speed value in km/h. (required)
- `-w`, `--swarm_only`: Flag to only modify non-swarm vehicles (exclude vehicles with '[' in name)
- `-v`, `--verbose`: Flag to print detailed information about changes

**Example usage:**

```bash
# Set speed for non-swarm vehicles with verbose output
python scripts/scenario_set_initial_speed.py -i scenario.sce -s 100 -w -v

# Set speed with custom output file
python scripts/scenario_set_initial_speed.py --input scenario.sce --output modified.sce --speed 80 --swarm_only

# Simple usage (output will be scenario_initial_speed_set.sce)
python scripts/scenario_set_initial_speed.py -i scenario.sce -s 100 -w
```
