import type { Route } from "./+types/home";
import { Link } from "react-router";

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

export default function RecipeList({ loaderData }: Route.ComponentProps) {
  return (
    <div>
      {!!loaderData?.jobs && <p>Fetching jobs...</p>}
      {loaderData?.jobs && (
        <ul>
          {loaderData?.jobs?.map(
            (job: Record<string, string>, index: number) => (
              <li key={index}>
                <Link to={`/recipes/import?jobId=${job.id}`}>
                  {job.id} - {job.status}
                </Link>
              </li>
            ),
          )}
        </ul>
      )}
    </div>
  );
}
