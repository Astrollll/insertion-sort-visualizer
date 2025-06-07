#Finding the sum of integers using recursion
def treesum(n):
    # Base case: if n is 1, return 1
    if n == 1:
        return 1
    # Recursive case: add current number to sum of previous numbers
    else:
        return n + treesum(n - 1)

def main():
    try:
        # Get first number and calculate its sum
        num1 = int(input("Enter the first number: "))
        if num1 < 1:
            print("Please enter a positive integer!")
            return
        result1 = treesum(num1)
        print(f"The sum of the first {num1} integers is {result1}")

        # Get second number and calculate its sum
        num2 = int(input("Enter the second number: "))
        if num2 < 1:
            print("Please enter a positive integer!")
            return
        result2 = treesum(num2)
        print(f"The sum of the first {num2} integers is {result2}")

        # Calculate and display the total sum
        total_sum = result1 + result2
        print(f"The sum of both results is: {total_sum}")

    except ValueError:
        print("Please enter a valid integer!")

if __name__ == "__main__":
    main()
    