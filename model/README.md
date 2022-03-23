# Team 1. Bookish Journey: Cocktail Recommendation System

:cocktail: :tropical_drink: :wine_glass: :tumbler_glass: :bubble_tea: :cup_with_straw:

## 1. Data

We get the data from **TheCocktailDB** (https://www.thecocktaildb.com/), an open crowd-sourced database of drinks and cocktails from around the world. 

The dataset contains:

- *635* international drinks and cocktails recipes, 

- *296* unique ingredients, and

-  *635* drink images.

    
## 2. Feature engineering

Data Preparation: This preprocessing step involves the manipulation and consolidation of raw data from different sources into a standardized format so that it can be used in a model:

For this process we had to:

- [x] Drop empty columns, there is no cocktail with more than 12 ingredients.

- [x] Selecting Specific Columns in Google BigQuery 

- [x] Change all ingredients to lowercase letters.

- [x] Standarize the name of ingredients

- [x] Pass ingredientes into one hot encoding format. 


We had to change the format of the data frames from this:

|idDrink                          | strIngredient1                 | strIngredient2  | strIngredient3|...|
|:------------------------------:|:-----------------------:|:------:|:--------------:|:--------------:|
| 11001                    | Vodka       | Light rum         | Gin       |...|
| 11002                    | Light rum   | Lime	             | Sugar     |...|
| 11003                    | Bourbon     | Angostura bitters | Sugar     |...|
| 11004                    | Negroni     | Gin	             | Campari   |...|

	 
To this:

|idDrink                          | Vodka                 | Lime  | Bourbon |...|
|:------------------------------:|:-----------------------:|:------:|:--------------:|:--------------:|
| 11001                    | 1      | 0         | 0       |...|
| 11002                    | 0      | 1         | 0       |...|
| 11003                    | 0      | 0         | 1       |...|
| 11004                    | 0      | 0	        | 0       |...|



We had to do this because, many machine learning algorithms cannot operate on label data directly. They require all input variables and output variables to be numeric.

One hot encoding is a process of converting categorical data variables so they can be provided to machine learning algorithms to improve predictions.


**One-hot encoded vector of Ingredients**


To find similarities between cocktails and their ingredients, we will represent a recipe by a one-hot encoded vector of its ingredients. We will be establishing a vocabulary of ingredients using a method ‘DictVectorizer’ provided in the sklearn library.We use [How Dishes are Clustered together based on the Ingredients?](https://medium.com/web-mining-is688-spring-2021/how-dishes-are-clustered-together-based-on-the-ingredients-3b357ac02b26) to guide our code.


> DictVectorizer transforms lists of feature-value mappings to vectors. This transformer turns lists of mappings (dict-like objects) of feature names to feature values into Numpy arrays for use with scikit-learn estimators.
When feature values are strings, this transformer will do a binary one-hot (aka one-of-K) coding: one boolean-valued feature is constructed for each of the possible string values that the feature can take on.


```
#function to convert list of ingredients into a dictionary
def convert_to_dict(lst):
    d = {} #empty dict
    for ingre in lst:
        d[ingre] = 1
    return d
```






```
#We use the function to convert every row into a dictionary. 
#'vodka': 1, 'lime juice': 1... this will help us later to create a one hot encoding.

base['bagofwords'] = base.ingredients.str.split(',').apply(convert_to_dict)
print(base.bagofwords)
```


```
#DictVectorizer:  turns lists of mappings (dict-like objects) of feature names to feature values.C
#sparse, default=True. Whether transform should produce scipy.sparse matrices. In this case we set it as False.

vector_dict = DictVectorizer(sparse = False)

#fit_transform() is used on the training data so that we can scale the training data and also learn the scaling parameters of that data. 
#The fit method is calculating the mean and variance of each of the features present in our data. 
#The transform method is transforming all the features using the respective mean and variance.
#We past every dictionary into a list.

X = vector_dict.fit_transform(base["bagofwords"].tolist())

#We select the column strDrink(name of the drink) from de dataset
y = base.strDrink
```
## 3. Algorithm 

## KPCA Method

Kernel Principal Component Analysis (KPCA) is a non-linear dimensionality reduction technique. It is an extension of Principal Component Analysis (PCA)   *which is a linear dimensionality reduction technique* using kernel methods.

PCA is a technique for reducing the number of dimensions in a dataset whilst retaining most information. It is using the correlation between some dimensions and tries to provide a minimum number of variables that keeps the maximum amount of variation or information about how the original data is distributed

<img src="../image/ClusterPlot.png">

We are starting with somethig that is not a ML model at all, [cosine similarity](https://en.wikipedia.org/wiki/Cosine_similarity). This is in our opinion the easiest to implement, and can give us a good idea of some basic recommendations. 

<img src="../image/CosineSimilarity.png">

### K-means

We want to build a more robust ML system that will be based on clustering. We want to start with [k-means clustering](https://en.wikipedia.org/wiki/K-means_clustering), and grow to other clustering algorithms from there. This is where the meat of the machine learning computation will take place. Something interesting to note is that we have discrete classes and k-means clustering works **only on real vectors**, so we have to solve the problem of generating real vectors from a list of categorical variables. This will be done by using [principal component analysis (PCA)](https://en.wikipedia.org/wiki/Principal_component_analysis) as an in-between step from having the raw ingredients to generating an n-dimensional proximation to a point from that list. 

The K-means algorithm clusters data by trying to separate samples in n groups of equal variance, minimizing a criterion known as the inertia or within-cluster sum-of-squares. This algorithm requires the number of clusters to be specified. It scales well to large number of samples and has been used across a large range of application areas in many different fields.

<img src="../image/KmeansPlt.png">


   

    
## 4. Experiments
    
## 5. ML metrics


We have decided that we are doing model evaluation for each of our two ML models, and then after combining these with the cosine distance and generating our final meta-model, we are also doing some more subjective evaluation based not on metrics but on human input.

For the ML model evaluation, we really have two different models. For clustering, we are sticking to silhouette curves and the elbow method. We note that both of these metrics are heuristic, which makes sense because we are working with an unsupervised learning problem. While there are other metrics to evaluate the efficiency and predictive power of the clusters we define, we are sticking with these two because we have worked with them in the past and we have a good understanding of how to interpret them.

As for market basket analysis, there is the trifecta of metrics that seems to be the go-to evaluation method: support, confidence and lift, with lift being the primary metric we are interested in.

    
## 6. Trade-offs


## References

- https://plotly.com/python/pca-visualization/

- https://programminghistorian.org/en/lessons/clustering-with-scikit-learn-in-python

- https://medium.com/web-mining-is688-spring-2021/how-dishes-are-clustered-together-based-on-the-ingredients-3b357ac02b26

- https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html

- https://www.askpython.com/python/examples/plot-k-means-clusters-python

- https://numpy.org/doc/stable/reference/generated/numpy.argpartition.html
