"""
Script: license_stats.py

This script calculates and prints license checkins, checkout, Existence check.

Usage: python license_stats.py <license_file>

Arguments:
    <license_file>: Path to the file containing license data.
"""

import sys

infile = sys.argv[1]

licenses = []
with open(infile, "r") as file:
    for line in file:
        x = line.strip().split(",")
        licenses.append(x)


lic_dict = {}
for lic in licenses[1:]:
    key, status = lic[1], lic[9]
    if status == "Checkout" or status == "Checkin" or status == "Exist":
        if key not in lic_dict:
            lic_dict[key]={}
        if status not in lic_dict[key]:
            lic_dict[key][status] = 0
        lic_dict[key][status]+=1     

print("License Statistics:")
for key, value in lic_dict.items():
    print(f"{key}:")
    for status, count in value.items():
        print(f"    {status}: {count}")