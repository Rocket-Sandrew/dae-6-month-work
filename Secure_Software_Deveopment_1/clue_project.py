#import needed libraries
import random
import time

#creating each deck of clue cards
rooms = ["Billiard room", "Ball room", "Conservatory", "Dinning room", "Hall", "Kitchen", "Library", "Lounge", "Study"]
suspects = ["Professor Plum","Mr. Green", "Colonel Mustard", "Dr. Orchid", "Mrs. Peacock", "Miss Scarlet"]
weapons = ["Knife", "Lead pipe", "Revolver", "Poison", "Rope", "Wrench"]

#creating variables for answer to crime
truth = ""

#variable for player hand and hidden hand
player_hand = []
hidden_hand = []

#variable for player's charachter, chosen during gameplay
player_character = ""

#variable for player notebook of clues they know to not be the answer for each deck
notebook = rooms.copy() + suspects.copy() + weapons.copy()

#function to allow user to choose character to play as
def choose_character():
    print_numbered_list(suspects)
    player_character = input("\nPlease press a number from the list above to choose your character: ")
    
    player_character = validate_input(player_character,suspects)
    print("Thank you for choosing to play as", player_character)
    time.sleep(1)
    
    return player_character

#function to set up answer to game
def file_crime():
    #creating copies of the decks so they can be shuffled safely
    rooms_in_play = rooms.copy()
    suspects_in_play = suspects.copy()
    weapons_in_play = weapons.copy()
    
    random.shuffle(rooms_in_play)
    random.shuffle(suspects_in_play)
    random.shuffle(weapons_in_play)
    print("Clue cards shuffled, Now picking the truth of the case.")
    time.sleep(1)
    
    culprit = suspects_in_play.pop()
    scene = rooms_in_play.pop()
    murder_weapon = weapons_in_play.pop()
    truth_of_the_case = culprit + " used the " + murder_weapon + " To kill the victim in the " + scene
    print("Truth hidden by culprit, shuffling remaining clues.")
    time.sleep(1)
    
    full_deck_in_play = rooms_in_play + suspects_in_play + weapons_in_play
    random.shuffle(full_deck_in_play)
    print("Remaining clues shuffled.")
    time.sleep(1)
    
    deal_cards(full_deck_in_play)
    return truth_of_the_case

#function to deal cards to player and a hidden hand evenly
def deal_cards(deck):
    print("Dealing remaining clues")
    time.sleep(1)
    card_in_deck = 0
    for card in deck:
        player_hand.append(card) if card_in_deck %2 == 0 else hidden_hand.append(card)
        card_in_deck += 1
    print("\nHere are the clues you were given: ")
    time.sleep(1)
    print(player_hand)
    time.sleep(1)

#function to edit a list "notebook" for players to keep track of clues they eliminated as possibilities
def edit_notebook(clues):
    print("\nAdding new clues to notebook")
    time.sleep(1)
    for index in range(len(notebook)):
        if notebook[index] in clues and not notebook[index].endswith("X"):
            notebook[index] += " X"
    return notebook

#function to print notebook as three list separated by room, suspect and weapon
def show_notebook():
    card_in_notebook = 0
    room_files = []
    suspect_files = []
    weapon_files = []
    while card_in_notebook < len(notebook):
        if notebook[card_in_notebook].removesuffix(" X") in rooms:
            room_files.append(notebook[card_in_notebook])
        elif notebook[card_in_notebook].removesuffix(" X") in suspects:
            suspect_files.append(notebook[card_in_notebook])
        else:
            weapon_files.append(notebook[card_in_notebook])
        card_in_notebook+= 1
    print("", room_files, suspect_files, weapon_files, "", sep = "\n")

#function to return notebook to the state it started in for when user wants to play again
def reset_notebook():
    print("Reseting clues in notebook")
    time.sleep(1)
    for index_to_reset in range(len(notebook)):
        if notebook[index_to_reset].endswith(" X"):
            notebook[index_to_reset] = notebook[index_to_reset].removesuffix(" X")
    return notebook

