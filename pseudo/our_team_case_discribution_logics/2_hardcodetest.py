# Hardcoded sup_array (Rows Data)
sup_array = [
    {"row_number": 1, "char": "b", "value": 84},
    {"row_number": 2, "char": "n", "value": 80},
    {"row_number": 3, "char": "w", "value": 70},
    {"row_number": 4, "char": "w", "value": 65},
    {"row_number": 5, "char": "b", "value": 55},
    {"row_number": 6, "char": "e", "value": 50},
    {"row_number": 7, "char": "b", "value": 45},
    {"row_number": 8, "char": "n", "value": 40},
    {"row_number": 9, "char": "a", "value": 35},
    {"row_number": 10, "char": "c", "value": 30},
    {"row_number": 11, "char": "m", "value": 25},
    {"row_number": 12, "char": "x", "value": 20},
    {"row_number": 13, "char": "y", "value": 15},
    {"row_number": 14, "char": "z", "value": 10},
    {"row_number": 15, "char": "GG", "value": 8},
]

# Sort sup_array by integer value (ascending order)
sup_array.sort(key=lambda x: x["value"])

# Hardcoded bucket configurations
buckets = {
    "bk_A": {"limit": 4, "characters": {"a", "b", "w"}, "items": []},
    "bk_B": {"limit": 3, "characters": {"c", "b", "e"}, "items": []},
    "bk_C": {"limit": 4, "characters": {"m", "b", "n"}, "items": []},
    "bk_D": {"limit": 4, "characters": {"x", "y", "z"}, "items": []}
}

# Bucket order for round-robin filling
bucket_names = list(buckets.keys())
bucket_count = len(bucket_names)
unapplied_array = []

# **Function to fill buckets in a round-robin fashion**
def fill_buckets():
    global unapplied_array
    unapplied_array = []
    
    for i, row in enumerate(sup_array):
        row_num, char, value = row["row_number"], row["char"], row["value"]
        placed = False

        # **Round-robin filling logic**
        target_bucket = bucket_names[i % bucket_count]  # Pick bucket in order
        for _ in range(bucket_count):  # Try to fit into a valid bucket
            if char in buckets[target_bucket]["characters"] and len(buckets[target_bucket]["items"]) < buckets[target_bucket]["limit"]:
                buckets[target_bucket]["items"].append(row)
                placed = True
                break
            target_bucket = bucket_names[(bucket_names.index(target_bucket) + 1) % bucket_count]  # Move to next bucket

        # **Swapping logic within the same iteration**
        if not placed:
            swapped = False
            for bucket_name, bucket in buckets.items():
                if len(bucket["items"]) >= bucket["limit"]:  # Bucket is full
                    for i, existing_row in enumerate(bucket["items"]):
                        existing_char = existing_row["char"]

                        # Find another bucket to swap with
                        for target_bucket_name, target_bucket in buckets.items():
                            if existing_char in target_bucket["characters"] and len(target_bucket["items"]) < target_bucket["limit"]:
                                # Swap elements
                                target_bucket["items"].append(bucket["items"].pop(i))
                                bucket["items"].append(row)
                                swapped = True
                                break
                        if swapped:
                            break
                if swapped:
                    break

        # If no placement or swapping is possible, move to unapplied
        if not placed and not swapped:
            unapplied_array.append(row)

# **Function to reprocess unapplied items**
def reprocess_unapplied():
    global unapplied_array
    new_unapplied = []

    for row in unapplied_array:
        row_num, char, value = row["row_number"], row["char"], row["value"]
        placed = False

        # Try to place in available buckets
        for bucket_name, bucket in buckets.items():
            if char in bucket["characters"] and len(bucket["items"]) < bucket["limit"]:
                bucket["items"].append(row)
                placed = True
                break

        # If not placed, keep in unapplied list
        if not placed:
            new_unapplied.append(row)

    unapplied_array = new_unapplied

# **Perform initial bucket filling**
fill_buckets()

# **Reprocess unapplied items until no further placements**
previous_unapplied_length = -1
while len(unapplied_array) != previous_unapplied_length:
    previous_unapplied_length = len(unapplied_array)
    reprocess_unapplied()

# **Output results**
for bucket_name, bucket in buckets.items():
    print(f"{bucket_name}: {bucket['items']}")
print("Unapplied:", unapplied_array)
