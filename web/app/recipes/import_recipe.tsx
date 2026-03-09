import type { Route } from "./+types/home";
import { Form } from "react-router";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Import Recipe" },
    { name: "description", content: "Import Recipe" },
  ];
}

export async function loader({ request }: Route.ComponentProps) {
  const url = new URL(request.url);
  const query = url.searchParams.get("recipeUrl");

  // Don't fetch if no query param yet
  if (!query) return { error: "No recipe to import" };

  // const response = await fetch(
  //   `http://localhost:8000/recipes/search?query=${query}`,
  // );
  // const recipes = await response.json();
  return { importedRecipe: { title: "Sample Imported Recipe" } };
}

export default function ImportRecipe({ loaderData }: Route.ComponentProps) {
  const { importedRecipe } = loaderData;
  return (
    <div>
      <div>
        <Form method="GET">
          <input type="text" name="recipeUrl" />
          <button type="submit">Import</button>
        </Form>
      </div>
      {importedRecipe && (
        <div>
          <p>"Title": {importedRecipe.title}</p>
        </div>
      )}
    </div>
  );
}
