
# NAME: Anangafac Alabaweh


#This program allows users to manipulate a network of members by adding,
# removing, searching and displaying members. The program starts by prompting the user to enter two data files, one
# for profile information and the other for connection information. The program then initializes the data
# and stores it into lists. After that, it displays a menu to the user and based on the user's selection,
# the program will execute the appropriate command. The possible commands include displaying member information,
# listing the number of a member's friends, listing the friends of a member, displaying the graph of the network,
# recommending a friend to a member, searching for members from a particular country and saving the changes.
# Finally, the program exits when the user selects the exit option.

from Graph import *
from typing import IO, Tuple, List


#  this is for the menu item selection
PROGRAMMER = "Alaba"
MEMBER_INFO = "1"
NUM_OF_FRIENDS = "2"
LIST_OF_FRIENDS = "3"
RECOMMEND = "4"
SEARCH = "5"
ADD_FRIEND = "6"
REMOVE_FRIEND = "7"
SHOW_GRAPH = "8"
SAVE = "9"

LINE = "\n*-*_*-*_*-*_*-*_*-*_*-*_*-*_*-*_*-*_*-*_*-*_*-*_*-*_*-*_*-*\n"


# creating a class to hold members information
class Member:
    # initializing class variables
    def __init__(self, member_id: int,
                 first_name: str,
                 last_name: str,
                 email: str,
                 country: str):
        self.member_id = member_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.country = country

        #self.friends_id_list = []
    # this function allows members to add friends
    def add_friend(self, friend_id) -> None:

        if friend_id in self.friends_id_list:
            print("This person is already your friend.")
        else:
            self.friends_id_list.append(friend_id)
    # this will remove friends from the members list
    def remove_friend(self, friend_id) -> None:

        if friend_id in self.friends_id_list:
            self.friends_id_list.remove(friend_id)
        else:
            print("You don't have this friend in your list.")
    # this function returns a list of the members friends
    def friend_list(self) -> List[int]:
        return self.friends_id_list
    # this function returns the number of friends a member has in their list
    def number_of_friends(self) -> int:
        return len(self.friends_id_list)


    def __str__(self) -> str:
        return f"{self.member_id}: {self.first_name} {self.last_name} " \
               f"\n{self.email} {self.country}"

# opening and reading the contents of the file
def open_file(file_type: str) -> IO:
    # prompting the user to enter a filename
    file_name = input("Enter the " + file_type + " filename:\n")
    # setting the file pointer to None
    file_pointer = None
    # loop to make sure the file is valid
    while file_pointer is None:
        try:
            file_pointer = open(file_name, "r")
        # exception handling for an error occuring when opening the file
        except IOError:
            print(f"An error occurred while opening the file {file_name}.\n"
                  f"Make sure the file path and name are correct \nand that "
                  f"the file exist and is readable.")
            # asking for a new filename if an error occurs
            file_name = input("Enter the " + file_type + " filename:\n")

    return file_pointer

# creating the network of friends
def create_network(fp: IO) -> List[List[int]]:
    # reading the first line of the file which is the size of the network
    size = int(fp.readline())
    connection = []
    # creating an empty list
    for i in range(size):
        connection.append([])
    # loop to read each line
    line = fp.readline()
    while line is not None and len(line) >= 3:
        # splitting the lines
        split_line = line.strip().split(" ")
        # adding the connections to the list
        connection[int(split_line[0])].append(int(split_line[1]))
        connection[int(split_line[1])].append(int(split_line[0]))
        # reading the next line
        line = fp.readline()
    # returning the created network
    return connection

# creating the members list
def create_members_list(profile_fp: IO) -> List[Member]:

    profiles = []
    # reading the first line of the file
    profile_fp.readline()
    # reading the next line
    line = profile_fp.readline()
    # splitting the line
    profile_list = line.strip().split(',')
    # loop to read each line
    while line is not None and len(profile_list) == 5:
        # creating a member and adding it to the list
        profiles.append(Member(int(profile_list[0]),
                               profile_list[1],
                               profile_list[2],
                               profile_list[3],
                               profile_list[4]))
        # reading the next line
        line = profile_fp.readline()
        # splitting the line
        profile_list = line.strip().split(',')
    # returning the list of members
    return profiles

# this function is used to find the number of items in common between two lists
def num_in_common_between_lists(list1: List, list2: List) -> int:
    degree = 0
    # looping through both lists
    for i in range(len(list1)):
        # checking if the item is in both lists
        if list1[i] in list2:
            # incrementing the degree if the item is in both lists
            degree += 1

    return degree

