import random

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

class User:
    def __init__(self, name):
        self.name = name

class SocialGraph:
    def __init__(self):
        self.lastID = 0
        self.users = {}
        self.friendships = {}

    def addFriendship(self, userID, friendID):
        """
        Creates a bi-directional friendship
        """
        if userID == friendID:
            print("WARNING: You cannot be friends with yourself")
        elif friendID in self.friendships[userID] or userID in self.friendships[friendID]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[userID].add(friendID)
            self.friendships[friendID].add(userID)

    def addUser(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.lastID += 1  # automatically increment the ID to assign the new user
        self.users[self.lastID] = User(name)
        self.friendships[self.lastID] = set()

    def populateGraph(self, numUsers, avgFriendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.lastID = 0
        self.users = {}
        self.friendships = {}
        # !!!! IMPLEMENT ME

        if numUsers < avgFriendships:
            print("WARNING: The number of users must be greater than the average number of friendships.")
        else:
        # Add users
            for i in range(numUsers):
                self.addUser(f"User {i + 1}")
        # Create friendships - O(n^2) runtime
            # friendships = [(userID, friendID) for userID in self.users for friendID in range(userID+1, self.lastID+1)]
            # random.shuffle(friendships)
            # connections = numUsers * avgFriendships // 2
            # friendships = friendships[:connections]
            # for friend in friendships:
            #     self.addFriendship(friend[0], friend[1])

        # Stretch - Create friendships - O(n) runtime
            connections = numUsers * avgFriendships // 2   # O(1)

            for _ in range(connections):    # O(n)
                userID = random.randint(1, numUsers)   # O(1)
                friendID = random.randint(1, numUsers)   # O(1)

                # # Ensure not befriending self and to keep getting new random integer until not equal
                # while userID == friendID:
                #     friendID = random.randint(1, numUsers)   # O(1)

                # # Ensure not befriending an already connected friend
                # while friendID in self.friendships[userID]:   # O(n)
                #     friendID = random.randint(1, numUsers)   # O(1)

                self.addFriendship(userID, friendID)   # O(1)

    def getAllSocialPaths(self, userID):
        """
        Takes a user's userID as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {}  # Note that this is a dictionary, not a set
        # !!!! IMPLEMENT ME
        queue = Queue()
        queue.enqueue([userID])

        while queue.size() > 0:
            path = queue.dequeue()
            friendID = path[-1]

            if friendID not in visited:
                visited[friendID] = path

                for next_friendID in self.friendships[friendID]:
                    new_path = path + [next_friendID]
                    queue.enqueue(new_path)
        
        return visited


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populateGraph(1000, 5)
    print(sg.friendships)
    connections = sg.getAllSocialPaths(1)
    print(connections)

    sum = 0
    for i in connections:
        sum += len(connections[i])
    percent = (len(connections)/1000)*100
    print(f'{percent}%')
    degree = sum/len(connections)
    print(f'{degree}°')

"""
Q:  To create 100 users with an average of 10 friends each, how many times would you need to call addFriendship()? Why?
A:  500. => The function is ran for every item in an array from index 0 to the number of connection you want to make.
    The number of connections is determined by numUsers * avgFriendships // 2 ==> (100 * 10)//2 ==> 1000//2 ==> 500

Q:  If you create 1000 users with an average of 5 random friends each, what percentage of other users will be in a particular user's extended social network? 
    What is the average degree of separation between a user and those in his/her extended network?
A:  After running several times, the percentage comes out to average a little over 99% of other users being in the social network 
    with an average of about 5 degrees of seperation.


Stretch Goal
Q:  You might have found the results from question #2 above to be surprising. 
    Would you expect results like this in real life? 
    If not, what are some ways you could improve your friendship distribution model for more realistic results?
A:  I would not expect in real life for a user to be connected with 99% of all other users and by only 5 degrees.
    One way to improve this model is to possibly not do a full shuffle of all the possible friendships.
    That way some of the friends could be grouped together a little more realistically like real groups of friends.
    You could also maybe write a shuffle algorithm that is weighted to try to pick a certain number or two 
    more frequently than others to try to recreate a grouping of friends.

Q:  If you followed the hints for part 1, your populateGraph() will run in O(n^2) time. 
    Refactor your code to run in O(n) time. 
    Are there any tradeoffs that come with this implementation?
A:  Able to get it down to O(n) with a side effect that it can generate random invalid connections like trying to
    befriend yourself or a friend a user you are already connected with. Cannot avoid this case unless creating a sub
    function within the for loop which at worst would be O(n^2) but it reality would only run that second O(n) function
    a few times not every time.
"""