def myLoad(bal):
    while bal > 0:
        print(f"Current balance: {bal}")
        mobile = input("Enter mobile number: ")
        amt = float(input("Enter amount to load: "))
        if amt > 0 and amt <= bal:
            bal -= amt
            print(f"Loaded {amt} to {mobile}.")
            print(f"New balance is {bal}\n")
        elif amt > bal:
            print("Insufficient balance. Try a smaller amount.\n")
        else:
            print("Invalid amount. Please enter a positive value.\n")
    print("zero balance")

myB = float(input("Enter initial balance: "))
myLoad(myB)