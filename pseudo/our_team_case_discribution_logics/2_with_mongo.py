from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['your_database_name']
sup_collection = db['sup_array']
buckets_collection = db['buckets']

# Fetch sup_array from MongoDB
sup_array = list(sup_collection.find({}, {'_id': 0}))

# Fetch bucket configurations from MongoDB
buckets_config = list(buckets_collection.find({}, {'_id': 0}))

# Dynamically initialize buckets and their configurations
buckets = {}
for config in buckets_config:
    bucket_name = config['name']  # Assuming each bucket has a 'name' field
    buckets[bucket_name] = {
        'limit': config['limit'],
        'chars': set(config['chars']),
        'rows': []
    }

# Initialize unapplied array
unapplied_array = []

# Function to attempt to fill buckets
def fill_buckets():
    global unapplied_array
    unapplied_array = []
    for row in sup_array:
        row_num, char, value = row['row_num'], row['char'], row['value']
        
        # Check if all buckets are full
        if all(len(bucket['rows']) >= bucket['limit'] for bucket in buckets.values()):
            unapplied_array.append(row)
            continue
        
        # Try to add the row to the appropriate bucket
        added = False
        for bucket_name, bucket in buckets.items():
            if char in bucket['chars'] and len(bucket['rows']) < bucket['limit']:
                bucket['rows'].append(row)
                added = True
                break
        
        # If not added, attempt to swap with other buckets
        if not added:
            for bucket_name, bucket in buckets.items():
                if char in bucket['chars'] and len(bucket['rows']) >= bucket['limit']:
                    # Try to swap with another bucket
                    for swap_bucket_name, swap_bucket in buckets.items():
                        if swap_bucket_name != bucket_name and len(swap_bucket['rows']) < swap_bucket['limit']:
                            # Find a row in the current bucket that can be moved to the swap bucket
                            for i, (r_num, r_char, r_value) in enumerate(bucket['rows']):
                                if r_char in swap_bucket['chars']:
                                    # Swap the rows
                                    swap_bucket['rows'].append(bucket['rows'].pop(i))
                                    bucket['rows'].append(row)
                                    added = True
                                    break
                            if added:
                                break
                    if added:
                        break
        
        # If still not added, add to unapplied array
        if not added:
            unapplied_array.append(row)

# Function to reprocess unapplied_array
def reprocess_unapplied():
    global unapplied_array
    new_unapplied = []
    for row in unapplied_array:
        row_num, char, value = row['row_num'], row['char'], row['value']
        
        # Check if all buckets are full
        if all(len(bucket['rows']) >= bucket['limit'] for bucket in buckets.values()):
            new_unapplied.append(row)
            continue
        
        # Try to add the row to the appropriate bucket
        added = False
        for bucket_name, bucket in buckets.items():
            if char in bucket['chars'] and len(bucket['rows']) < bucket['limit']:
                bucket['rows'].append(row)
                added = True
                break
        
        if not added:
            new_unapplied.append(row)
    
    unapplied_array = new_unapplied

# Perform the initial fill
fill_buckets()

# Reprocess unapplied_array until no more elements can be added to buckets
previous_unapplied_length = -1
while len(unapplied_array) != previous_unapplied_length:
    previous_unapplied_length = len(unapplied_array)
    reprocess_unapplied()

# Output the results
for bucket_name, bucket in buckets.items():
    print(f"{bucket_name}: {bucket['rows']}")
print("Unapplied:", unapplied_array)

# Optionally, update MongoDB with the results
results_collection = db['results']
results = [{'bucket': bucket_name, 'rows': bucket['rows']} for bucket_name, bucket in buckets.items()]
results.append({'unapplied': unapplied_array})
results_collection.insert_many(results)