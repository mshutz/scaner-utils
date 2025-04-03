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
