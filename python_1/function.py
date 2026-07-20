#function without parameters
def great_user():
    print("---------------------------------")
    print("Hello world! :3")
    print("Hope you have a nice day! :3")
    print("---------------------------------")

#function with a parameter
def great_user(user_name):
    print("---------------------------------")
    print("Hello", user_name)
    print("Hope you have a nice day! :3")
    print("---------------------------------")

#function with multiple parameters
def great_user(user_name, home_town):
    print("---------------------------------")
    print(user_name, home_town)
    print("---------------------------------")
#call function without an argument
# great_user()

#call a function with an argument
# great_user("Andrew")
# great_user(input( "What's your name? ") )

#call a function with multiple aruments
name = input("What is your name? ")
town = input("What is your hometown? ")

great_user(name,town)