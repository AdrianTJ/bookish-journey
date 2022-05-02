/* create a new external table 
 uris gives an array of fully qualified URIs for the external data locations
With format json*/

CREATE EXTERNAL TABLE IF NOT EXISTS `{{ params.project_id }}.cocktails_dataset.cocktail_dag`
OPTIONS (
    uris = ['gs://{{ params.bucket }}/cocktails/*/ingredients.json'],
    format = 'NEWLINE_DELIMITED_JSON'
);

-- A view is a virtual table based on the result-set of an SQL statement, selecting the variables to use
CREATE OR REPLACE VIEW `{{ params.project_id }}.cocktails_dataset.imgredients_dag`
AS SELECT
    idDrink,
    strDrink,
    strIngredient1,
    strIngredient2,
    strIngredient3,
    strIngredient4,
    strIngredient5,
    strIngredient6,
    strIngredient7,
    strIngredient8,
    strIngredient9,
    strIngredient10,
    strIngredient11,
    strIngredient12,
    strIngredient13,
    strIngredient14,
    strIngredient15
FROM `{{ params.project_id }}.cocktails_dataset.cocktails-table`
;
