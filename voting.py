import random
def construct_lists(weights, pref):
    list_of_lists = []
    for voter in xrange(weights):
        list_of_lists.append(pref)
    return list_of_lists

def get_user_weights_and_prefs(random_flag=False, forced_choice=[]):
    #return [[2,3,1], [2,3,1], [1,2,3], [1,2,3], [1,2,3], [1,2,3], [3,1,2], [3,2,1], [3,2,1]]
    prefs = []

    num_candidates = random.randint(2, 8)
    if len(forced_choice) is 2:
	num_candidates = random.randint(max(forced_choice[0], forced_choice[1]), max(forced_choice[0], forced_choice[1])+5)
    if len(forced_choice) is 3:
	num_candidates = random.randint(max(forced_choice[0], forced_choice[1], forced_choice[2] ), max(forced_choice[0], forced_choice[1], forced_choice[2])+5)
    random_counter = 0
    random_limit = random.randint(2, 6)
    sentinel = False
    while sentinel is False:
	if random_flag:
	    weight = random.randint(1, 3)
	    pref = [x for x in xrange(1, num_candidates+1)]
	    random.shuffle(pref)
	else:
            weight = input("\nEnter a weight: ")
            pref = list(input("Enter a preference order (separate with commas, no spaces). 1 represents candidate a, 2 b, and so on: "))

        for voter in construct_lists(weight, pref):
            prefs.append(voter)
       	if random_flag is False: 
	    cont = input("\nMore entries? Enter 1 for yes or 0 for no. ")
	    if cont is 1:
		pass
	    elif cont is 0:
		sentinel = True
	else:
	    if random_counter < random_limit:
		pass
	    else:
		sentinel = True 
	random_counter += 1 
    if len(forced_choice) is 2:
	for pref in prefs:
	    better = forced_choice[0]
	    worse = forced_choice[1]
	    if pref.index(better) > pref.index(worse):
		temp = pref[pref.index(better)]
		pref[pref.index(better)] = pref[pref.index(worse)]
		pref[pref.index(worse)] = temp
    if len(forced_choice) is 3:
	for pref in prefs:
	    better = forced_choice[0]
	    middle = forced_choice[1]
	    worse = forced_choice[2]
	    if pref.index(better) > pref.index(worse):
		temp = pref[pref.index(better)]
		pref[pref.index(better)] = pref[pref.index(worse)]
		pref[pref.index(worse)] = temp
	    if pref.index(better) > pref.index(middle):
		temp = pref[pref.index(better)]
		pref[pref.index(better)] = pref[pref.index(middle)]
		pref[pref.index(middle)] = temp
	    if pref.index(middle) > pref.index(worse):
		temp = pref[pref.index(middle)]
		pref[pref.index(middle)] = pref[pref.index(worse)]
		pref[pref.index(worse)] = temp
    return prefs

def display_majority_graph(prefs):
    print "\n\n\n--------Majority Graph (1 stands for candidate a, 2 for b, and so on):\n"
    print len(prefs), "voter's preferences, left to right:"
    for pref in prefs:
	print pref
def print_results(bucklin, borda, instant):
    print "\n--------Results (preference from left to right):\n"
    print "Bucklin ordering:                  ", bucklin
    print "Borda ordering:                    ", borda
    print "Single Transferable Vote ordering: ", instant
    

