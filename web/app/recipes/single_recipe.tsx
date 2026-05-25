import type { Route } from "./+types/home";

export async function loader({ params }: Route.ComponentProps) {
  const response = await fetch(
    `http://server:3000/recipes/${params.recipeId}/details`,
  );
  console.log(params);

  const data = await response.json();
  return data;
}

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Single Recipe" },
    { name: "description", content: "Single Recipe Name" },
  ];
}

export default function SingleRecipe({ loaderData }: Route.ComponentProps) {
  const { name, _, ingredients, instructions, tags } = loaderData;

  return (
    <div>
      <h3>{name}</h3>
      <h4>Ingredients</h4>
      <ul>
        {ingredients.map((ingredient, index) => (
          <li>
            {ingredient.quantity} {ingredient.unit} - {ingredient.name}{" "}
            {ingredient.notes}
          </li>
        ))}
      </ul>
      <h4>Instructions</h4>
      <ul>
        {instructions.map((instruction, index) => (
          <li>{instruction.instruction}</li>
        ))}
      </ul>
      <h4>Tags</h4>
      <ul>
        {tags.map((tag, index) => (
          <li>{tag.tagName}</li>
        ))}
      </ul>
    </div>
  );
}
