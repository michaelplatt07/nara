const express = require("express");
const app = express();
const port = 3000;

const Recipe = require("./src/models/recipes");
const mongoose = require("mongoose");

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

app.get("/recipes", async (req, res) => {
  const recipes = await Recipe.find();
  res.send(recipes);
});

app.post("/recipe/create", async (req, res) => {
  // TODO(map) Set the search friendly name which should just be underscores with no special characters
  const recipe = new Recipe(req.body);
  await recipe.save();
  res.status(201).send("Recipe created");
});

app.listen(port, () => {
  mongoose.connect("mongodb://db:27017/dev");
  console.log(`Server running at http://localhost:${port}`);
});