# this function is used to initialize the matrix
def init_matrix(size: int) -> List[List[int]]:
    matrix = []
    # looping through the size
    for row in range(size):
        matrix.append([])
        # looping through the row
        for column in range(size):
            # setting each value to 0
            matrix[row].append(0)

    return matrix

# this function calculates the similarity score between each member
def calc_similarity_scores(profile_list: List[Member]) -> List[List[int]]:
    # initializing the matrix
    matrix = init_matrix(len(profile_list))

    # looping through the list of members
    for i in range(len(profile_list)):
        # looping through the list of members
        for j in range(i, len(profile_list)):
            # getting the number of items in common between the two lists
            degree = num_in_common_between_lists(profile_list[i].friends_id_list,
                                                 profile_list[j].friends_id_list)
            # setting the value of the matrix to the degree
            matrix[i][j] = degree
            matrix[j][i] = degree

    return matrix

# this function is used to search through the frinds relationship and recommned friends
# for member_id who aren't friends
def recommend(member_id: int, friend_list: List[int], similarity_list: List[int]) -> int:
    # setting the max similarity to -1
    max_similarity_val = -1
    max_similarity_pos = -1

    # looping through the list of similarities
    for i in range(len(similarity_list)):
        # checking if the member is not in the friends list and is not the same member
        if i not in friend_list and i != member_id:
            # checking if the similarities is greater than the max
            if max_similarity_val < similarity_list[i]:
                # setting the max similarity position and value
                max_similarity_pos = i
                max_similarity_val = similarity_list[i]

    # returning the max similarity position
    return max_similarity_pos



# this is to dsiplay the menu so the user can select from
def display_menu():
    print("\nPlease select one of the following options.\n")
    print(MEMBER_INFO + ". Show a member's information \n" +
          NUM_OF_FRIENDS + ". Show a member's number of friends\n" +
          LIST_OF_FRIENDS + ". Show a member's list of friends\n" +
          RECOMMEND + ". Recommend a friend for a member\n" +
          SEARCH + ". Search for a member's country\n" +
          ADD_FRIEND + ". Add a connection between two members\n" +
          REMOVE_FRIEND + ". Remove a connection between two members\n" +
          SHOW_GRAPH + ". Show the graph\n" +
          SAVE + ". Save the changes\n"
          )
    # prompt the user to select a menu item or press any key to exit
    return input("Press any other key to exit.\n")


# this is to validate and make sure the user ID is within range
# and entered correctly
def receive_verify_member_id(size: int):
    valid = False
    # prompt the user to enter the member ID
    while not valid:
        member_id = input(f"Please enter a member id between 0 and {size}:\n")
        # check if the user entered a valid ID
        if not member_id.isdigit():
            print("This is not a valid entry.")
        elif not 0 <= int(member_id) < size:
            print(f"The member id must be between 0 and {size}.")
        else:
            valid = True

    return int(member_id)


# this function is used to connect friends who weren't already friends
def add_friend(profile_list: List[Member],
               similarity_matrix: List[List[int]]) -> None:
    size = len(profile_list)
    print("For the first friend: ")
    # prompt the user to enter the first friend's ID
    member1 = receive_verify_member_id(size)
    print("For the second friend: ")
    # prompt the user to enter the second friend's ID
    member2 = receive_verify_member_id(size)
    # check if the user entered two different IDs
    if member1 == member2:
        print("You need to enter two different ids. Please try again.")
    # check if the members are already friends
    elif member1 in profile_list[member2].friends_id_list:
        print("These two members are already friends. Please try again.")
    else:
        # add the connection between the two members
        profile_list[member1].add_friend(member2)
        profile_list[member2].add_friend(member1)
        print("The connection is added. Please check the graph.")


# this function is used to disconnect members who are friends, unfriend the members
# based on the user's input
def remove_friend(profile_list: List[Member],
                  similarity_matrix: List[List[int]]) -> None:
    size = len(profile_list)
    print("For the first friend: ")
    # prompt the user to enter the first friend's ID
    member1 = receive_verify_member_id(size)
    print("For the second friend: ")
    # prompt the user to enter the second friend's ID
    member2 = receive_verify_member_id(size)
    # check if the user entered two different IDs
    if member1 == member2:
        print("You need to enter two different ids. Please try again.")
    # check if the members are already friends
    elif member1 not in profile_list[member2].friends_id_list:
        print("These two members are not friends. Please try again.")
    else:
        # remove the connection between the two members
        profile_list[member1].remove_friend(member2)
        profile_list[member2].remove_friend(member1)
        print("The connection is removed. Please check the graph.")


