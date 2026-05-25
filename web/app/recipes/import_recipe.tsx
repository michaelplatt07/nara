import type { Route } from "./+types/home";
import { useFieldArray, useForm } from "react-hook-form";
import {
  Form,
  redirect,
  useRevalidator,
  useSearchParams,
  useSubmit,
} from "react-router";
import { useEffect, useRef, useState } from "react";

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
  console.log("TODO(map) REMOVE ME : " + JSON.stringify(data));
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

  const [searchParams] = useSearchParams();
  const jobId = searchParams.get("jobId");
  const [showOriginal, setShowOriginal] = useState(false);
  const handleShowOriginalToggle = () => {
    setShowOriginal(!showOriginal);
  };

  const submit = useSubmit();

  const url = loaderData?.url;

  const { register, control, getValues, reset, handleSubmit } = useForm({
    defaultValues: {
      jobId: jobId,
      url: url,
      name: loaderData?.recipe?.name,
      ingredients: loaderData?.recipe?.ingredients ?? [],
      instructions: loaderData?.recipe?.instructions ?? [],
    },
  });

  const {
    fields: ingredientFields,
    append: appendIngredient,
    remove: removeIngredient,
  } = useFieldArray({ control, name: "ingredients" });

  const {
    fields: instructionFields,
    append: appendInstruction,
    remove: removeInstruction,
  } = useFieldArray({ control, name: "instructions" });

  const {
    fields: tagFields,
    append: appendTag,
    remove: removeTag,
  } = useFieldArray({ control, name: "tags" });

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

  const handleFinalize = (data: any) => {
    submit(
      {
        recipe: JSON.stringify({
          name: data.name,
          ingredients: data.ingredients,
          instructions: data.instructions,
          tags: data.tags,
          url: data.url,
        }),
        jobId: data.jobId,
      },
      { method: "POST", action: "/recipes/finalize" },
    );
  };

  const manualImport = (data: any) => {
    // TODO(map) This should take in the original recipe once its stored
    submit({}, { method: "GET", action: "/recipes/import/manual" });
  };

  const createRecipe = () => {
    submit({}, { method: "GET", action: "/recipes/create" });
  };

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
      {loaderData?.status == "error" && (
        <div>
          <p>"Error importing recipe"</p>
          <p>{loaderData?.message}</p>
          {loaderData?.original_data && (
            <form onSubmit={handleSubmit(manualImport)}>
              <button type="submit">Manual Import</button>
            </form>
          )}
          {loaderData?.original_data == null && (
            <form onSubmit={handleSubmit(createRecipe)}>
              <button type="submit">Create</button>
            </form>
          )}
        </div>
      )}
      {(loaderData?.status == "success" ||
        loaderData?.status == "imported") && (
        <div>
          <label>
            <input
              type="checkbox"
              checked={showOriginal}
              onChange={handleShowOriginalToggle}
            />
            Show Original Text
          </label>
          <p>Successfully imported recipe</p>
          <form onSubmit={handleSubmit(handleFinalize)}>
            <input type="hidden" {...register("url")} />
            <input type="hidden" {...register("jobId")} />
            <div>
              <p>
                Recipe Name: <input {...register("name")} />
              </p>
            </div>
            <div>
              <p>Ingredient List</p>
              <ul>
                {ingredientFields.map((field, index) => (
                  <li key={field.id}>
                    <input
                      {...register(`ingredients.${index}.quantity`)}
                      placeholder="Qty"
                    />
                    <input
                      {...register(`ingredients.${index}.unit`)}
                      placeholder="Unit"
                    />
                    <input
                      {...register(`ingredients.${index}.name`)}
                      placeholder="Name"
                    />
                    <input
                      {...register(`ingredients.${index}.notes`)}
                      placeholder="Notes"
                    />
                    <button
                      type="button"
                      onClick={() => removeIngredient(index)}
                    >
                      Remove
                    </button>
                  </li>
                ))}
              </ul>
              <button
                type="button"
                onClick={() =>
                  appendIngredient({
                    quantity: "",
                    unit: "",
                    name: "",
                    notes: "",
                  })
                }
              >
                + Add Ingredient
              </button>
            </div>
            <div>
              <p>Instructions</p>
              <ul>
                {instructionFields.map((field, index) => (
                  <li key={field.id}>
                    <input
                      {...register(`instructions.${index}.stepNumber`)}
                      placeholder="Step #"
                    />
                    <input
                      {...register(`instructions.${index}.instruction`)}
                      placeholder="Instruction"
                    />
                    <button
                      type="button"
                      onClick={() => removeInstruction(index)}
                    >
                      Remove
                    </button>
                  </li>
                ))}
              </ul>
              <button
                type="button"
                onClick={() =>
                  appendInstruction({
                    stepNumber: instructionFields.length + 1,
                    instruction: "",
                  })
                }
              >
                + Add Step
              </button>
            </div>
            <div>
              <p>Tags</p>
              <ul>
                {tagFields.map((field, index) => (
                  <li key={field.id}>
                    <input
                      {...register(`tags.${index}.tagName`)}
                      placeholder="Tag"
                    />
                    <button type="button" onClick={() => removeTag(index)}>
                      Remove
                    </button>
                  </li>
                ))}
              </ul>
              <button
                type="button"
                onClick={() =>
                  appendTag({
                    tagName: "",
                  })
                }
              >
                + Add Tag
              </button>
            </div>

            <button type="submit">Finalize</button>
          </form>
          {showOriginal && loaderData?.original_data && (
            <div>
              {loaderData?.original_data.split("\n").map((line, _) => (
                <p>
                  {line.replace(/\\u([\dA-F]{4})/gi, (_, hex) =>
                    String.fromCharCode(parseInt(hex, 16)),
                  )}
                </p>
              ))}
            </div>
          )}
          {showOriginal && !loaderData?.original_data && (
            <div>No original data to show.</div>
          )}
        </div>
      )}
    </div>
  );
}
