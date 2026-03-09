import type { Route } from "./+types/home";

export async function loader({ params }: Route.ComponentProps) {
  return { recipeId: params.recipeId, message: "Sample Message" };
}

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Single Recipe" },
    { name: "description", content: "Single Recipe Name" },
  ];
}

export default function SingleRecipe({ loaderData }: Route.ComponentProps) {
  return (
    <div>
      <p>{loaderData.recipeId}</p>
      <p>{loaderData.message}</p>
    </div>
  );
}