# This function asks for a country name and list all members from that country.
def search(profile_list: List[Member]) -> None:
    # prompt the user to enter the country name
    pays = (input("Enter a country name\n")).lower()
    found=False
    # searching if the user are from the same country and display the results
    for i in range(len(profile_list)):
        # check each member's country
        if pays== (profile_list[i].country).lower():
            # print the member's info if the country matches
            print(f"{i}. {profile_list[i].first_name} {profile_list[i].last_name}")
            found=True
    # print a message if no member is found in the country
    if found == False:
        print("No Member found in this country")



def add_friends_to_profiles(profile_list: List[Member],
                            network: List[List[int]]) -> None:
    # loop through each member
    for i in range(len(profile_list)):
        # add the member's friends' ID to the list
        profile_list[i].friends_id_list = network[i]


# based on the user menu selection, this function will execute the menu command
def select_action(profile_list: List[Member],
                  network: List[List[int]],
                  similarity_matrix: List[List[int]]) -> str:
    response = display_menu()
    print(LINE)
    size = len(profile_list)

    if response in [MEMBER_INFO, NUM_OF_FRIENDS, LIST_OF_FRIENDS, RECOMMEND]:
        # prompt the user to enter the member's ID
        member_id = receive_verify_member_id(size)

    if response == MEMBER_INFO:
        # print the first_name  from country has number of friends
        print(f"{profile_list[member_id].first_name} {profile_list[member_id].last_name}\n{profile_list[member_id].email}\nFrom "
              f"{profile_list[member_id].country} Has {len(profile_list[member_id].friends_id_list)} friends.")

    elif response == NUM_OF_FRIENDS:
        # this will print the number of friends
        print(f" {profile_list[member_id].first_name} has {len(profile_list[member_id].friends_id_list)} friends.")
    elif response == LIST_OF_FRIENDS:
        # this will print the list of friends
        n=len(profile_list[member_id].friend_list())
        for i in range(n):
            k=profile_list[member_id].friends_id_list[i]
            print(f" {k} {profile_list[k].first_name} {profile_list[k].last_name}\n")
    elif response == RECOMMEND:
        # this will print the recommended friends relative to the member_id
        friend_list = profile_list[member_id].friend_list()
        k=recommend(member_id, friend_list, similarity_matrix[member_id])
        print(f" The Suggested friends for {profile_list[member_id].first_name} {profile_list[member_id].last_name} "
              f"is {profile_list[k].first_name} {profile_list[k].last_name} with id {k} ")

    elif response == SEARCH:
        # this will display the same members from the same country
        search(profile_list)
    elif response == ADD_FRIEND:
        # this will add two members as friends
        add_friend(profile_list, similarity_matrix)
    elif response == REMOVE_FRIEND:
        # this will remove two members as friends
        remove_friend(profile_list, similarity_matrix)
    elif response == SHOW_GRAPH:
        # this will display the friendship graph
        tooltip_list = []
        for profile in profile_list:
            tooltip_list.append(profile)
        graph = Graph(PROGRAMMER,
                      [*range(len(profile_list))],
                      tooltip_list, network)
        graph.draw_graph()
        print("Graph is ready. Please check your browser.")
    elif response == SAVE:
        # this will save the changes to the file
        save_changes(profile_list)
    else:
        return "Exit" # for the user to exit the program

    print(LINE)

    return "Continue"

# this function will save the chnages based int the user's manipulation
# this is done by saving the connection as a new connection file
def save_changes(profile_list: List[Member]) -> None:
    file_name = input("Enter the filename to save the changes: ")
    try:
        with open(file_name, 'w') as file:
            file.write(str(len(profile_list)) + '\n')
            for profile in profile_list:
                friends_list = profile.friend_list()
                for friend in friends_list:
                    file.write(str(profile.member_id) + ' ' + str(friend) + '\n')
        print("The changes are saved.")
    except IOError:
        print("An error occurred while saving the file.")


    # this function opens and read the files, then saves them to list so that it can be used later on
    # in the  program as it executes
def initialization() -> Tuple[List[Member], List[List[int]], List[List[int]]]:
    profile_fp = open_file("profile")
    profile_list = create_members_list(profile_fp)

    connection_fp = open_file("connection")
    network = create_network(connection_fp)
    add_friends_to_profiles(profile_list, network)
    similarity_matrix = calc_similarity_scores(profile_list)

    profile_fp.close()
    connection_fp.close()

    return profile_list, network, similarity_matrix

#  Do not change.
def main():
    print("Welcome to the network program.")
    print("We need two data files.")
    profile_list, network, similarity_matrix = initialization()
    action = "Continue"
    while action != "Exit":
        action = select_action(profile_list, network, similarity_matrix)

    input("Thanks for using this program.")


if __name__ == "__main__":
    main()
