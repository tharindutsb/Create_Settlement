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
    (10, 'c', 30),
    (11, 'x', 30),
    (12, 'y', 30),
    (13,'c',20),
    (14,'c',26),
]

# Initialize bk arrays and unapplied array
bk_A = []
bk_B = []
bk_C = []
unapplied_array = []

# Define the fill limits
bk_A_limit = 4
bk_B_limit = 3
bk_C_limit = 4

# Define the character constraints for each bk array
bk_A_chars = {'a', 'b', 'w'}
bk_B_chars = {'c', 'b', 'e'}
bk_C_chars = {'m', 'b', 'n'}

# Sort sup_array by the integer value
sup_array.sort(key=lambda x: x[2])
print ('array check 1 ',sup_array)
# Function to attempt to fill bk arrays
def fill_bk_arrays():
    global unapplied_array
    unapplied_array = []
    print('array check 2', sup_array)
    for row in sup_array:
        row_num, char, value = row
        if len(bk_A) >= bk_A_limit and len(bk_B) >= bk_B_limit and len(bk_C) >= bk_C_limit:
            unapplied_array.append(row)
            continue
        if char in bk_C_chars and len(bk_C) < bk_C_limit:
            bk_C.append(row)
        elif char in bk_B_chars and len(bk_B) < bk_B_limit:
            bk_B.append(row)
        elif char in bk_A_chars and len(bk_A) < bk_A_limit:
            bk_A.append(row)
        else:
            unapplied_array.append(row)

# Function to reprocess unapplied_array
def reprocess_unapplied():
    global unapplied_array
    new_unapplied = []
    for row in unapplied_array:
        row_num, char, value = row
        if len(bk_A) >= bk_A_limit and len(bk_B) >= bk_B_limit and len(bk_C) >= bk_C_limit:
            new_unapplied.append(row)
            continue
        if char in bk_C_chars and len(bk_C) < bk_C_limit:
            bk_C.append(row)
        elif char in bk_B_chars and len(bk_B) < bk_B_limit:
            bk_B.append(row)
        elif char in bk_A_chars and len(bk_A) < bk_A_limit:
            bk_A.append(row)
        else:
            new_unapplied.append(row)
    unapplied_array = new_unapplied

# Perform the initial fill
fill_bk_arrays()

# Reprocess unapplied_array until no more elements can be added to bk arrays
previous_unapplied_length = -1
while len(unapplied_array) != previous_unapplied_length:
    previous_unapplied_length = len(unapplied_array)
    reprocess_unapplied()

# Output the results
print("bk-A:", bk_A)
print("bk-B:", bk_B)
print("bk-C:", bk_C)
print("Unapplied:", unapplied_array)