def construct_lists(weights, pref):
    list_of_lists = []
    for voter in xrange(weights):
        list_of_lists.append(pref)
    return list_of_lists

def get_user_weights_and_prefs():
    prefs = []

    sentinel = False
    while sentinel is not True:
        weight = input("\nEnter a weight ")
        pref = list(input("Enter a preference order (separate with commas, no spaces). 1 represents a, 2 b, and so on. "))
        print weight, pref

        for voter in construct_lists(weight, pref):
            prefs.append(voter)
        print prefs
        
        cont = input("\nMore entries? Enter 1 for yes or 0 for no. ")
        if cont is 1:
            pass
        elif cont is 0:
            sentinel = True

def menu():
    print "Enter \n1 for user entered weights and preferences, \n2 for random weights and preferences,"
    print "3 for same voter preference between two candidates, and\n4 for something else"
    choice = input()
    if choice is 1:
       prefs = get_user_weights_and_prefs()
    if choice is 2:
        pass 
    if choice is 3:
        print "3"
    if choice is 4:
        print "f"

def bucklin(prefs):
    #start with k=1 (first choice row) and increase k gradually until some candidate is among the top k candidates
    #in more than half the votes; that candidate wins
    final_ordering = []
    num_candidates = len(prefs[0])
    needed_for_majority = len(prefs)/2 + 1
    majority_found = False 

    k = 0#since it's an index
    votes = [0 for x in xrange(1, num_candidates+1) ]
    while majority_found is False:
        for pref in prefs:
            votes[pref[k]-1] += 1 
        print "votes", votes
        for vote in votes:
            if vote > needed_for_majority:
                majority_found = True
        k += 1
        
        
    
def borda(prefs):
    vote_totals = {}
    #count votes for each candidate
    for pref in prefs:
	print "###################################cycling preferences", pref
	num_candidates = len(pref)
    	#define a dictionary of votes for each candidate - happens only on first key
	if len(vote_totals.keys()) is 0:
	    for candidate in xrange(1, num_candidates+1):#example of a pref  [3,1,2]
		vote_totals[candidate] = 0
	for index, candidate in enumerate(pref):
	    print "###############cycling candidates", candidate
	    print candidate, vote_totals[candidate], "+=", num_candidates-index
	    vote_totals[candidate] += (num_candidates - index)#number of voters with this preference times position
	    print candidate, vote_totals[candidate]
    print vote_totals

#    vote_totals = {}
#    #count votes for each candidate
#    for key in prefs:
#	print "###################################cycling preferences", key
#	num_candidates = len(prefs[key])
#    	#define a dictionary of votes for each candidate - happens only on first key
#	if len(vote_totals.keys()) is 0:
#	    for candidate in xrange(1, num_candidates+1):#example of prefs[key]   1:[3,1,2]
#		vote_totals[candidate] = 0
#	for index, candidate in enumerate(prefs[key]):
#	    print "###############cycling candidates", candidate
#	    print candidate, vote_totals[candidate], "+=",  key, "*", num_candidates-index
#	    vote_totals[candidate] += key*(num_candidates - index)#number of voters with this preference times position
#	    print candidate, vote_totals[candidate]
#    print vote_totals
			
def instant_runoff(prefs):
    #candidate with lowest plurality score (number of preferences where it's first place) drops out,
    #and repeat until one candidate is left
    final_ordering = []
    num_candidates = len(prefs[0])

    while len(prefs[0]) > 1:
        #find candidate with lowest priority score, and remove it from all preferences
        pluralities = [0 for x in xrange(1, num_candidates+1) ]
        #find plurality scores
        for pref in prefs:
            print "asdf", pref[0]
            pluralities[pref[0]-1] += 1
        print pluralities
        #find the lowest plurality score
        dead_candidate = -1#no tie handling here
        lowest_plur = 1000
        for index, plur in enumerate(pluralities):
            if plur < lowest_plur and plur is not 0:
                lowest_plur = plur
                dead_candidate = index + 1 #since there's no 0 candidate (1 represents a).
        print dead_candidate
        final_ordering.insert(0, dead_candidate)
        #elimitate it from preferences
        for pref in prefs:
            pref.remove(dead_candidate)
            print pref
    final_ordering.insert(0, prefs[0][0])	
    print prefs
    print final_ordering
    
    
#votes are for a,b, and c, represented as 1,2, and 3
#input
#voter_prefs = [[2,3,1], [2,3,1], [1,2,3], [1,2,3], [1,2,3], [1,2,3], [3,1,2]]
voter_prefs = [[2,3,1], [2,3,1], [1,2,3], [1,2,3], [1,2,3], [1,2,3], [3,1,2], [3,2,1], [3,2,1]]
#voter_prefs = [[2,3,1], [2,3,1], [1,2,3], [1,2,3], [1,2,3], [1,2,3], [3,1,2], [3,2,1], [3,2,1], [1,2,3]]
voter_prefs = menu()
print voter_prefs
#borda(voter_prefs)
#instant_runoff(voter_prefs)
#bucklin(voter_prefs)