#function that let's player move to room and create a theory on the case
def player_turn(player_character, turn_counter):
    print("\nTime to investigate,", player_character)
    turn_counter += 1
    time.sleep(1)

    print("Turn:", str(turn_counter))
    time.sleep(1)

    print_numbered_list(rooms)
    show_notebook()
    room_theory = input("Please press a number from the list above to move to a room and investigate: ")
    room_theory = validate_input(room_theory, rooms)
    print("\nNow moving to", room_theory)
    time.sleep(1)
    
    print_numbered_list(suspects)
    show_notebook()
    criminal_theory = input("Please press a number from the list above to question a suspect: ")
    criminal_theory = validate_input(criminal_theory, suspects)
    print("\nNow questioning the alibi of", criminal_theory)
    time.sleep(1)
    
    print_numbered_list(weapons)
    show_notebook()
    weapon_theory = input("Please press a number from the list to pose your theory on their murder weapon: ")
    weapon_theory = validate_input(weapon_theory, weapons)
    print("\nNow let's see what", criminal_theory,"Thinks about", player_character + "'s theory of the case")
    time.sleep(1)

    new_evidence = test_theory(room_theory,criminal_theory,weapon_theory, player_character)
    time.sleep(2)
    existing_evidence = double_check(room_theory,criminal_theory,weapon_theory)
    time.sleep(2)
    return new_evidence, existing_evidence, turn_counter


#function to check player theory against list "hidden_hand"
def test_theory(crime_scene, criminal, murder_weapon, player_character):
    disproving_clues = []
    for card in range(len(hidden_hand)):
        if hidden_hand[card] == crime_scene:
            disproving_clues.append(hidden_hand[card])
        elif hidden_hand[card] == criminal:
            disproving_clues.append(hidden_hand[card])
        elif hidden_hand[card] == murder_weapon:
            disproving_clues.append(hidden_hand[card])
    random.shuffle(disproving_clues)
    
    if disproving_clues == []:
        print("\n"+criminal,"can't disprove", player_character + "'s theory")
        return False
    else:
        print("\n" + criminal, "finds and provides evidence showing",disproving_clues[0],"is not involved in this case")
        edit_notebook(disproving_clues[0])
        return True

# function to check player theory against players own cards 
def double_check(crime_scene, criminal, murder_weapon):
    if crime_scene in player_hand:
        print("You can disprove this crime scene")
        return True
    elif criminal in player_hand:
        print("You can disprove this suspect")
        return True
    elif murder_weapon in player_hand:
        print("You can disprove this murder weapon")
        return True
    else:
        print("You can't disprove this theory with any evidence you had at the start of the party")
        return False

#function for printing a numbered list for input purposes
def print_numbered_list(list):
    print("")
    for index_to_show in range(len(list)):
        print(str(index_to_show)+".", list[index_to_show])

#function to check that input "clue" is a number in the index of list "clue cards"
def validate_input(clue, clue_cards):
    input_valid = False
    while not input_valid:
        try:
            clue = int(clue)
            if clue < len(clue_cards) and clue >= 0:
                input_valid = True
                clue = clue_cards[clue]
            else:
                raise ValueError
        except ValueError:
            clue = input("Sorry! that doesn't work, please only enter a number from the list above: ")
    return clue

#function for final player theory, will reveal answer
def accuse(player_character, truth_of_case):
    print("\nTime for the final accusation,", player_character + "!")
    time.sleep(1)
    print_numbered_list(rooms)
    show_notebook()
    crime_scene = input("Please determine where you think the crime scene is: ")
    crime_scene = validate_input(crime_scene, rooms)
    
    print_numbered_list(suspects)
    show_notebook()
    culprit = input("Please determine who you believe the true culprit is: ")
    culprit = validate_input(culprit, suspects)
    
    print_numbered_list(weapons)
    show_notebook()
    murder_weapon = input("Please determine the murder weapon you beleive was used in the case: ")
    murder_weapon = validate_input(murder_weapon, weapons)

    accusation = culprit + " used the " + murder_weapon + " To kill the victim in the " + crime_scene
    return accusation == truth_of_case

