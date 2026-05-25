import mongoose from "mongoose";

export const RecipeSchema = new mongoose.Schema({
  name: String,
  search_name: String,
  description: String,
  url: String,
  photoId: mongoose.Schema.Types.ObjectId,
  created_at: Date,
  ingredients: [
    {
      name: String,
      quantity: mongoose.Schema.Types.Mixed,
      unit: mongoose.Schema.Types.Mixed,
      notes: mongoose.Schema.Types.Mixed,
    },
  ],
  instructions: [{ stepNumber: Number, instruction: String }],
  tags: [{ tagName: String }],
});
