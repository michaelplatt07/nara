import { Link } from "react-router";
import type { Route } from "./+types/home";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Search Recipes" },
    { name: "description", content: "Search all recipes" },
  ];
}

export async function loader({ request }: Route.ComponentProps) {
  const url = new URL(request.url);
  const term = url.searchParams.get("term");
  const response = await fetch(
    // TODO(map) This should be just a term and the BE should handle building the regex query
    `http://server:3000/recipes/search?terms=bang`,
  );
  const data = await response.json();
  console.log(data);
  return data;
}

export default function RecipeList({ loaderData }: Route.ComponentProps) {
  const recipes = loaderData?.recipes ?? [];

  return (
    <div>
      <p>Search Results:</p>
      <div className="grid grid-cols-4 gap-4">
        {recipes.map((recipe, _) => (
          <div key={recipe._id} className="bg-[#4a6741] min-h-40">
            <Link to={`/recipes/${recipe._id}/details`}>{recipe.name}</Link>
          </div>
        ))}
      </div>
    </div>
  );
}
