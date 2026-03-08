import mongoose from "mongoose";
import { RecipeSchema } from "../schemas/recipes.js";

export const Recipe = mongoose.model("Recipe", RecipeSchema);

export interface RecipeInput {
  name: String;
  description: String;
  ingredients: [
    {
      name: String;
      quantity: mongoose.Schema.Types.Mixed;
      unit: mongoose.Schema.Types.Mixed;
    },
  ];
  instructions: [{ stepNumber: Number; instruction: String }];
  tags: [{ tagName: String }];
}
