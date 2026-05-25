import { useState } from "react";
import type { Route } from "./+types/home";
import { Form, Link } from "react-router";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "View All Jobs" },
    { name: "description", content: "View all Jobs" },
  ];
}

export async function loader() {
  const response = await fetch(`http://scraper:5000/jobs`);
  const data = await response.json();
  return data;
}

export async function action({ request }: Route.ComponentProps) {
  const formData = await request.formData();
  const jobId = formData.get("jobId");
  await fetch(`http://scraper:5000/jobs/${jobId}/retry`);
}

export default function RecipeList({ loaderData }: Route.ComponentProps) {
  const [renderImported, setRenderImported] = useState(false);
  const handleChange = () => {
    setRenderImported(!renderImported);
  };

  // TODO(map) Add a state where there would be a "Mark Done" or something to be able to hide recipes you don't actually want to get. Maybe even a soft delete
  return (
    <div>
      <label>
        <input
          type="checkbox"
          checked={renderImported}
          onChange={handleChange}
        />
        Render Imported
      </label>
      {loaderData?.jobs && renderImported && (
        <ul>
          {loaderData?.jobs?.map(
            (job: Record<string, string>, index: number) => (
              <li key={index}>
                <Link to={`/recipes/import?jobId=${job.id}`}>
                  {job.name ? job.name : job.url} - {job.id} - {job.status}
                </Link>{" "}
                {job.status == "error" && (
                  <Form method="post">
                    <input type="hidden" name="jobId" value={job.id} />
                    <button type="submit">Retry</button>
                  </Form>
                )}
              </li>
            ),
          )}
        </ul>
      )}
      {loaderData?.jobs && !renderImported && (
        <ul>
          {loaderData?.jobs?.map(
            (job: Record<string, string>, index: number) =>
              job.status != "imported" && (
                <li key={index}>
                  <Link to={`/recipes/import?jobId=${job.id}`}>
                    {job.name ? job.name : job.url} - {job.id} - {job.status}
                  </Link>{" "}
                  {job.status == "error" && (
                    <Form method="post">
                      <input type="hidden" name="jobId" value={job.id} />
                      <button type="submit">Retry</button>
                    </Form>
                  )}
                </li>
              ),
          )}
        </ul>
      )}
    </div>
  );
}
