# Description
The project is a recommendation system of text posts based on data about users, 
publications and interactions between them.

# Run the Code
1. You need to copy the repository to yourself locally:
```
git clone https://github.com/Donskoy-Andrey/Post_RecSys.git
```

2. Create an image of the Docker container:
```
docker build . -t TAG
```
where TAG is its name.

3. Create a Docker container:
```
docker run -p 8899:8899 TAG
```
where TAG is the name from the previous step. 

4. After the time allotted to start the service (to load the initial databases), it will become available.
You can check the operation at the local address, which starts with:
```
http://127.0.0.1:8899/
```
or
```
http://localhost:8899/
```
5. For example, query 2 (limit) recommendations for user 2021 (id) 
at time 2020-11-11 (time) looks like this
```
http://127.0.0.1:8899/post/recommendations/?id=2021&time=2020-11-11%2010:35:54&limit=2
```
or
```
http://localhost:8899/post/recommendations/?id=2021&time=2020-11-11%2010:35:54&limit=2
```
\
![Service Example](https://github.com/Donskoy-Andrey/Post_RecSys/blob/master/images/example.gif)

# The Stages of Development
The ROC - AUC on the target "did the user like the post" - was chosen as the post evaluation metric for the recommendation.

The project includes two blocks: application of machine learning methods to process raw data and build models (Stack: sklearn, catboost, nltk, pandas, numpy, etc.), and creation of a service for interaction with models within AB-testing (Stack: FastAPI, pydantic, hashlib, etc.).

>**STEP 1.** Creating a database of ready-to-use features for users and posts was done in Jupyter Notebook and included:
1. Loading initial databases with SQL queries.
2. Primary processing of the post data.
3. Selecting textual information from posts (TF-IDF) and clustering them based on these features.
3. Primary data processing about users.
4. Categorical information coding - Feature Target Encoding.
5. Saving pre-processed datasets via SQL for loading them into a service model.
6. Generating a complete dataset of > million lines based on publications, users, and interactions between them.
7. Model training, selecting the best parameters using parameter grid search.
8. Saving models into files for uploading to the service.

>**STEP 2.** Implemented a model interaction service that includes the following aspects:
1. Loading and creating the features of a particular user.
2. Defining it in one of two groups for AB - testing (choosing between 2 models).
3. Concatenation of data about the user and all publications (content approach to recommendations).
4. Predicting the metric (the probability of liking a particular post).
5. Sorting by metrics and selecting the necessary number of the best.
6. Output of the result.
