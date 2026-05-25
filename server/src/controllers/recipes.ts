import { RecipeQuery } from "../validators/recipeSearch";
import mongoose from "mongoose";
import { Recipe, RecipeInput } from "../models/recipes";

export async function getAllRecipes() {
  return await Recipe.find();
}

export async function getRecipeDetails(recipeId: string) {
  return await Recipe.findById(recipeId);
}

export async function updateRecipe(recipeId: string, data: any) {
  return await Recipe.findOneAndUpdate(
    { _id: new mongoose.Types.ObjectId(recipeId) },
    data,
  );
}

export async function createRecipe(recipeInput: RecipeInput) {
  let recipe = new Recipe({
    ...recipeInput,
    search_name: recipeInput.name.replace(/\s+/g, "_").toLowerCase(),
    created_at: Date.now(),
  });
  return await recipe.save();
}

function buildQuery(queryParams: RecipeQuery) {
  // if (queryParams.name) {
  //   // TODO(map) Make this a bit more flexible to be used. Incomplete names should be searchable still.
  //   return { search_name: queryParams.name.replace(/\s+/g, "_").toLowerCase() };
  // }
  const tagNameSearch = queryParams.terms.map((term) => ({
    "tags.tagName": { $regex: term, $options: "i" },
  }));
  const recipeNameSearch = queryParams.terms.map((term) => ({
    name: { $regex: term, $options: "i" },
  }));
  return {
    $or: [...tagNameSearch, ...recipeNameSearch],
  };
}

export async function searchRecipes(queryParams: RecipeQuery) {
  const query = buildQuery(queryParams);
  return await Recipe.find(query).exec();
}
