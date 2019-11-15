import random

def create_network(file_name):
     friends = open(file_name).read().splitlines()
     network = []
     clone = []

     num = int(friends.pop(0))

     for i in range(len(friends)):
          x = friends[i].split(' ')
          clone.append(x[1] + ' ' + x[0])

     friends = friends + clone
     friends.sort()

     temp = friends.pop(0).split(' ')
     entry = (temp[0], [temp[1]])

     network.append(entry)

     i = 1

     try:
         while i <= num+1:
             temp = friends.pop(0).split(' ')
             if(temp[0] == network[i-1][0]):
                 network[i-1][1].append(temp[1])
             else:
                  entry = (temp[0], [temp[1]])
                  network.append(entry)
                  i += 1

     except:
          pass

     return network

def getCommonFriends(user1, user2, network):
     common=[]
     index1 = 0
     index2 = 0

     for i in range(len(network)):
          if(int(network[i][0]) == user1):
               index1 = i
          if(int(network[i][0]) == user2):
               index2 = i

     for i in range(len(network[index1][1])):
          if(network[index1][1][i] in network[index2][1]):
               common.append(network[index1][1][i])

     common.sort()

     return common

def recommend(user, network):

     possible = []

     index1 = 0

     for i in range(len(network)):
          if(int(network[i][0]) == user):
               index1 = i

     for i in range(len(network)):
          if(i == index1 or network[i][0] in network[index1][1]):
               pass
          else:
               entry = (network[i][0],len(getCommonFriends(user,int(network[i][0]),network)))
               possible.append(entry)

     if(len(possible) == 0):
          return None

     high = 0

     for i in range(len(possible)):
          if(possible[i][1] > high):
               high = possible[i][1]

     final = []

     for i in range(len(possible)):
          if(possible[i][1] == high):
               final.append(possible[i][0])

     return int(min(final))

def k_or_more_friends(network, k):
    '''(2Dlist,int)->int
    Given a 2D-list for friendship network and non-negative integer k,
    returns the number of users who have at least k friends in the network
    Precondition: k is non-negative'''

    num = 0

    for i in range(len(network)):
        if(len(network[i][1]) >= k):
            num += 1

    return num

def maximum_num_friends(network):
    '''(2Dlist)->int
    Given a 2D-list for friendship network,
    returns the maximum number of friends any user in the network has.
    '''

    high = 0

    for i in range(len(network)):
        if(len(network[i][1]) > high):
            high = len(network[i][1])

    return high

def people_with_most_friends(network):
    '''(2Dlist)->1D list
    Given a 2D-list for friendship network, returns a list of people (IDs) who have the most friends in network.'''
    max_friends=[]

    for i in network:
        if(len(i[1]) == maximum_num_friends(network)):
            max_friends.append(i[0])

    return max_friends


def average_num_friends(network):
    '''(2Dlist)->number
    Returns an average number of friends overs all users in the network'''

    avg = 0

    for i in network:
        avg += len(i[1])

    return avg//len(network)


def knows_everyone(network):
    '''(2Dlist)->bool
    Given a 2D-list for friendship network,
    returns True if there is a user in the network who knows everyone
    and False otherwise'''

    for i in network:
        if (len(i[1]) == len(network)-1):
            return True
        else:
            return False


####### CHATTING WITH USER CODE:

def is_valid_file_name():
    '''None->str or None'''
    file_name = None
    try:
        file_name=input("Enter the name of the file: ").strip()
        f=open(file_name)
        f.close()
    except FileNotFoundError:
        print("There is no file with that name. Try again.")
        file_name=None
    return file_name

def get_file_name():
    '''()->str
    Keeps on asking for a file name that exists in the current folder,
    until it succeeds in getting a valid file name.
    Once it succeeds, it returns a string containing that file name'''
    file_name=None
    while file_name==None:
        file_name=is_valid_file_name()
    return file_name


def get_uid(network):
    '''(2Dlist)->int
    Keeps on asking for a user ID that exists in the network
    until it succeeds. Then it returns it'''

    try:
        uid = int(input("Enter a user ID that exists in the network"))
        for i in range(len(network)):
            if(uid == int(network[i][0])):
                return int(uid)
        print("That user does not exist in the network. Please try again")
        get_uid(network)
    except:
        get_uid(network)

##############################
# main
##############################

# NOTHING FOLLOWING THIS LINE CAN BE REMOVED or MODIFIED

file_name=get_file_name()

net=create_network(file_name)

print("\nFirst general statistics about the social network:\n")

print("This social network has", len(net), "people/users.")
print("In this social network the maximum number of friends that any one person has is "+str(maximum_num_friends(net))+".")
print("The average number of friends is "+str(average_num_friends(net))+".")
mf=people_with_most_friends(net)
print("There are", len(mf), "people with "+str(maximum_num_friends(net))+" friends and here are their IDs:", end=" ")
for item in mf:
    print(item, end=" ")

print("\n\nI now pick a number at random.", end=" ")
k=random.randint(0,len(net)//4)
print("\nThat number is: "+str(k)+". Let's see how many people has that many friends.")
print("There is", k_or_more_friends(net,k), "people with", k, "or more friends")

if knows_everyone(net):
    print("\nThere at least one person that knows everyone.")
else:
    print("\nThere is nobody that knows everyone.")

print("\nWe are now ready to recommend a friend for a user you specify.")
uid=get_uid(net)
rec=recommend(uid, net)
if rec==None:
    print("We have nobody to recommend for user with ID", uid, "since he/she is dominating in their connected component")
else:
    print("For user with ID", uid,"we recommend the user with ID",rec)
    print("That is because users", uid, "and",rec, "have", len(getCommonFriends(uid,rec,net)), "common friends and")
    print("user", uid, "does not have more common friends with anyone else.")


print("\nFinally, you showed interest in knowing common friends of some pairs of users.")
print("About 1st user ...")
uid1=get_uid(net)
print("About 2st user ...")
uid2=get_uid(net)
print("Here is the list of common friends of", uid1, "and", uid2)
common=getCommonFriends(uid1,uid2,net)
for item in common:
    print(item, end=" ")
