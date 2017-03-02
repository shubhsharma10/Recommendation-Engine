import graphlab

data = graphlab.SFrame.read_csv("https://static.turi.com/datasets/movie_ratings/training_data.csv", column_type_hints={"rating":int})
#print data.head()
data_train,data_test = data.random_split(.8,seed=5)
model1 = graphlab.recommender.create(data_train, user_id="user", item_id="movie", target="rating")
#results = model.recommend(users=None, k=5)
#print results.head(20)

model2 = graphlab.popularity_recommender.create(data_train, user_id="user",
									item_id="movie",target="rating")
#results2 = model2.recommend(users=None, k=5)
#print results2.head(20)

model_performance = graphlab.compare(data_test,[model1,model2])
graphlab.show_comparison(model_performance,[model1,model2])