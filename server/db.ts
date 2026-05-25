import mongoose from "mongoose";
import { GridFSBucket } from "mongodb";

let bucket;

export async function connectDb() {
  await mongoose.connect("mongodb://db:27017/dev");

  bucket = new GridFSBucket(mongoose.connection.db, {
    bucketName: "recipePhotos",
  });
}

export function getBucket() {
  if (!bucket) {
    throw new Error("No bucket");
  }
  return bucket;
}
