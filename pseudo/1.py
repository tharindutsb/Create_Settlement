# sup_array = [
#     (1, 'z', 84),
#     (2, 'b', 80),
#     (3, 'b', 70),
#     (4, 'w', 65),
#     (5, 'e', 55),
#     (6, 'm', 50),
#     (7, 'b', 45),
#     (8, 'n', 40),
#     (9, 'a', 5),
#     (10, 'c', 30)
# ]

# sup_array = [
#     (1, 'b', 84),
#     (2, 'n', 80),
#     (3, 'w', 70),
#     (4, 'w', 65),
#     (5, 'e', 55),
#     (6, 'm', 50),
#     (7, 'b', 45),
#     (8, 'n', 40),
#     (9, 'a', 5),
#     (10, 'c', 30)
# ]

sup_array = [
    (1, 'b', 84),
    (2, 'n', 80),
    (3, 'w', 70),
    (4, 'w', 65),
    (5, 'b', 55),
    (6, 'e', 50),
    (7, 'b', 45),
    (8, 'n', 40),
    (9, 'a', 5),
    (10, 'c', 30)
]

# Initialize bk arrays and unapplied array
bk_arrays = {
    'A': {'array': [], 'chars': {'a', 'b', 'w'}, 'limit': 4},
    'B': {'array': [], 'chars': {'c', 'b', 'e'}, 'limit': 3},
    'C': {'array': [], 'chars': {'m', 'b', 'n'}, 'limit': 4}
}
unapplied_array = []

# Sort sup_array by the integer value in descending order
sup_array.sort(key=lambda x: x[2], reverse=True)

# Function to attempt to fill bk arrays within a cycle
def fill_bk_arrays_cycle(array):
    global unapplied_array
    unapplied_array = []
    for row in array:
        row_num, char, value = row
        placed = False
        for bk in bk_arrays.values():
            if char in bk['chars'] and len(bk['array']) < bk['limit']:
                bk['array'].append(row)
                placed = True
                break
        if not placed:
            unapplied_array.append(row)

# Function to process the sup_array in cycles
def process_cycles():
    global sup_array
    cycle_size = len(sup_array) // len(bk_arrays) + (1 if len(sup_array) % len(bk_arrays) != 0 else 0)
    for i in range(0, len(sup_array), cycle_size):
        cycle_array = sup_array[i:i + cycle_size]
        fill_bk_arrays_cycle(cycle_array)
        reprocess_unapplied()

# Function to reprocess unapplied_array
def reprocess_unapplied():
    global unapplied_array
    new_unapplied = []
    for row in unapplied_array:
        row_num, char, value = row
        placed = False
        for bk in bk_arrays.values():
            if char in bk['chars'] and len(bk['array']) < bk['limit']:
                bk['array'].append(row)
                placed = True
                break
        if not placed:
            new_unapplied.append(row)
    unapplied_array = new_unapplied

# Perform the initial cycle processing
process_cycles()

# Reprocess unapplied_array until no more elements can be added to bk arrays
previous_unapplied_length = -1
while len(unapplied_array) != previous_unapplied_length:
    previous_unapplied_length = len(unapplied_array)
    reprocess_unapplied()

# Output the results
for bk_name, bk in bk_arrays.items():
    print(f"bk-{bk_name}:", bk['array'])
print("Unapplied:", unapplied_array)