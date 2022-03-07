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
FROM `bookish-journey.cocktail.cocktails-table`
WHERE strIngredient1 = "Vodka" OR strIngredient2 = "Vodka" OR strIngredient3 = "Vodka" OR strIngredient4 = "Vodka" OR strIngredient5 = "Vodka"