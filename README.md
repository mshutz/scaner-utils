# SCANeR Utility Scripts

## Terrain File Fix

`rnd_import_fix.py`: Fix broken intersections after OSM import.
- Removes all authorizations in intersections
- Names all lanes in tracks (Lane 1, Lane 2, Lane 3, ...)

Open repaired file in SCANeR and save it - SCANeR will automatically add (default) intersection authorizations.

**Example usage:**

```
python scripts/rnd_import_fix.py --input btc_lrn.rnd --output btc_lrn_fixed.rnd
```

## Terrain File Data Extraction

`rnd_extract_connections.py`: Extract track info (connected tracks, length, portions, lanes, ...) in the defined JSON structure that is needed by custom swarm.

**Example usage:**

```
python scripts/rnd_extract_connections.py --input btc_lrn.rnd --output btc_lrn.json
```
