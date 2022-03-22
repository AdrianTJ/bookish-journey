# Team 1. Bookish Journey: Cocktail Recipes Made By Machibe Learning

:cocktail: :tropical_drink: :wine_glass: :tumbler_glass: :bubble_tea: :cup_with_straw:

## 1. Data

We get the data from **TheCocktailDB** (https://www.thecocktaildb.com/), an open crowd-sourced database of drinks and cocktails from around the world. 

The dataset contains:

- *635* international drinks and cocktails recipes, 

- *296* unique ingredients, and

-  *635* drink images.

    
## 2. Feature engineering

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

To achive this we had to do the follow

- [x] Drop empty columns, there is no cocktail with more than 12 ingredients.

- [x] Change all ingredients to lowercase letters.

- [x] Select unique ingredients.

- [x] Make one hot encoding using ingredientes as columns.

### **What is the Problem with Categorical Data?**

Many machine learning algorithms cannot operate on label data directly. They require all input variables and output variables to be numeric.

One hot encoding is a process of converting categorical data variables so they can be provided to machine learning algorithms to improve predictions.


## 3. Algorithm
    
## 4. Experiments
    
 ## 5. ML metrics
    
 ## 6. Trade-offs


## References

- https://plotly.com/python/pca-visualization/

- https://programminghistorian.org/en/lessons/clustering-with-scikit-learn-in-python

- https://medium.com/web-mining-is688-spring-2021/how-dishes-are-clustered-together-based-on-the-ingredients-3b357ac02b26

- https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html

- https://www.askpython.com/python/examples/plot-k-means-clusters-python

- https://numpy.org/doc/stable/reference/generated/numpy.argpartition.html