#main function to call other functions and handle main gameplay loops
def main():
    wants_to_play_detective = True
    while wants_to_play_detective:
        turn_counter = 0
        print("""  
 __          __  _                            _               _            _ 
 \ \        / / | |                          | |             | |          | |
  \ \  /\  / /__| | ___ ___  _ __ ___   ___  | |_ ___     ___| |_   _  ___| |
   \ \/  \/ / _ \ |/ __/ _ \| '_ ` _ \ / _ \ | __/ _ \   / __| | | | |/ _ \ |
    \  /\  /  __/ | (_| (_) | | | | | |  __/ | || (_) | | (__| | |_| |  __/_|
     \/  \/ \___|_|\___\___/|_| |_| |_|\___|  \__\___/   \___|_|\__,_|\___(_)
                                                                             
                                                                                                                
               """)                
        time.sleep(1)

        print("""

  _          _   _             _                   _      _            _   _           _ 
 | |        | | ( )           | |                 | |    | |          | | (_)         | |
 | |     ___| |_|/ ___   _ __ | | __ _ _   _    __| | ___| |_ ___  ___| |_ ___   _____| |
 | |    / _ \ __| / __| | '_ \| |/ _` | | | |  / _` |/ _ \ __/ _ \/ __| __| \ \ / / _ \ |
 | |___|  __/ |_  \__ \ | |_) | | (_| | |_| | | (_| |  __/ ||  __/ (__| |_| |\ V /  __/_|
 |______\___|\__| |___/ | .__/|_|\__,_|\__, |  \__,_|\___|\__\___|\___|\__|_| \_/ \___(_)
                        | |             __/ |                                            
                        |_|            |___/                                                                                        
              """)
        time.sleep(1)

        player_character = choose_character()
        truth = file_crime()
        truth_hidden = True
        notebook = edit_notebook(player_hand)
        
        while truth_hidden:
            new_evidence, existing_evidence, turn_counter = player_turn(player_character,turn_counter)
            if not new_evidence and not existing_evidence:
                game_ending = input("\n" + player_character + " might have the answer to this case, " \
                "would you like to move to your final accusation? Press y/n: ")
        
                while game_ending != "y" and game_ending != "n":
                    game_ending = input("Hey, please only enter y or n, Nothing else: ")    
                if game_ending == "y":
                    final_theory_correct = accuse(player_character,truth)
                    if final_theory_correct:
                        print("Congratulations! Your accusation was correct! The truth of the case is: ")
                        time.sleep(1)
                        print(truth)
                        time.sleep(1)
                        print("\nGreat detective work", player_character + "!")
                    else:
                        print("Unfortunately no, your accusation was incorrect! The truth of this case was: ")
                        time.sleep(1)
                        print(truth)
                        time.sleep(1)
                        print("\nNext time you should investigate a bit more thoroughly,", player_character)
                    truth_hidden = False
        print("\nIt took you", str(turn_counter), "Turns to make your final accusation")
        time.sleep(1)
        wants_to_play_detective = input("The truth was revealed and the party is over!" \
        " Would you like to play detective again? Press y/n: ")
        
        while wants_to_play_detective != "y" and wants_to_play_detective != "n":
            wants_to_play_detective = input("Hey, please only enter y or n, Nothing else: ")

        if wants_to_play_detective == "y":
            wants_to_play_detective = 1
            print("OK! Now reseting game!")
            time.sleep(1)
            player_hand.clear()
            hidden_hand.clear()
            print("Clue cards returned to the deck")
            time.sleep(1)
            notebook = reset_notebook()
            print("Game reset, now starting again.")
            time.sleep(1)
        else:
            wants_to_play_detective = 0
    print("""

  _______ _                 _           __                   _             _             
 |__   __| |               | |         / _|                 | |           (_)            
    | |  | |__   __ _ _ __ | | _____  | |_ ___  _ __   _ __ | | __ _ _   _ _ _ __   __ _ 
    | |  | '_ \ / _` | '_ \| |/ / __| |  _/ _ \| '__| | '_ \| |/ _` | | | | | '_ \ / _` |
    | |  | | | | (_| | | | |   <\__ \ | || (_) | |    | |_) | | (_| | |_| | | | | | (_| |
    |_|  |_| |_|\__,_|_| |_|_|\_\___/ |_| \___/|_|    | .__/|_|\__,_|\__, |_|_| |_|\__, |
                                                      | |             __/ |         __/ |
                                                      |_|            |___/         |___/ 
      """)
main()