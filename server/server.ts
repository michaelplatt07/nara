import express, { Request, Response } from "express";
import axios from "axios";
import { RecipeInput } from "./src/models/recipes";
import { RecipeQueryValidator } from "./src/validators/recipeSearch";
import * as RecipesController from "./src/controllers/recipes";
import * as JobsController from "./src/controllers/jobs";
import * as PhotoController from "./src/controllers/photos";
import { validateQuery } from "./middleware";
import { connectDb, getBucket } from "./db";
import multer from "multer";

const app = express();
const port = 3000;
const SCRAPER_URL = "http://scraper:5000";

app.use(express.json());

// Basic multer set up that loads the file into memory. This will need to change to be better in the future to do a
// multipart upload to not destroy memory but is fine for now
const upload = multer(); // memory storage

app.get("/recipes", async (req: Request, res: Response) => {
  const recipes = await RecipesController.getAllRecipes();
  res.send({ recipes: recipes });
});

app.get("/recipes/:recipeId/details", async (req: Request, res: Response) => {
  const recipeId = req.params.recipeId;
  const recipe = await RecipesController.getRecipeDetails(recipeId);
  res.send(recipe);
});

app.get(
  "/recipes/search",
  validateQuery(RecipeQueryValidator),
  async (req: Request, res: Response) => {
    const recipes = await RecipesController.searchRecipes(req.validated);
    res.status(201).send({ recipes: recipes });
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

app.post("/jobs/complete", async (req: Request, res: Response) => {
  const body = req.body;
  const job = await JobsController.markJobImported(body.jobId);
  res.send({ job: job });
});

app.get("/photos/:photoId", async (req: Request, res: Response) => {
  const photo = await PhotoController.getPhotoById(req.params.photoId);
  if (photo != null) {
    res.send({ photo: photo });
  } else {
    res.status(404).send("Couldn't find file with given ID");
  }
});

app.post(
  "/recipes/:recipeId/photos",
  upload.single("file"),
  async (req: Request, res: Response) => {
    try {
      const fileUploadRes = await PhotoController.uploadFile(req.file);

      RecipesController.updateRecipe(req.params.recipeId, {
        photoId: fileUploadRes.fileId,
      });
      res.send({ fileId: fileUploadRes.fileId });
    } catch (err: any) {
      res.status(404).send({ err: err });
    }
  },
);

async function start() {
  await connectDb();

  app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
  });
}

start();
