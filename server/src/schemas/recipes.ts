import mongoose from "mongoose";

export const RecipeSchema = new mongoose.Schema({
  name: String,
  search_name: String,
  description: String,
  ingredients: [
    {
      name: String,
      quantity: mongoose.Schema.Types.Mixed,
      unit: mongoose.Schema.Types.Mixed,
    },
  ],
  instructions: [{ stepNumber: Number, instruction: String }],
  tags: [{ tagName: String }],
});

// TODO(map) Figure out typing on model but the above is doing mixed for now.
// const Recipe = new mongoose.Schema({
//   // TODO(map) Make the appropriate fields required
//   name: String,
//   description: String,
//   ingredients: [{ name: String, quantity: Number, unit: String }],
//   instructions: [{ stepNumber: Number, instruction: String }],
//   tags: [{ tagName: String }],
// });
