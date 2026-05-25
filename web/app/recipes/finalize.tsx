import type { Route } from "./+types/home";
import { Form, redirect, useRevalidator } from "react-router";
import { useEffect } from "react";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Finalize Recipe" },
    { name: "description", content: "Finalize Recipe" },
  ];
}

export async function loader({ request }: Route.ComponentProps) {
  return "";
}

export async function action({ request }: Route.ComponentProps) {
  const formData = await request.formData();
  console.log(formData);
  const recipe = JSON.parse(formData.get("recipe") as string);
  const jobId = formData.get("jobId");

  await fetch(`http://server:3000/jobs/complete`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ jobId: jobId }),
  });

  const response = await fetch(`http://server:3000/recipe/create`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(recipe),
  });

  const x = await response.json();
  console.log(x);
}

export default function FinalizeRecipe({ loaderData }: Route.ComponentProps) {
  return <div>Successfully submitted</div>;
}
