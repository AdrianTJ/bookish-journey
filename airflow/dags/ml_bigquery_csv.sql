/*
Creates a temporary table. Is visible only within the current session
Then select the variables
Export in qualified URI for the external data location as csv
*/
BEGIN
    CREATE TEMP TABLE _SESSION.tmpExportTable AS (
        SELECT
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
        FROM `###############`
    );
    EXPORT DATA OPTIONS(
        uri='###############'
        , format='CSV'
        , overwrite=true
        , header=true
        , field_delimiter=","
    ) AS
    SELECT * FROM _SESSION.tmpExportTable;
END;