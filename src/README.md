## Database integration


This directory hosts the files used to create our data store. To do this, we implement an *ELT* process:

   **E**xtract - the input data for the machine learning model was extracted from **TheCocktailDB API** [https://www.thecocktaildb.com/api.php] using a virtual machine *(cocktail notebook)* on the **VERTEX AI platform**. The script can be found in the **Cocktails_Load.ipynb** file.
  
   **L**oad - The extracted information was uploaded to **Google Cloud Storage** with the following structure: 1 folder for each cocktail and a file in json format associated with that drink.
  
   **T**ransformation - **Google BigQuery** was used for data transformation. And it consisted of replacing the labels of 2 variables (*strInstructionsZH-HANS and strInstructionsZH-HANT) since the BigQuery format does not accept hyphens, so it was replaced with an underscore.

Finally, 2 types of queries are made to the table that hosts the extracted information *(cocktails-table)*. The first is to keep the variables of interest (cocktail ID, cocktail name and its ingredients), and the second query refers to cocktails in particular.
The files to perform the queries are *query_ingredients.sql* and *query_contains_vodka.sql*.
