# Define the sup_array
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
    (10, 'x', 30)
    
]

# Sort sup_array based on the integer value (ascending order)
sup_array.sort(key=lambda x: x[2])

# Initialize bk arrays and unapplied_array
bk_A = []
bk_B = []
bk_C = []
unapplied_array = []

# Define the allowed characters for each bk array
allowed_chars = {
    'bk_A': {'a', 'b', 'w'},
    'bk_B': {'c', 'b', 'e'},
    'bk_C': {'m', 'b', 'n'}
}

# Define the maximum capacity for each bk array
max_capacity = {
    'bk_A': 4,
    'bk_B': 3,
    'bk_C': 4
}

# Function to check if an element can be placed in a bk array
def can_place(element, bk_name):
    return element[1] in allowed_chars[bk_name] and len(globals()[bk_name]) < max_capacity[bk_name]

# Function to exchange elements within the same iteration
def exchange_elements(element, bk_name):
    for i, existing_element in enumerate(globals()[bk_name]):
        if existing_element[1] in allowed_chars[bk_name]:
            # Swap the elements
            globals()[bk_name][i] = element
            return existing_element
    return None

# Iterate through the sup_array and fill the bk arrays
for element in sup_array:
    if element[1] not in allowed_chars['bk_A'] and element[1] not in allowed_chars['bk_B'] and element[1] not in allowed_chars['bk_C']:
        unapplied_array.append(element)
        continue

    placed = False
    for bk_name in ['bk_A', 'bk_B', 'bk_C']:
        if can_place(element, bk_name):
            globals()[bk_name].append(element)
            placed = True
            break
    if not placed:
        unapplied_array.append(element)

# Re-process unapplied_array until no elements can be placed
reprocess = True
while reprocess:
    reprocess = False
    for i in range(len(unapplied_array)):
        element = unapplied_array[i]
        for bk_name in ['bk_A', 'bk_B', 'bk_C']:
            if can_place(element, bk_name):
                globals()[bk_name].append(element)
                unapplied_array.pop(i)
                reprocess = True
                break
        if reprocess:
            break

# Print the results
print("bk-A:", bk_A)
print("bk-B:", bk_B)
print("bk-C:", bk_C)
print("Unapplied:", unapplied_array)