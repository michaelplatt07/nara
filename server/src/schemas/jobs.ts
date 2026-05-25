import mongoose from "mongoose";

export const JobSchema = new mongoose.Schema({
  job_id: String,
  status: String,
  original_data: String,
  data: {
    name: String,
    url: String,
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
  },
});
