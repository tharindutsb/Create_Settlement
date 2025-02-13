from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Update with your MongoDB connection string
db = client["bucket_assignment_db"]  # Database name

# **Clear existing collections**
db["sup_collection"].delete_many({})
db["buckets_collection"].delete_many({})
db["unapplied_collection"].delete_many({})

# **Sample sup_collection (Rows Data)**
sup_data = [
    {"row_number": 1, "char": "b", "value": 84},
    {"row_number": 2, "char": "n", "value": 80},
    {"row_number": 3, "char": "w", "value": 70},
    {"row_number": 4, "char": "w", "value": 65},
    {"row_number": 5, "char": "b", "value": 55},
    {"row_number": 6, "char": "e", "value": 50},
    {"row_number": 7, "char": "b", "value": 45},
    {"row_number": 8, "char": "n", "value": 40},
    {"row_number": 9, "char": "a", "value": 5},
    {"row_number": 10, "char": "c", "value": 30},
    # {"row_number": 11, "char": "m", "value": 25},
    # {"row_number": 12, "char": "x", "value": 20},
    # {"row_number": 13, "char": "y", "value": 15},
    # {"row_number": 14, "char": "z", "value": 10},
]

# Insert data into `sup_collection`
db["sup_collection"].insert_many(sup_data)

# **Sample buckets_collection (Bucket Configuration)**
buckets_data = [
    {
        "name": "bk_A",
        "limit": 4,
        "characters": ["a", "b", "w"]
    },
    {
        "name": "bk_B",
        "limit": 3,
        "characters": ["c", "b", "e"]
    },
    {
        "name": "bk_C",
        "limit": 4,
        "characters": ["m", "b", "n"]
    }
]

# Insert bucket configurations into `buckets_collection`
db["buckets_collection"].insert_many(buckets_data)

print("✅ MongoDB setup complete. Sample data inserted successfully!")
