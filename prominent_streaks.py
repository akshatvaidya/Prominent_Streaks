#Author - Akshat Vaidya
import pandas as pd
import time


#####Jump to line number 202 where the actual code execution starts#######

def readfiles():    
    #read from the csv file and return a Pandas DataFrame.
    nba = pd.read_csv("1991-2004-nba.dat",  delimiter='#')
        
    #Pandas DataFrame allows you to select columns. 
    #We use column selection to split the data. 
    #We only need 2 columns in the data file: Player ID and Points.
    columns = ['ID', 'PTS']
    nba_records = nba[columns]
    
    #For each player, store the player's points in all games in an ordered list.
    #Store all players' sequences in a dictionary.
    pts = {}    
    cur_player = 'NULL'
    #The data file is already sorted by player IDs, followed by dates.
    for index, row in nba_records.iterrows():
        player, points = row
        if player != cur_player:
            cur_player = player
            pts[player] = []            
        pts[player].append(points)

    return pts


####Compare method compares two streaks and returns 0 if streak1 dominates streak2
####Returns 1 if streak2 dominates streak1
def compare(streak1, streak2):
	#Lengths of the streaks are calculated by subtracting the left index from the right index
	length1 = streak1[2] - streak1[1] + 1
	length2 = streak2[2] - streak2[1] + 1
	value1 = streak1[3]
	value2 = streak2[3]
	#Dominance checks
	if ((length1 > length2 and value1 >= value2) or (length1 >= length2 and value1 > value2)):
		return 0
	elif ((length1 < length2 and value1 <= value2) or (length1 <= length2 and value1 < value2)):
		return 1
	else:
		return -1


def prominent_streaks(sequences):
	#This list stores all the local prominent streaks of all the players
	local_prominent_streaks = []
	for player,scores in sequences.items():
		#This list stores the potential growing streaks of each player and is initialized again for 
		#each player again
		potential_lps = []			
		i = 0
		for score in scores:
			#If its the first iteration then directly add the first score as a potential streak
			if i == 0:
				ps = [player,i,i,score]
				potential_lps.append(ps)
				i+=1
			else:
			#There can be three cases after the first iteration
				case1 = 1
				case2 = 1
				case3 = 1
				#If the minimum values of all the potential growing streaks are not less than the
				#next value then it is not the case1 for sure
				for lps in potential_lps:
					if lps[3] >= score:
						case1 = 0
						break
				#If its case1 then the following code executes
				if case1 == 1:
					#Extending the streak
					for lps in potential_lps:
						lps[2] = i
					#Creating a new streak at the position of the next value
					new_ps = [player,i,i,score]
					potential_lps.append(new_ps)
					i+=1
				else:
					#If the minimum values of all the potential growing streaks are not greater than
					#next value and since it is not case1 it is not case2 for sure too
					for lps in potential_lps:
						if lps[3] <= score:
							case2 = 0
							break
					#If its case2 then the following code executes
					if case2 == 1:
						#This variable keeps track of the longest streak whose minimum value is greater
						#than the next value
						leftmost_lps = potential_lps[0]
						#This list keeps track of all the streaks to be removed from the list of
						#potential streaks
						lps_to_remove = []
						for lps in potential_lps:
							#Streaks having minimum value higher than next value are directly stored
							#as local prominent streaks
							new_ps = [lps[0], lps[1], lps[2], lps[3]]
							local_prominent_streaks.append(new_ps)
							if lps[1] < leftmost_lps[1]:
								leftmost_lps = lps
						for lps in potential_lps:
							if lps != leftmost_lps:
								#If the streak is not the longest streak then it is stored in the to be
								#removed list
								lps_to_remove.append(lps)
							else:
								#If it is the longest such streak then it is extended and the minimum
								#value is updated
								lps[2] = i
								lps[3] = score
						#All the streaks to be removed are removed from the list of potential streaks
						for lps in lps_to_remove:
							potential_lps.remove(lps)
						i+=1
					else:
						#If it is not case1 and case2 then the following code executes which is nothing
						#but the combination of case1 and case2
						#Streaks having minimum values higher than the next value are stored seperately
						upper_lps = []
						lps_to_remove = []
						#Streaks having minimum values less than the next value are simply extended
						for lps in potential_lps:
							if lps[3] <= score:
								lps[2] = i
							else:
								#If the streak has minimum value higher than the next value then it is
								#stores seperately
								upper_lps.append(lps)
						#If no streak had value higher than the next value then it is the end of the 
						#iteration
						if upper_lps == []:
							i+=1
						else:
							#Same as case2 where we keep track of the longest streak and extend only that
							leftmost_lps = upper_lps[0]
							for lps in upper_lps:
								new_ps = [lps[0], lps[1], lps[2], lps[3]]
								local_prominent_streaks.append(new_ps)
								if lps[1] < leftmost_lps[1]:
									leftmost_lps = lps
							for lps in upper_lps:
								if lps != leftmost_lps:
									lps_to_remove.append(lps)
								else:
									lps[2] = i
									lps[3] = score
							for lps in lps_to_remove:
								potential_lps.remove(lps)
							i+=1
		
		lps_to_remove = []
		#After all the iterations all the remaining streaks in the list of potential streaks
		#are moved to local prominent streaks
		for lps in potential_lps:
			new_ps = [lps[0], lps[1], lps[2], lps[3]]
			local_prominent_streaks.append(new_ps)
			lps_to_remove.append(lps)

		#After moving them to local prominent streaks they are removed from the list of the potential
		#streaks just for cleanup purposes
		for lps in lps_to_remove:
			potential_lps.remove(lps)

	#A new list is created after generating all the candidate streaks
	#This new list is for the skyline points among those candidate points
	#Skyline algorithm is same as that of the one explained by professor
	PS = []
	n = len(local_prominent_streaks)
	for i in range(n): #0 - 100
		dominated = 0
		streaks_to_remove = []
		l = len(PS)
		for j in range(l): # 0
			result = compare(local_prominent_streaks[i],PS[j])
			if result == 1:
				dominated = 1
				break
			if result == 0:
				streaks_to_remove.append(PS[j])
		if dominated == 0:
			PS.append(local_prominent_streaks[i])
		for streak in streaks_to_remove:
			PS.remove(streak)
	
	#Since all the streaks were stored as lists at first, they are converted to tuple format
	#for better reading of output
	final = []
	for lps in PS:
		length = lps[2] - lps[1] + 1
		t = lps[0], lps[1], length, lps[3]
		final.append(t)

	return final


t0 = time.time()
sequences = readfiles()
t1 = time.time()
print("Reading the data file takes ", t1-t0, " seconds.")
#print(sequences)

t1 = time.time()
streaks = prominent_streaks(sequences)
t2 = time.time()
print("Computing prominent streaks takes ", t2-t1, " seconds.")
print(streaks)
