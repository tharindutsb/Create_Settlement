import numpy as np
from collections import deque

# Generate a sample sup_array with 100 rows (row number, character, integer value)
np.random.seed(42)  # For reproducibility
characters = list("abcdefghijklmnopqrstuvwxyz")
sup_array = np.array(
    [[i, np.random.choice(characters), np.random.randint(1, 100)] for i in range(1, 101)],
    dtype=object
)

# Sorting sup_array by integer value (Condition 5)
sup_array = sup_array[sup_array[:, 2].argsort()]

# BK array filling conditions
bk_conditions = {
    "A": {"chars": {"a", "b", "w"}, "limit": 4},
    "B": {"chars": {"c", "b", "e"}, "limit": 3},
    "C": {"chars": {"m", "b", "n"}, "limit": 4},
}

# Initialize bk arrays and unapplied_array
bk_A, bk_B, bk_C = deque(), deque(), deque()
unapplied_array = deque()
bk_list = [bk_A, bk_B, bk_C]

# Function to check and fill BK arrays
def fill_bk_arrays():
    global unapplied_array
    unapplied = deque()
    
    for row in sup_array:
        row_num, char, value = row
        placed = False
        
        for bk, (bk_name, condition) in zip(bk_list, bk_conditions.items()):
            if char in condition["chars"] and len(bk) < condition["limit"]:
                bk.append(row)
                placed = True
                break
        
        if not placed:
            unapplied.append(row)
    
    unapplied_array = unapplied

# Function to process unapplied elements
def reprocess_unapplied():
    global unapplied_array
    new_unapplied = deque()
    
    for row in unapplied_array:
        row_num, char, value = row
        placed = False
        
        for bk, (bk_name, condition) in zip(bk_list, bk_conditions.items()):
            if char in condition["chars"] and len(bk) < condition["limit"]:
                bk.append(row)
                placed = True
                break
        
        if not placed:
            new_unapplied.append(row)
    
    unapplied_array = new_unapplied

# Fill BK arrays initially
fill_bk_arrays()

# Reprocess unapplied elements until no more elements can be placed
while unapplied_array:
    prev_unapplied_size = len(unapplied_array)
    reprocess_unapplied()
    if len(unapplied_array) == prev_unapplied_size:
        break  # Stop if no more elements can be placed

# Print results
print("BK-A:", list(bk_A))
print("BK-B:", list(bk_B))
print("BK-C:", list(bk_C))
print("Unapplied:", list(unapplied_array))