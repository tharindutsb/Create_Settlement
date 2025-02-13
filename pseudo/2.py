from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Update your MongoDB URI if needed
db = client["bucket_assignment_db"]  # Replace with your actual database name
sup_collection = db["sup_collection"]  # Collection for sup_array
buckets_collection = db["buckets_collection"]  # Collection for bucket configurations

# Fetch sup_array from MongoDB and sort by integer value (ascending order)
sup_array = list(sup_collection.find({}, {"_id": 0}))
sup_array.sort(key=lambda x: x["value"])  # Sorting by integer value

# Fetch bucket configurations dynamically
buckets_data = list(buckets_collection.find({}, {"_id": 0}))

# Initialize bucket structures dynamically
buckets = {}
unapplied_array = []

# Process bucket configurations
for bucket in buckets_data:
    bucket_name = bucket["name"]  # Example: "bk_A"
    buckets[bucket_name] = {
        "limit": bucket["limit"],  # Maximum filling capacity
        "characters": set(bucket["characters"]),  # Allowed characters
        "items": []
    }

# Get total bucket count
bucket_names = list(buckets.keys())
bucket_count = len(bucket_names)

# **Function to fill buckets in a round-robin fashion**
def fill_buckets():
    global unapplied_array
    unapplied_array = []
    
    for i, row in enumerate(sup_array):
        row_num, char, value = row["row_number"], row["char"], row["value"]
        placed = False
        
        # **Round-robin filling logic**
        target_bucket = bucket_names[i % bucket_count]  # Pick bucket in order
        for _ in range(bucket_count):  # Try to fit it into a valid bucket
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

# **Update MongoDB with results**
for bucket_name, bucket in buckets.items():
    buckets_collection.update_one(
        {"name": bucket_name},
        {"$set": {"filled_items": bucket["items"]}},
        upsert=True
    )

# **Store unapplied items in MongoDB**
db["unapplied_collection"].delete_many({})
if unapplied_array:
    db["unapplied_collection"].insert_many(unapplied_array)

print("Buckets and unapplied items updated in MongoDB.")
