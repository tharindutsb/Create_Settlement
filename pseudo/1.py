# Updated sup_array
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

# Separate arrays for bk-A, bk-B, bk-C, and an unapplied_array
bk_A = []
bk_B = []
bk_C = []
unapplied_array = []

# Conditions for each bk array
bk_conditions = {
    'A': ['a', 'b', 'w'],
    'B': ['c', 'b', 'e'],
    'C': ['m', 'b', 'n']
}

# Limiting the filling capacity of each bk array
bk_limits = {
    'A': 4,
    'B': 3,
    'C': 4
}

# Sorting sup_array based on the integer value
sup_array.sort(key=lambda x: x[2])

# Function to fill the bk arrays
def fill_bk_arrays():
    # A helper function to fill elements into the bk arrays
    def try_fill_element(row_num, char, int_val):
        # Try to fill in the arrays in the order A -> B -> C
        for bk_type, condition_set in bk_conditions.items():
            if char in condition_set and len(eval(f'bk_{bk_type}')) < bk_limits[bk_type]:
                eval(f'bk_{bk_type}').append((row_num, char, int_val))
                return True  # Element was placed successfully
        return False  # Element couldn't be placed

    # Main loop for processing the cycles
    while sup_array:
        # Track elements to be removed from sup_array after being processed
        elements_to_remove = []
        for i, row in enumerate(sup_array):
            row_num, char, int_val = row

            # Try to fill the element in the arrays
            if not try_fill_element(row_num, char, int_val):
                elements_to_remove.append(i)  # Mark this element as not placed

        # Remove elements that were not placed into the arrays
        for i in reversed(elements_to_remove):
            sup_array[i] = None

        # Clean the sup_array to remove None values
        sup_array[:] = [row for row in sup_array if row is not None]

        # If there are any unapplied elements, move them to the unapplied array
        if not sup_array:
            break

        # Move any remaining elements into the unapplied array
        for row in sup_array:
            if row is not None:
                unapplied_array.append(row)

        # After each cycle, process unapplied array to attempt to place again
        temp_unapplied = []
        for element in unapplied_array:
            row_num, char, int_val = element
            if not try_fill_element(row_num, char, int_val):
                temp_unapplied.append(element)  # If can't place, add back to the temp list
        unapplied_array[:] = temp_unapplied  # Update unapplied_array with elements that couldn't be placed

# Fill the bk arrays based on the conditions
fill_bk_arrays()

# Results
print("bk_A:", bk_A)
print("bk_B:", bk_B)
print("bk_C:", bk_C)
print("Unapplied Array:", unapplied_array)