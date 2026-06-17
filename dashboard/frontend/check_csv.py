import csv
with open('synthetic_test_data.csv') as f:
    rows = list(csv.DictReader(f))
    print("Sampled districts from CSV:")
    for row in rows[:3]:
        print(f"  • {row['district']}")
    print(f"\n✓ Total districts in CSV: {len(rows)}")
