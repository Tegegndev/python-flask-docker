from core import WinzaClient

def main():
    client = WinzaClient()
    phone = input("Enter phone number: ")
    password = input("Enter password: ")
    amount = float(input("Enter deposit amount: "))

    login_result = client.login(phone, password)
    if not login_result:
        print("User not found or login failed. Trying to register...")
        reg_result = client.register_user(phone, password)
        if reg_result and reg_result.get("IsSuccess"):
            print("Registration successful. Logging in...")
            login_result = client.login(phone, password)
            if not login_result:
                print("Login failed after registration. Exiting.")
                return
        else:
            print("Registration failed.")
            return
    print("Login successful!")
    deposit_result = client.deposit(amount)
    print("Deposit result:", deposit_result)

if __name__ == "__main__":
    main()
