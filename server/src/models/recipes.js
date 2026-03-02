const mongoose = require("mongoose");
const RecipeSchema = require("../schemas/recipes");

const Recipe = mongoose.model("Recipe", RecipeSchema);

module.exports = Recipe;
