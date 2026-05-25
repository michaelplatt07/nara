import mongoose from "mongoose";
import { JobSchema } from "../schemas/jobs.js";

export const Job = mongoose.model("Job", JobSchema);
