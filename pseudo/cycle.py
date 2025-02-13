import random

# Generate a sup_array with 100 rows for testing
# sup_array = [(i, random.choice('abcdefghijklmnopqrstuvwxyz'), random.randint(1, 100)) for i in range(1, 101)]
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
    (10, 'c', 30),
    # (11, 'b', 30),
    # (12, 'a', 30),
    # (13, 'c', 20),
    # (14, 'c', 26),
    # (15, 'c', 26),
    # (16, 'c', 26),
]

# Initialize bk arrays and unapplied arrays
bk_A = []
bk_B = []
bk_C = []
permanent_unapplied_array = []  # Permanent unapplied array
temp_unapplied_array = []  # Temporary unapplied array

# Define the fill limits
bk_A_limit = 3
bk_B_limit = 3
bk_C_limit = 3

# Define the character constraints for each bk array
bk_A_chars = {'a', 'b', 'w'}
bk_B_chars = {'c', 'b', 'e'}
bk_C_chars = {'m', 'b', 'n'}

# Function to attempt to fill bk arrays
def fill_bk_arrays():
    global temp_unapplied_array
    temp_unapplied_array = []  # Reset temporary unapplied array for each cycle
    for row in sup_array:
        row_num, char, value = row
        if len(bk_A) >= bk_A_limit and len(bk_B) >= bk_B_limit and len(bk_C) >= bk_C_limit:
            temp_unapplied_array.append(row)  # Add to temporary unapplied if all buckets are full
            continue
        if char in bk_C_chars and len(bk_C) < bk_C_limit:
            bk_C.append(row)
        elif char in bk_B_chars and len(bk_B) < bk_B_limit:
            bk_B.append(row)
        elif char in bk_A_chars and len(bk_A) < bk_A_limit:
            bk_A.append(row)
        else:
            # Attempt to swap within the same iteration
            swapped = False
            if char in bk_C_chars and len(bk_C) >= bk_C_limit:
                for i, (r_num, r_char, r_value) in enumerate(bk_C):
                    if r_char in bk_B_chars and len(bk_B) < bk_B_limit:
                        bk_B.append(bk_C.pop(i))
                        bk_C.append(row)
                        swapped = True
                        break
                    elif r_char in bk_A_chars and len(bk_A) < bk_A_limit:
                        bk_A.append(bk_C.pop(i))
                        bk_C.append(row)
                        swapped = True
                        break
            if not swapped and char in bk_B_chars and len(bk_B) >= bk_B_limit:
                for i, (r_num, r_char, r_value) in enumerate(bk_B):
                    if r_char in bk_C_chars and len(bk_C) < bk_C_limit:
                        bk_C.append(bk_B.pop(i))
                        bk_B.append(row)
                        swapped = True
                        break
                    elif r_char in bk_A_chars and len(bk_A) < bk_A_limit:
                        bk_A.append(bk_B.pop(i))
                        bk_B.append(row)
                        swapped = True
                        break
            if not swapped and char in bk_A_chars and len(bk_A) >= bk_A_limit:
                for i, (r_num, r_char, r_value) in enumerate(bk_A):
                    if r_char in bk_C_chars and len(bk_C) < bk_C_limit:
                        bk_C.append(bk_A.pop(i))
                        bk_A.append(row)
                        swapped = True
                        break
                    elif r_char in bk_B_chars and len(bk_B) < bk_B_limit:
                        bk_B.append(bk_A.pop(i))
                        bk_A.append(row)
                        swapped = True
                        break
            if not swapped:
                temp_unapplied_array.append(row)  # Add to temporary unapplied if no swap is possible

# Function to reprocess temp_unapplied_array
def reprocess_temp_unapplied():
    global temp_unapplied_array, permanent_unapplied_array
    new_temp_unapplied = []
    for row in temp_unapplied_array:
        row_num, char, value = row
        if len(bk_A) >= bk_A_limit and len(bk_B) >= bk_B_limit and len(bk_C) >= bk_C_limit:
            permanent_unapplied_array.append(row)  # Move to permanent unapplied if all buckets are full
            continue
        if char in bk_C_chars and len(bk_C) < bk_C_limit:
            bk_C.append(row)
        elif char in bk_B_chars and len(bk_B) < bk_B_limit:
            bk_B.append(row)
        elif char in bk_A_chars and len(bk_A) < bk_A_limit:
            bk_A.append(row)
        else:
            new_temp_unapplied.append(row)  # Keep in temporary unapplied for next cycle
    temp_unapplied_array = new_temp_unapplied

# Perform the initial fill
fill_bk_arrays()

# Reprocess temp_unapplied_array until no more elements can be added to bk arrays
previous_temp_unapplied_length = -1
while len(temp_unapplied_array) != previous_temp_unapplied_length:
    previous_temp_unapplied_length = len(temp_unapplied_array)
    reprocess_temp_unapplied()

# Output the results
print("bk-A:", bk_A)
print("bk-B:", bk_B)
print("bk-C:", bk_C)
print("Permanent Unapplied:", permanent_unapplied_array)