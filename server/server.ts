import express, { Request, Response } from "express";
import axios from "axios";
import mongoose from "mongoose";
import { RecipeInput } from "./src/models/recipes";
import { RecipeQueryValidator } from "./src/validators/recipeSearch";
import * as RecipesController from "./src/controllers/recipes";
import { validateQuery } from "./middleware";

const app = express();
const port = 3000;
const SCRAPER_URL = "http://scraper:5000";

app.use(express.json());

/*
 * List of TODO Tasks:
 * Create a routes directory and different routes to import
 * Create services directory and move writing to DB to that layer
 * Create orchestrator directory and start using that for all calls to validate data, derive fields, call save, etc.
 * Set up Enums on fields that need it so we can ensure uniformity in the data
 * Implement endpoints for searching for recipes by various means, name, tags, etc
 * Build mapper for ingredient amount full name to abbreviation, C -> Cup(s) and Cup(s) -> C
 * Think about additional models needed
 */

app.get("/recipes", async (req: Request, res: Response) => {
  const recipes = await RecipesController.getAllRecipes();
  res.send(recipes);
});

app.get(
  "/recipes/search",
  validateQuery(RecipeQueryValidator),
  async (req: Request, res: Response) => {
    const recipes = await RecipesController.searchRecipes(req.validated);
    res.status(201).send(recipes);
  },
);

app.post(
  "/recipe/create",
  async (req: Request<{}, {}, RecipeInput>, res: Response) => {
    const createdRecipe = await RecipesController.createRecipe(req.body);
    res.status(201).send(createdRecipe);
  },
);

app.post("/recipe/import", async (req: Request, res: Response) => {
  // TODO(map) Set the search friendly name which should just be underscores with no special characters
  const recipe_url = req.query.recipe_url;
  if (recipe_url == null) {
    res.status(500).send("recipe_url is required");
  }
  try {
    const response = await axios.get(
      SCRAPER_URL + "/scrape?recipe_url=" + recipe_url,
    );
    console.log("Got response: " + response.data);
    const createdRecipe = await RecipesController.createRecipe(response.data);
    res.status(201).send(createdRecipe);
  } catch (error) {
    res.status(500).send("Error calling Scraper API: \n" + error);
  }
});

app.listen(port, () => {
  mongoose.connect("mongodb://db:27017/dev");
  console.log(`Server running at http://localhost:${port}`);
});
