from webdriver_manager import chrome
# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


# webdriver.Chrome()
#
# input('enter upon logged in: ')
def counting_sort_by_last_digit(arr):
    # Create a count array for digits 0-9
    count = [0] * 10
    output = [0] * len(arr)

    # Step 1: Count occurrences of each last digit
    for num in arr:
        last_digit = num % 10
        count[last_digit] += 1

    # Step 2: Compute cumulative positions
    for i in range(1, 10):
        count[i] += count[i - 1]

    # Step 3: Place elements in sorted order (stable sorting)
    for i in range(len(arr) - 1, -1, -1):  # Process from right to left for stability
        last_digit = arr[i] % 10
        output[count[last_digit] - 1] = arr[i]
        count[last_digit] -= 1

    return output

# Example usage
arr = [23, 45, 12, 67, 89, 90, 34, 21, 55, 78]
sorted_arr = counting_sort_by_last_digit(arr)
print(sorted_arr)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