def menu():
    print "Enter: \n1 for user-entered weights and preferences, \n2 for random weights and preferences,"
    print "3 for same voter preference between two candidates, and\n4 for same voter preference between three candidates"
    choice = input()
    if choice is 1:
        prefs = get_user_weights_and_prefs()
	display_majority_graph(prefs)
	bucklin_ordering = bucklin(prefs)
	borda_ordering = borda(prefs)
	instant_ordering = instant_runoff(prefs)	
	print_results(bucklin_ordering, borda_ordering, instant_ordering)
    if choice is 2:
        prefs = get_user_weights_and_prefs(True)
	display_majority_graph(prefs)
	bucklin_ordering = bucklin(prefs)
	borda_ordering = borda(prefs)
	instant_ordering = instant_runoff(prefs)	
	print_results(bucklin_ordering, borda_ordering, instant_ordering)
    if choice is 3:
	choice = input("Enter the two candidates, with the one that everyone prefers first, separated with a comma: ")
        prefs = get_user_weights_and_prefs(True, choice)
	display_majority_graph(prefs)
	bucklin_ordering = bucklin(prefs)
	borda_ordering = borda(prefs)
	instant_ordering = instant_runoff(prefs)	
	print_results(bucklin_ordering, borda_ordering, instant_ordering)
    if choice is 4:
	choice = input("Enter the three candidates, with the one that everyone prefers first, then the next, then the last, separated with commas: ")
        prefs = get_user_weights_and_prefs(True, choice)
	display_majority_graph(prefs)
	bucklin_ordering = bucklin(prefs)
	borda_ordering = borda(prefs)
	instant_ordering = instant_runoff(prefs)	
	print_results(bucklin_ordering, borda_ordering, instant_ordering)

def bucklin(prefs):
    #start with k=1 (first choice row) and increase k gradually until some candidate is among the top k candidates
    #in more than half the votes; that candidate wins
    num_candidates = len(prefs[0])
    needed_for_majority = len(prefs)/2 + 1
    majority_found = False 

    k = 0#since it's an index
    votes = [0 for x in xrange(1, num_candidates+1) ]
    while majority_found is False:
        for pref in prefs:
            votes[pref[k]-1] += 1 
        for vote in votes:
            if vote >= needed_for_majority:
                majority_found = True
        k += 1
    #now get an ordering based on how many votes for each candidate
    tuples = [(index, vote) for index, vote in enumerate(votes)] 
    tuples.sort(key=lambda x: x[1], reverse=True)#no tie resolution here
    final_ordering = [x[0]+1 for x in tuples]
    return final_ordering
	
        
        
    
def borda(prefs):
    vote_totals = {}
    #count votes for each candidate
    for pref in prefs:
	num_candidates = len(pref)
    	#define a dictionary of votes for each candidate - happens only on first key
	if len(vote_totals.keys()) is 0:
	    for candidate in xrange(1, num_candidates+1):#example of a pref  [3,1,2]
		vote_totals[candidate] = 0
	for index, candidate in enumerate(pref):
	    vote_totals[candidate] += (num_candidates - index)#number of voters with this preference times position
    ordering = sorted(vote_totals.items(), key=lambda x: x[1], reverse=True)
    ordering = [x[0] for x in ordering]
    return ordering

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
            pluralities[pref[0]-1] += 1
	
	fresh_kill = False	
	old_kills = []
	while fresh_kill is False:
	    #find the lowest plurality score
	    dead_candidate = -1#no tie handling here
	    lowest_plur = 1000
	    lowest_index = -1
	    for index, plur in enumerate(pluralities):
		if plur < lowest_plur and index+1 not in old_kills:
		    lowest_plur = plur
		    lowest_index = index
	    dead_candidate = lowest_index + 1 #since there's no 0 candidate (1 represents a).
	    if dead_candidate in prefs[0]:
		#found a candidate that hasn't been removed yet
		fresh_kill = True
	    else:
		old_kills.append(dead_candidate)
	
		

        final_ordering.insert(0, dead_candidate)
        #elimitate it from preferences
        for pref in prefs:
	    if dead_candidate in pref:
                pref.remove(dead_candidate)

    final_ordering.insert(0, prefs[0][0])	
    return final_ordering
    
    
#votes are for a,b, and c, represented as 1,2, and 3
#input
#voter_prefs = [[2,3,1], [2,3,1], [1,2,3], [1,2,3], [1,2,3], [1,2,3], [3,1,2]]
voter_prefs = [[2,3,1], [2,3,1], [1,2,3], [1,2,3], [1,2,3], [1,2,3], [3,1,2], [3,2,1], [3,2,1]]
#voter_prefs = [[2,3,1], [2,3,1], [1,2,3], [1,2,3], [1,2,3], [1,2,3], [3,1,2], [3,2,1], [3,2,1], [1,2,3]]
voter_prefs = menu()
