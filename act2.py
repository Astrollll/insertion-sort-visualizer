num = int(input("Enter a number: "))

#finding the sum of all the numbers from 1 to num
sum = 0
for i in range(1, num + 1):
    sum += i
print(f"The sum of the first {num} integers is {sum}")