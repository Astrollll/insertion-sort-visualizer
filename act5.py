import sys

stack_size = 5
stack = [None] * stack_size
top = -1

def push_recursive(count):
    global top
    if count == 0:
        return
    if top >= stack_size - 1:
        print("Cannot push more elements")
        return

    value = input("Enter value to push: ")
    #increment top
    top += 1
    stack[top] = value
    print(f"Pushed {value}")
    
    push_recursive(count - 1)

def pop():
    global top
    if top == -1:
        print("Nothing to pop.")
        return None
    value = stack[top]
    stack[top] = None
    top -= 1
    print(f"Popped {value}")
    return value

def peek():
    if top == -1:
        print("Stack is empty")
        return None
    return stack[top]

def is_empty():
    return top == -1

def is_full():
    return top == stack_size - 1

def display():
    if top == -1:
        print("Stack is empty")
        return
    print("Stack:", stack[:top+1])

# Input validation for number of elements to push
while True:
    try:
        n = int(input(f"How many elements do you want to push? (Max: {stack_size}): "))
        if n < 0:
            print("Please enter a non-negative integer.")
        else:
            break
    except ValueError:
        print("Invalid input. Please enter an integer value.")

push_recursive(min(n, stack_size))

display()
pop()
print("Top element after popping:", peek())
display()

check_empty = is_empty()
print("Is stack empty?", check_empty)

check_full = is_full()
print("Is stack full?", check_full)