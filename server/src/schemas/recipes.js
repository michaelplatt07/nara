const mongoose = require("mongoose");

const Recipe = new mongoose.Schema({
  // TODO(map) Make the appropriate fields required
  name: String,
  description: String,
  ingredients: [{ name: String, quantity: Number, unit: String }],
  instructions: [{ stepNumber: Number, instruction: String }],
  tags: [{ tagName: String }],
});

module.exports = Recipe;
