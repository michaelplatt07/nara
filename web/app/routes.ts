import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
  index("routes/home.tsx"),
  route("/recipes", "./recipes/recipes_list.tsx"),
  route("/recipes/create", "./recipes/create_recipe.tsx"),
  route("/recipes/import", "./recipes/import_recipe.tsx"),
  route("/recipes/finalize", "./recipes/finalize.tsx"),
  route("/recipes/search", "./recipes/search_recipe.tsx"),
  route("/recipes/:recipeId/details", "./recipes/single_recipe.tsx"),
  route("/jobs", "./jobs/jobs_list.tsx"),
] satisfies RouteConfig;
