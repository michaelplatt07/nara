import { Job } from "../models/jobs";

export async function markJobImported(jobId: string) {
  return await Job.findOneAndUpdate({ job_id: jobId }, { status: "imported" });
}
