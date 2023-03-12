create TABLE ingredients(
IngredientID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
NameIngredient TINYTEXT NOT NULL,
EnergyValue INT,
Calory INT,
Weight FLOAT,
Producer TINYTEXT);

create TABLE recipe(
RecipeID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
NameRecipe TINYTEXT,
CookingTime INT,
TotalWeight INT,
Rating ENUM('1', '2', '3', '4', '5') DEFAULT '1',
Amount INT,
CHECK(Amount > 2));

create TABLE users(
UserID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
FirstName TINYTEXT NOT NULL,
LastName TINYTEXT NOT NULL,
Age INT NOT NULL,
Experience INT NOT NULL,
FavoriteCuisine TINYTEXT,
FavoriteRecipe INT,
FOREIGN KEY (FavoriteRecipe) REFERENCES recipe(RecipeID));

create TABLE recipe_ingredient(
Recipe INT NOT NULL,
Ingredient INT NOT NULL,
CONSTRAINT recipe_igredient PRIMARY KEY (Recipe, Ingredient),
FOREIGN KEY (Recipe) REFERENCES recipe(RecipeID),
FOREIGN KEY (Ingredient) REFERENCES ingredients(IngredientID));
