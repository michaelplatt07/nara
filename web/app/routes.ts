import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
  index("routes/home.tsx"),
  route("/recipes", "./recipes/recipes_list.tsx"),
  route("/recipes/import", "./recipes/import_recipe.tsx"),
  route("/recipes/view/:recipeId", "./recipes/single_recipe.tsx"),
  route("/jobs", "./jobs/jobs_list.tsx"),
] satisfies RouteConfig;
