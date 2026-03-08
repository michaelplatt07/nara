import { Request, Response, NextFunction } from "express";

export function validateQuery(schema: any) {
  return (req: Request, res: Response, next: NextFunction) => {
    const result = schema.safeParse(req.query);

    if (!result.success) {
      return res.status(400).json(result.error);
    }

    req.validated = result.data;
    next();
  };
}
