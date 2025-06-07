# First, let's add the input validation utility at the top of the file
def get_integer_input(prompt):
    """Safely get integer input from user with validation."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid integer.")

# prev2 = 0
# prev1 = 1

# print(prev2)
# print(prev1)
# for fibo in range(18):
#     next_fibo = prev1 + prev2
#     print(next_fibo)
#     prev1 = prev2
#     prev2 = next_fibo 

# print(0)
# print(1)
# count = 2

# def fibonacci(prev1, prev2):
#     """
#     Generate Fibonacci sequence recursively.
    
#     Args:
#         prev1: First number in sequence
#         prev2: Second number in sequence
        
#     Prints Fibonacci numbers until count reaches 19
#     """
#     global count
#     if count <= 19:
#         newFibo = prev1 + prev2
#         print(newFibo)
#         prev2 = prev1
#         prev1 = newFibo
#         count += 1
#         fibonacci(prev1, prev2)
#     else:
#         return

# fibonacci(1,0)


# def F(n):
#     """
#     Calculate nth Fibonacci number recursively.
    
#     Args:
#         n: Index of Fibonacci number to calculate
        
#     Returns:
#         The nth Fibonacci number
#     """
#     if n <= 1:
#         return n
#     else:
#         return F(n-1) + F(n-2)
# print(F(19))


# # Type your code below
# count = 0
# count += 4 * 2 - 1

# # Don't change the line below
# print(f"count = {count}")


# # Type your code below
# n1 = 8
# n2 = 9
# n3 = n1 > n2

# # Don't change the line below
# print(f"n1 = {n1}, n2 = {n2}, n3 = {n3}")


# age = 20
# has_license = True

# result = age >= 18 and has_license
# print(f"Eligible to drive: {result}")


# b1 = True
# b2 = True
# b3 = False

# # Don't change the lines below
# b4 = b1 and b2 and (not b3)
# print(f"b4 = {b4}")


# # Initialize variables
# is_sunny = True
# wind_speed = 5.4
# temperature = 23
# solar_panel_output = 9
# is_cloudy = False

# # The complete logical expression
# result = (is_sunny and wind_speed < 10 and solar_panel_output < 15 and temperature > 20) or is_cloudy

# # Don't delete the lines below
# print("Checking conditions for solar energy production...")
# print("1. Is it sunny?", is_sunny)
# print("2. Is wind speed safe?", wind_speed < 10)
# print("3. Can panels produce more?", solar_panel_output < 15)
# print("4. Is temperature good OR no clouds?", (temperature > 20 or not is_cloudy))
# print("\nFinal result - Good day for solar energy production:", result)




# # Initialize variables
# has_licence = True
# has_space = True
# has_experience = False

# # Calculate conditions
# can_sell_regular_pet = (has_licence or has_experience) and has_space
# can_sell_exotic_pet = (has_licence and has_experience) and has_space
# cannot_sell_any_pet = not(has_licence or has_experience) or not(has_space)

# # Don't delete the lines below
# print("Can sell regular pet:", can_sell_regular_pet)
# print("Can sell exotic pet:", can_sell_exotic_pet)
# print("Cannot sell any pet:", cannot_sell_any_pet)




# a = 12
# b = 11

# # Don't change below this line
# c = 0
# if a >= b and not b < 10:
#     c = 2

# c += 1
# print(f"c = {c}")




# wind = int(input()) # Don't change this line
# status = "unset"
# # Type your code below
# if wind < 8:
#     status = "Calm"
# elif wind >= 8 and wind <= 31:
#     status = "Breeze"
# elif wind >= 32 and wind <= 63:
#     status = "Gale"
# else:
#     status = "Storm"

# # Don't change the line below
# print(f"status = {status}")




# n1 = int(input()) # Don't change this line
# n2 = int(input()) # Don't change this line
# op = input() # Don't change this line
# result = 0

