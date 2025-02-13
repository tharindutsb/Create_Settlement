from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Update with your connection string
db = client["gpt_bucket"]  # Replace with your database name
sup_collection = db["sup_collection"]  # Collection storing sup_array data
buckets_collection = db["buckets_collection"]  # Collection storing bucket constraints

# Fetch sup_array from MongoDB
sup_array = list(sup_collection.find({}, {"_id": 0}))  # Exclude MongoDB's `_id` field

# Fetch bucket configurations from MongoDB
buckets_data = list(buckets_collection.find({}, {"_id": 0}))

# Initialize bucket structures dynamically
buckets = {}
unapplied_array = []

# Process bucket configurations
for bucket in buckets_data:
    bucket_name = bucket["name"]
    buckets[bucket_name] = {
        "limit": bucket["limit"],  # Max capacity
        "characters": set(bucket["characters"]),  # Allowed characters
        "items": []
    }

# Sort sup_array by row number
sup_array.sort(key=lambda x: x["row_number"])

# Function to fill buckets
def fill_buckets():
    global unapplied_array
    unapplied_array = []

    for row in sup_array:
        row_num, char, value = row["row_number"], row["char"], row["value"]
        placed = False

        # Try placing in the first available bucket
        for bucket_name, bucket in buckets.items():
            if char in bucket["characters"] and len(bucket["items"]) < bucket["limit"]:
                bucket["items"].append(row)
                placed = True
                break

        # If placement fails, attempt swapping
        if not placed:
            swapped = False
            for bucket_name, bucket in buckets.items():
                if len(bucket["items"]) >= bucket["limit"]:  # Full bucket
                    for i, existing_row in enumerate(bucket["items"]):
                        existing_char = existing_row["char"]

                        # Check if existing item can be swapped with the new row
                        for target_bucket_name, target_bucket in buckets.items():
                            if existing_char in target_bucket["characters"] and len(target_bucket["items"]) < target_bucket["limit"]:
                                # Swap items
                                target_bucket["items"].append(bucket["items"].pop(i))
                                bucket["items"].append(row)
                                swapped = True
                                break
                        if swapped:
                            break
                if swapped:
                    break

            # If swapping fails, add to unapplied
            if not swapped:
                unapplied_array.append(row)

# Function to reprocess unapplied rows
def reprocess_unapplied():
    global unapplied_array
    new_unapplied = []

    for row in unapplied_array:
        row_num, char, value = row["row_number"], row["char"], row["value"]
        placed = False

        # Try placing again
        for bucket_name, bucket in buckets.items():
            if char in bucket["characters"] and len(bucket["items"]) < bucket["limit"]:
                bucket["items"].append(row)
                placed = True
                break

        # If still not placed, keep in unapplied
        if not placed:
            new_unapplied.append(row)

    unapplied_array = new_unapplied

# Perform initial bucket filling
fill_buckets()

# Reprocess unapplied rows until no further changes occur
previous_unapplied_length = -1
while len(unapplied_array) != previous_unapplied_length:
    previous_unapplied_length = len(unapplied_array)
    reprocess_unapplied()

# Output results
for bucket_name, bucket in buckets.items():
    print(f"{bucket_name}: {bucket['items']}")
print("Unapplied:", unapplied_array)

# Update MongoDB with results
for bucket_name, bucket in buckets.items():
    buckets_collection.update_one(
        {"name": bucket_name},
        {"$set": {"filled_items": bucket["items"]}},
        upsert=True
    )

# Store unapplied items in MongoDB
db["unapplied_collection"].delete_many({})
if unapplied_array:
    db["unapplied_collection"].insert_many(unapplied_array)

print("Buckets and unapplied items updated in MongoDB.")
