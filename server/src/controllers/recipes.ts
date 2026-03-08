import { RecipeQuery } from "../validators/recipeSearch";
import { Recipe, RecipeInput } from "../models/recipes";

export async function getAllRecipes() {
  return await Recipe.find();
}

export async function createRecipe(recipeInput: RecipeInput) {
  let recipe = new Recipe({
    ...recipeInput,
    search_name: recipeInput.name.replace(/\s+/g, "_").toLowerCase(),
  });
  return await recipe.save();
}

function buildQuery(queryParams: RecipeQuery) {
  if (queryParams.name) {
    // TODO(map) Make this a bit more flexible to be used. Incomplete names should be searchable still.
    return { search_name: queryParams.name.replace(/\s+/g, "_").toLowerCase() };
  }
  return {};
}

export async function searchRecipes(queryParams: RecipeQuery) {
  const query = buildQuery(queryParams);
  return await Recipe.find(query).exec();
}
