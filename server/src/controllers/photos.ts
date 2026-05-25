import { finished } from "stream/promises";
import { getBucket } from "../../db";
import mongoose from "mongoose";

export async function getPhotoById(photoId: string) {
  const bucket = getBucket();
  const files = await bucket
    .find({
      _id: new mongoose.Types.ObjectId(photoId),
    })
    .toArray();
  return files[0] || null;
}

export async function uploadFile(uploadFile) {
  const bucket = getBucket();

  const uploadStream = bucket.openUploadStream(uploadFile.originalname, {
    contentType: uploadFile.mimetype,
  });

  uploadStream.end(uploadFile.buffer);

  await finished(uploadStream);

  return { fileId: uploadStream.id };
}