# if op == "+":
#     result = n1 + n2
# elif op == "-":
#     result = n1 - n2
# elif op == "/":
#     result = n1 / n2
# elif op == "*":
#     result = n1 * n2

# # Don't change the line below
# print(f"result = {result}")




# # Get age as an integer
# age = int(input())

# # Get parental guidance as a boolean (True/False)
# with_parent = input() == "True"

# # Write your nested if-else code here
# if age >= 18:
#     print("You can watch any movie")
# elif age < 18:
#     if with_parent == True:
#         print("You can watch PG-13 movies")
#     elif with_parent == False:
#         print("You can only watch G-rated movies")




# # Type your code below
# x = 15
# y = 4
# z = 23
# w = x // y
# v = z // x
# u = z // y

# # Don't change the line below
# print(f"x = {x}")
# print(f"y = {y}")
# print(f"z = {z}")
# print(f"w = {w}")
# print(f"v = {v}")
# print(f"u = {u}")




# # Type your code below
# score = 100
# score /= 2
# score += 10
# score *= 3

# # Don't change the line below
# print(f"score = {score}")




# # Type your code below
# x = 15
# y = 10
# z = x <= y

# # Don't change the line below
# print(f"x = {x}, y = {y}, z = {z}")




# # Type your code below
# x1 = True
# x2 = False

# # Don't change the lines below
# x3 = x1 and x2
# print(f"x3 = {x3}")




# # Replace the values with booleans
# a = True
# b = True
# c = False

# # This line checks if (a or b) and not c is True
# result = (a or b) and not c

# # Don't change the line below
# print(f"result = {result}")




# # Initialize variables
# is_sunny = True
# temperature = 25
# wind_speed = 10
# water_temperature = 22

# # Calculate conditions
# can_go_hiking = is_sunny and temperature > 15 and wind_speed < 20
# can_go_swimming = is_sunny and temperature > 20 and water_temperature > 18
# cannot_go_outside = not is_sunny and temperature < 10 or wind_speed > 30

# # Don't delete the lines below
# print("Can go hiking:", can_go_hiking)
# print("Can go swimming:", can_go_swimming)
# print("Cannot go outside:", cannot_go_outside)




# # Initialize variables
# has_license = True
# has_experience = False
# has_clean_record = True

# # Calculate conditions
# can_drive_car = has_license and has_clean_record
# can_drive_truck = has_license and has_experience and has_clean_record
# cannot_drive_any = not(has_license and has_clean_record)

# # Don't delete the lines below
# print("Can drive car:", can_drive_car)
# print("Can drive truck:", can_drive_truck)
# print("Cannot drive any:", cannot_drive_any)




# # Initialize variables
# a = 1
# b = 2

# # Don't change below this line
# c = 0
# if a < b or b >= 10:
#     c = 2

# c += 1
# print(f"c = {c}")




# temperature = int(input()) # Don't change this line
# weather = "unset"
# # Type your code below
# if temperature < 0:
#     weather = "Freezing"
# elif temperature >= 0 and temperature <= 15:
#     weather = "Cold"
# elif temperature >= 16 and temperature <= 25:
#     weather = "Mild"
# else:
#     weather = "Hot"

# # Don't change the line below
# print(f"weather = {weather}")




# level = int(input()) # Don't change this line
# has_training = input() == "True" # Don't change this line

# # Write your code below
# if level >= 1 and level <= 5:
#     print("Basic weapons only")
# elif level >= 6 and level <= 10:
#     if has_training == False:
#         print("Need weapon training first")
#     elif has_training == True:
#         print("Access to advanced weapons granted")
# elif level >= 11:
#     print("Access to all weapons granted")
# elif level <= 0:
#     print("Invalid level")




# name = input()
# age = int(input())
# future_age = age + 10
# # Write code here
# print(f"In 10 years, {name} will be {future_age} years old.")




# var1 = int(input())
# var2 = float(input())
# result = var1 * var2

