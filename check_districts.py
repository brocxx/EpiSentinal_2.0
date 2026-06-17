import csv
import json

# Check CSV districts
csv_file = r'c:\Users\gndis\.gemini\antigravity\worktrees\EpiSentinal_2.0\verify-ensemble-heatmap-logic\dashboard\frontend\synthetic_test_data.csv'
with open(csv_file) as f:
    reader = csv.DictReader(f)
    csv_districts = [row['district'] for row in reader]

# Check GeoJSON districts
geojson_file = r'c:\Users\gndis\.gemini\antigravity\worktrees\EpiSentinal_2.0\verify-ensemble-heatmap-logic\dashboard\frontend\karnataka_districts.json'
with open(geojson_file) as f:
    geojson = json.load(f)
    geojson_districts = [feat['properties']['district'] for feat in geojson['features']]

print("CSV Districts:")
for d in csv_districts[:10]:
    print(f"  • {d}")
print(f"  ({len(csv_districts)} total)\n")

print("Karnataka GeoJSON Districts:")
for d in geojson_districts[:10]:
    print(f"  • {d}")
print(f"  ({len(geojson_districts)} total)\n")

# Check matches
csv_set = set(csv_districts)
geojson_set = set(geojson_districts)
matches = csv_set & geojson_set
missing_in_geojson = csv_set - geojson_set
missing_in_csv = geojson_set - csv_set

print(f"✓ Matching districts: {len(matches)}")
if missing_in_geojson:
    print(f"⚠ CSV districts NOT in GeoJSON: {missing_in_geojson}")
if missing_in_csv:
    print(f"ℹ GeoJSON districts NOT in CSV: {missing_in_csv}")
