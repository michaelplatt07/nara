import type { Route } from "./+types/home";
import { Form, redirect, useRevalidator } from "react-router";
import { useEffect } from "react";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Import Recipe" },
    { name: "description", content: "Import Recipe" },
  ];
}

export async function loader({ request }: Route.ComponentProps) {
  const url = new URL(request.url);
  const jobId = url.searchParams.get("jobId");

  // Don't fetch if no query param yet
  if (!jobId) return { status: "idle" };

  const response = await fetch(`http://scraper:5000/jobs/${jobId}/status`);
  const data = await response.json();
  return data;
}

export async function action({ request }: Route.ComponentProps) {
  const data = await request.formData("recipeUrl");
  const recipeUrl = data.get("recipeUrl");

  // Don't fetch if no query param yet
  if (!recipeUrl) return { error: "No recipe to import" };

  const response = await fetch(
    `http://scraper:5000/scrape?recipe_url=${recipeUrl}`,
  );
  const { job_id } = await response.json();
  return redirect(`/recipes/import?jobId=${job_id}`);
}

export default function ImportRecipe({ loaderData }: Route.ComponentProps) {
  const revalidator = useRevalidator();

  useEffect(() => {
    if (loaderData?.status === "pending") {
      const interval = setInterval(() => {
        if (revalidator.state == "idle") {
          revalidator.revalidate();
        }
      }, 3000);
      return () => clearInterval(interval); // stop polling when status changes
    }
  }, [loaderData?.status, revalidator.state]);

  return (
    <div>
      {loaderData?.status == "idle" && (
        <div>
          <Form method="POST">
            <input type="text" name="recipeUrl" />
            <button type="submit">Import</button>
          </Form>
        </div>
      )}
      {loaderData?.status == "pending" && <p>"Importing recipe..."</p>}
      {loaderData?.status == "error" && <p>"Error importing recipe"</p>}
      {loaderData?.status == "success" && (
        <div>
          <p>Successfully imported recipe</p>
          <p>{loaderData?.recipe?.name}</p>
          <ul>
            {loaderData?.recipe?.ingredients?.map(
              (ingredient: Record<string, string>, index: number) => (
                <li key={index}>
                  {ingredient.quantity} - {ingredient.unit} {ingredient.name}
                </li>
              ),
            )}
          </ul>
          <ul>
            {loaderData?.recipe?.instructions?.map(
              (instruction: Record<string, string>, index: number) => (
                <li key={index}>
                  {instruction.stepNumber} - {instruction.instruction}
                </li>
              ),
            )}
          </ul>
        </div>
      )}
    </div>
  );
}