# print(result)




# var1 = float(input())
# var2 = float(input())
# result = var1 / var2

# print(result)




# year = int(input())
# supp = 120 - year

# print(f"{supp} years till 120")




# num = int(input())
# if num == 1:
#     print('T')
# else:
#     print('F')




# print("Bill Split Calculator")

# bill_amount = float(input())
# tip_percentage = float(input())
# participants = int(input())

# tip_amount = (tip_percentage / 100) * bill_amount
# total_amount = bill_amount + tip_amount
# amount_per_person = total_amount / participants

# print(f"Total (including the tip): ${total_amount}")
# print(f"Each person pays: ${amount_per_person}")




# for i in range(3, 28):
#     print(f"Hello Coddy: {i}")




# # Type your code below
# count_even = 0
# for i in range(10, 51):
#     if i % 2 == 0:
#         count_even += 1

# # Don't change the line below
# print(f"count_even = {count_even}")




# num = float(input())

# while num >= 3.5:
#     num /= 2

# print(num)




# number = float(input())
# # Write your code below
# while number >= 2.5:
#     number /= 3

# print(number)




# for i in range(1, 11):
#     if i == 6:
#         break
#     print(i)




# num1 = int(input())
# num2 = int(input())


# for num in range(num1, num2):
#     if num > 5 and num % 2 == 0:
#         print(f"First even number greater than 5: {num}")
#         break

# for num in range(num1, num2):
#     if num % 7 == 0:
#         print(f"First number divisible by 7: {num}")
#         break




# for i in range(1, 21):
#     if i % 2 == 1:
#         continue
#     print(i)




# for i in range(1, 101):
#     if i % 3 == 0:
#         continue
#     print(i)




# n = int(input())
# res = 1

# for i in range(1, n + 1):
#     res *= i
# print(res)




# def print_range(start, end, step):
#     # Write your code here
#     for i in range(start, end, step):
#         print(i)
#     pass

# # Get input from user
# start = int(input())
# end = int(input())
# step = int(input())

# # Call the function
# print_range(start, end, step)




# # Task 1: Numbers divisible by 4 between 30-80
# print("Numbers divisible by 4 between 30-80:")
# # Your code here
# for i in range(30, 81):
#     if i % 4 == 0:
#         print(i, end=", ")

# print()  # new line
# # Task 2: First 8 odd numbers from 15
# print("\nFirst 8 odd numbers from 15:")
# # Your code here
# for i in range(15, 31):
#     if i % 2 == 1:
#         print(i, end=", ")

# print()  # new line
# # Task 3: Counting backwards, divisible by 5
# print("\nCounting backwards, divisible by 5:")
# # Your code here
# for i in range(50, 9, -1):
#     if i % 5 == 0:
#         print(i, end=", ")

# print()  # new line
# # Task 4: Product of numbers divisible by 3
# print("\nProduct of numbers divisible by 3 (1-30):")
# # Your code here
# product = 1
# for i in range(1, 31):
#     if i % 3 == 0:
#         product *= i
# print(product)  # new line




# def print_pattern(rows, cols):
#     # Write your code here
#     for i in range(rows):
#         for j in range(cols):
#             print('*', end='')
#         print()
#     pass

# # Get input for rows and columns
# rows = int(input())
# cols = int(input())

# # Call the function
# print_pattern(rows, cols)




# def find_pairs(n):
#     pairs = []
#     for i in range(1, n + 1):
#         for j in range(1, n + 1):
#             if i * j == n:
#                 pairs.append((i, j))
#     return pairs

# # Get user input
# num = int(input("Enter an integer: "))

# # Find and print pairs
# print("Pairs of numbers that multiply to give", num, ":")
# pairs = find_pairs(num)
# for pair in pairs:
#     print(pair[0], pair[1])




# n = int(input())
# # Write your code below
# for i in range(1, n + 1):
#     for j in range(1, n + 1):
#         if i * j == n:
#             print(i, j)




