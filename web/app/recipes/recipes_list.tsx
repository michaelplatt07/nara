import type { Route } from "./+types/home";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "View All Recipes" },
    { name: "description", content: "View all recipes" },
  ];
}

export default function RecipeList() {
  return (
      <div>
          <p>All The Recipes</p>
      </div>
  );
}
