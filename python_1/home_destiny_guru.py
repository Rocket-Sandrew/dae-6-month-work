print("Welcome to your Home Destiny Guru!")

#hard coding these values to represent user's credentials
correct_username = "admin"
correct_password = "LET ME IN"

#hard coding weather for now
computer_weather = 76
retry = 1

#ask user for their user name and password
user_name = input("Please enter Username: ")
password = input("Thank you " + user_name + ", please also enter password: ")

#stop them if at least one of these are true
while user_name!= correct_username or password!= correct_password:
    #ask user again for their user name and password
    print("Access deneied! Incorrect username or password!")
    user_name = input("Please re-enter username: ")
    password = input("Please re-enter password: ")
print("Welcome to our menu",user_name + "!")

while retry:
    #ask user for location and save
    # location = input("Where are you? at work or home? ")
    at_home = int(input( "where are you? Press 1 for Home, 0 for work: ") )
    # location_as_str = input("where are you? Press 1 for Home, 2 for work")
    # location_as_int = int(location_as_str)
    location = "Home" if at_home else "Work"

    raining = int( input("Is it raining? Press 1 for yes, 0 for no: ") )

    #condition used if location isn't entered as text
    # if raining and location_as_int == 1:
    #     print("Stay home")
    # elif raining and location_as_int == 2:
    #     print("Stay at work")
    # elif location_as_int == 1:
    #     print("Go to work")
    # else :
    #     print("Go home")

    #condition used if we can save direct location instead of using numbers
    print("Stay at", location) if raining else print("Go",location)
    # if raining:
    #     print("Stay at", location)
    # else:
    #     print("Go",location)

    #condition if at_home and raining variables used
    # if raining and at_home:
    #     print("Stay home")
    # elif raining and not at_home:
    #     print("Stay at work")
    # elif not raining and at_home:
    #     print("Go to work")
    # elif not raining and not at_home:
    #     print("Go home")

    print("Thank you for using this application!")

    user_response = input("Would you like to try again? Press y/n: ")

    # if user_response == "n":
    #     retry = 0
    
    while user_response != "y" and user_response != "n":
        user_response = input("Hey, please only enter y or n, Nothing else: ")
        # if user_response == "y":
        #     retry = 1
        # else:
        #     retry = 0

    retry = 1 if retry == "y" else 0
print("Bye!")