# count = int(input())
# res = 0

# for i in range(count):
#     num = int(input())
#     res += num
# print(res)




# def sum_numbers():
#     total = sum(range(1, 10001))
#     print(total)

# num = int(input())

# for i in range(num):
#     sum_numbers()




# def hello_function():
#     print("Hello Function!")

# n = int(input())
# # Write your code below
# for i in range(n):
#     hello_function()




# def prod(a, b):
#     suppa = a * b
#     print(suppa)

# num1 = int(input())
# num2 = int(input())

# prod(num1, num2)




# def calculate_area(length, width):
#     # Write your code below
#     suppa = length * width
#     print(suppa)

# length = float(input())
# width = float(input())
# # Call the function below
# calculate_area(length, width)




# def fug():
#     return 100

# number = fug()

# print(fug())




# def square_number(n):
#     return n ** 2

# num = int(input())
# result = square_number(num)

# print(result)




# def sigma(n):
#     return sum(range(1, n + 1))




# def is_valid(username, password):
#     # Write code here
#     if username == "admin":
#         return True
#     elif username == "user" and password == "qweasd":
#         return True
#     else:
#         return False




# def fizzbuzz(num):
#     if num % 3 == 0 and num % 7 == 0:
#         return "FizzBuzz"
#     elif num % 7 == 0:
#         return "Buzz"
#     elif num % 3 == 0:
#         return "Fizz"
#     elif '3' in str(num):
#         return "Almost Fizz"
#     else:
#         return str(num)

# print("Welcome to FizzBuzz!")
# n = int(input())

# for i in range(1, n + 1):
#     print(fizzbuzz(i))




# shopping_list = ["bread", "eggs", "milk", "butter"]
# print(f"shopping_list = {shopping_list}")




# def values(my_list):
#     # Write code here
#     for i in range(len(my_list)):
#         print(my_list[i])

# my_list = [10, 20, 30, 40, 50]
# values(my_list)




# def change_element(lst, index, new_element):
#     # Write code here
#     lst[index] = new_element
#     return lst

# # Test the function
# my_list = [1, 2, 3, 4, 5]
# print(change_element(my_list, 2, 10))




# def change_element(first_list, index, second_list):
#     # Replace the element at the given index in the first list with the first element of the second list.
#     first_list[index] = second_list[0]
#     return first_list

# # Example usage:
# result = change_element([1, 2, 3], 1, [5, 6, 7])
# print(result)  # Output: [1, 5, 3]




# def merge(lst1, lst2):
#     # Write code here
#     merge_list = lst1 + lst2
#     merge_list.sort()
#     return merge_list




# def combine_and_filter(lst, threshold):
#     # Write code here
#     # Combine the list with itself and filter out elements that are less than the threshold
#     filtered_list = [i for i in lst if i > threshold]
#     filtered_list.sort()
#     return filtered_list

# result = combine_and_filter([1, 5, 3, 2, 7, 4], 3)
# print(result)




# import math
# def prod(lst):
#     # Write code here
#     return math.prod(lst)




# def reverse(lst):
#     # Write code here
#     reversed_list = []
#     for number in lst:
#         reversed_list.insert(0, number)
#     return reversed_list




# lst = input().split(",")
# # Write your code below
# for word in lst:
#     if len(lst) >= 5:
#         print(lst)




# lst = input().split(",")
# # Write your code below
# long_words = [word for word in lst if len(lst) > 5]
# for word in long_words:
#     print(lst)




# lst = input().split(",")
# # Write your code below
# def filter_long_words(words):
#     long_words = [word for word in words if len(word) > 5]
#     return long_words

# result = filter_long_words(lst)
# print(result)




# lst = input().split(",")
# new_lst = []
# for item in lst:
#     if len(item) > 5:
#         new_lst.append(item)
# print(new_lst)




