import type { Route } from "./+types/home";
import { useFieldArray, useForm } from "react-hook-form";
import { redirect, useRevalidator, useSubmit } from "react-router";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Create Recipe" },
    { name: "description", content: "Create Recipe" },
  ];
}

export async function action({ request }: Route.ComponentProps) {
  const formData = await request.formData();
  const recipe = JSON.parse(formData.get("recipe") as string);

  const response = await fetch(`http://server:3000/recipe/create`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(recipe),
  });
  const { _id } = await response.json();
  return redirect(`/recipes/${_id}/details`);
}

export default function ImportRecipe({ loaderData }: Route.ComponentProps) {
  const revalidator = useRevalidator();

  const submit = useSubmit();

  const { register, control, getValues, reset, handleSubmit } = useForm({
    defaultValues: {
      name: "",
      ingredients: [],
      instructions: [],
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

  const handleFinalize = (data: any) => {
    submit(
      { recipe: JSON.stringify(data) },
      { method: "POST", action: "/recipes/create" },
    );
  };

  return (
    <div>
      <div>
        <form onSubmit={handleSubmit(handleFinalize)}>
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
                  <button type="button" onClick={() => removeIngredient(index)}>
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
      </div>
    </div>
  );
}
