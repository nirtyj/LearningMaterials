
Matrix - 
[[0] * cols for i in range(rows)]

Find the index of the first number in arr that is greater than k - 
next((i for i,v in enumerate(arr) if v > k), -1)

 For each pair, subtract the second number from the first number.
c = [a - b for a, b in zip(arr, arr[1:])]