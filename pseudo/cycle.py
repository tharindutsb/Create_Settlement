def fill_bk_arrays(sup_array):
    # Sort sup_array by the integer value
    sup_array.sort(key=lambda x: x[2])

    bk_A, bk_B, bk_C = [], [], []
    unapplied_array = []

    # Define the filling limits
    limit_A, limit_B, limit_C = 4, 3, 4

    # Define the valid characters for each bk array
    valid_A = {'a', 'b', 'w'}
    valid_B = {'c', 'b', 'e'}
    valid_C = {'m', 'b', 'n'}

    # Calculate the number of cycles
    num_cycles = len(sup_array) // 3 + 1

    for cycle in range(num_cycles):
        for row in sup_array:
            row_num, char, value = row

            if char in valid_A and len(bk_A) < limit_A:
                bk_A.append(row)
            elif char in valid_B and len(bk_B) < limit_B:
                bk_B.append(row)
            elif char in valid_C and len(bk_C) < limit_C:
                bk_C.append(row)
            else:
                unapplied_array.append(row)

        # Process unapplied_array within the same cycle
        for row in unapplied_array[:]:
            row_num, char, value = row

            if char in valid_A and len(bk_A) < limit_A:
                bk_A.append(row)
                unapplied_array.remove(row)
            elif char in valid_B and len(bk_B) < limit_B:
                bk_B.append(row)
                unapplied_array.remove(row)
            elif char in valid_C and len(bk_C) < limit_C:
                bk_C.append(row)
                unapplied_array.remove(row)

    # Re-process unapplied_array after all cycles
    while unapplied_array:
        for row in unapplied_array[:]:
            row_num, char, value = row

            if char in valid_A and len(bk_A) < limit_A:
                bk_A.append(row)
                unapplied_array.remove(row)
            elif char in valid_B and len(bk_B) < limit_B:
                bk_B.append(row)
                unapplied_array.remove(row)
            elif char in valid_C and len(bk_C) < limit_C:
                bk_C.append(row)
                unapplied_array.remove(row)
            else:
                break

    return bk_A, bk_B, bk_C, unapplied_array

# Example usage
sup_array = [
    # ... 100 rows with (row number, character, integer value) ...
]

bk_A, bk_B, bk_C, unapplied_array = fill_bk_arrays(sup_array)
print("bk-A:", bk_A)
print("bk-B:", bk_B)
print("bk-C:", bk_C)
print("Unapplied:", unapplied_array)
