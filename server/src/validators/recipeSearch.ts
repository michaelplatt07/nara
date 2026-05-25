import { z } from "zod";

export const RecipeQueryValidator = z.object({
  // name: z.string().optional(),
  // tags: z.preprocess(
  //   (val) => (Array.isArray(val) ? val : val ? [val] : undefined),
  //   z.array(z.string()).optional(),
  // ),
  // ingredients: z.preprocess(
  //   (val) => (Array.isArray(val) ? val : val ? [val] : undefined),
  //   z.array(z.string()).optional(),
  // ),
  terms: z.preprocess(
    (val) => (Array.isArray(val) ? val : val ? [val] : undefined),
    z.array(z.string()).optional(),
  ),
});
export type RecipeQuery = z.infer<typeof RecipeQueryValidator>;
