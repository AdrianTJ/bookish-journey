# General Imports
from sklearn.feature_extraction import DictVectorizer
from sklearn.decomposition import KernelPCA
from sklearn.cluster import KMeans
import itertools
import numpy as np
import pandas as pd
import pathlib
import yaml
import string
import requests

# Import for model saving in bucket
import joblib
from google.cloud import storage
import datetime

# Recall from the APIs for Data lab that including passwords in code is a terrible $
# So we include a yaml file.
config_file = open('/home/airflow/dags/GCP_model_details.yaml', 'r')
config = yaml.safe_load(config_file)

# load the model from disk
loaded_model = joblib.load('/home/airflow/dags/meanshift_model.joblib')

# load data from disk 
loaded_data = pd.read_csv("/home/airflow/dags/000000000000.csv")

# Drop empty columns
base = loaded_data.drop(['strIngredient12','strIngredient13','strIngredient14','strIngredient15'],axis=1)

# Replace NaN with ""
base = base.replace(np.nan,"")

# Create a ner variable, ingredients, that has all the previous ingredients together. 
base['ingredients'] = base[['strIngredient1','strIngredient2','strIngredient3','strIngredient4','strIngredient5',
        'strIngredient6','strIngredient7','strIngredient8','strIngredient9','strIngredient10','strIngredient11']].agg(','.join, axis=1)

# Function to transform letters to lowercase.
def lower(text):
    text=text.lower()
    return text

# Pass all words throw the funtion and append them
ingredients_low=[]
for i in base.ingredients:
    il=lower(i)
    ingredients_low.append(il)

# Lowercase
base['ingredients']=ingredients_low

# This function convert a list of ingredients into a dictionary, note: every ingredient gets a 1.
# this mean that the value of every key is 1. key:value
def convert_to_dict(lst):
    d = {} #empty dict
    for ingre in lst:
        d[ingre] = 1
    return d

# We use the function to convert every row into a dictionary. 
# 'vodka': 1, 'lime juice': 1... this will help us later to create a one hot encoding.
base['bagofwords'] = base.ingredients.str.split(',').apply(convert_to_dict)

# One Hot Encoding
# To find similarities between dishes and cluster cocktails using their ingredients, we will represent a recipe by a one-hot encoded vector 
# of its ingredients. We will be establishing a vocabulary of ingredients using a method ‘DictVectorizer’ provided in the sklearn library

# DictVectorizer:This transformer turns lists of mappings (dict-like objects) of feature names to feature values into Numpy arrays or scipy.sparse matrices for use with scikit-learn estimators.
# sparse, default=True. Whether transform should produce scipy.sparse matrices. In this case we set it as False.

vector_dict = DictVectorizer(sparse = False)

# fit_transform() is used on the training data so that we can scale the training data and also learn the scaling parameters of that data. 
#The fit method is calculating the mean and variance of each of the features present in our data. 
#The transform method is transforming all the features using the respective mean and variance.
# We past every dictionary into a list.
X = vector_dict.fit_transform(base["bagofwords"].tolist())

# We select the column strDrink(name of the drink) from de dataset
y = base.strDrink

# Using Kernel PCA
# kernel = "cosine": This is called cosine similarity, because Euclidean (L2) normalization projects the vectors onto the unit sphere, and their dot product is then the cosine of the angle between the points denoted by the vectors.

kpca = KernelPCA(n_components=2,kernel="cosine", n_jobs=2)

# Using the transform method we can use the same mean and variance as it is calculated from our training data to transform our test data. 
#Thus, the parameters learned by our model using the training data will help us to transform our test data.
x_pca = kpca.fit_transform(X)

# Recommendations
def cluster_recomm(index,algorithm = loaded_model,n_return = 5):
    cluster = algorithm.predict(x_pca[index].reshape(1, -1))[0]
    cluster_map = pd.DataFrame()
    cluster_map['cluster'] = algorithm.labels_
    in_cluster = cluster_map[cluster_map.cluster == cluster].sample(n=n_return)
    return y[in_cluster.index]

recomm_list = []
for i in range(len(X)): 
    recomm_list.append(list(cluster_recomm(index = i, algorithm = loaded_model, n_return = 5)))

recomms = pd.concat([pd.Series(x) for x in recomm_list], axis=1)
recomms = recomms.T

recomms.to_csv("/home/airflow/dags/meanshift_results.csv", index = False)


# Bucket holding the data
client = storage.Client.from_service_account_json(config['path_auth'])
gcs_bucket = client.get_bucket(config['bucket_name'])
path = f"MeanShift/" + "meanshift_results"
blob = gcs_bucket.blob(path)
blob.upload_from_filename("/home/airflow/dags/meanshift_results.csv")
