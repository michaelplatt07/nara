import type { Route } from "./+types/home";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Create Recipe" },
    { name: "description", content: "Create Recipe" },
  ];
}

export default function CreateRecipe({}: Route.ComponentProps) {
  return (
    <div>
      <form method="POST"></form>
    </div>
  );
}

export async function action({ request }) {
  const data = await request.formData();
  // Make call to the DB
}
