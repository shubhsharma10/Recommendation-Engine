from math import sqrt
import pandas as pd

class recommender:

	def __init__(self):
		self.training_data = {}
		self.test_data = {}


	def load_dataset(self):
		df = pd.read_csv("https://static.turi.com/datasets/movie_ratings/training_data.csv")
		users = {}

		for index,row in df.iterrows():
			key = row["user"]
			movie = row["movie"]
			rating = row["rating"]
			movie_entry = {movie:rating}
			if key in users:
				users[key][movie] = rating
			else:
				users[key] = movie_entry;

		count = 0
		length = len(users)

		for key,value in users.iteritems():
			count += 1
			if(count <= length*0.7):
				self.training_data[key] = value
			else:
				self.test_data[key] = value

		return self.test_data

	def add_to_training_data(self,key,value):
		self.training_data[key] = value

	# Returns a eucledian distance-based similarity score for person1 and person2
	def sim_distance(self,person1,person2):
		si={}
		for item in self.training_data[person1]:
			if item in self.training_data[person2]:
				si[item]=1
		if len(si)==0: 
			return 0
		sum_of_squares=sum([pow(self.training_data[person1][item]-self.training_data[person2][item],2)
							for item in self.training_data[person1] if item in self.training_data[person2]])
		return 1/(1+sum_of_squares)


	# Returns the Pearson correlation coefficient between person1 and person2
	def sim_pearson(self,person1,person2):
		si={}
		for item in self.training_data[p1]:
			if item in self.training_data[p2]: 
				si[item]=1
		n=len(si)

		
		if n==0: 
			return 0

		# Add preferences
		sum1=sum([self.training_data[p1][it] for it in si])
		sum2=sum([self.training_data[p2][it] for it in si])

		# Sum of the squares
		sum1Sq=sum([pow(self.training_data[p1][it],2) for it in si])
		sum2Sq=sum([pow(self.training_data[p2][it],2) for it in si])

		# Sum of products
		pSum=sum([self.training_data[p1][it]*self.training_data[p2][it] for it in si])

		# Calculate Pearson score
		num=pSum-(sum1*sum2/n)

		den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))

		if den==0: 
			return 0
		r=num/den
		return r


	def getRecommendations(self,person,simM = 0):
		totals={}
		simSums={}

		for other in self.training_data:
		# don't compare me to myself
			if other==person: 
				continue

			if simM == 0:
				sim = self.sim_pearson(person,other)
			else:
				sim=self.sim_distance(person,other)
			if sim<=0: continue
			for item in self.training_data[other]:
				if item not in self.training_data[person] or self.training_data[person][item]==0:
					# Similarity * Score
					totals.setdefault(item,0)
					totals[item]+=self.training_data[other][item]*sim
					# Sum of similarities
					simSums.setdefault(item,0)
					simSums[item]+=sim

		
		rankings=[(total/simSums[item],item) for item,total in totals.items( )]
		rankings.sort( ).reverse()
		return rankings


def main():
	recom = recommender();
	validation_data = recom.load_dataset();
	index = int(raw_input("enter index"))
	while(index >= 0):
		user1 = validation_data.keys()[index]
		value1 = validation_data[user1]
		movie_name = value1.keys()[0]
		exp_rating = value1[movie_name]
		value1.pop(movie_name)
		recom.add_to_training_data(user1,value1)
		pearson_recom = recom.getRecommendations(user1)
		eucledian_recom =  recom.getRecommendations(user1,simM = 1)

		print "User name is: "+str(user1)+" movie name is: "+str(movie_name)

		for i in range(len(pearson_recom)):
			if(pearson_recom[i][1] == movie_name):
				print "rating given by Pearson distance is: "+str(pearson_recom[i][0])
				break;

		for i in range(len(eucledian_recom)):
			if eucledian_recom[i][1] == movie_name :
				print "rating given by Eucledian distance is: "+str(eucledian_recom[i][0])
				break;

		print "Expected rating is: "+str(exp_rating)
		index = int(raw_input("enter index"))

if __name__ == '__main__':
	main()
