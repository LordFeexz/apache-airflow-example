import { BadRequestException } from "@nestjs/common";
import * as yup from "yup";

export const VALIDATION_ERROR = "VALIDATION_ERROR";

export abstract class BaseValidation {
  protected async validate<T = any>(schema: yup.Schema, data: any): Promise<T> {
    try {
      return (await schema.validate(data, {
        stripUnknown: true,
        abortEarly: false,
      })) as T;
    } catch (err) {
      const errorDetails: Record<string, string[]> = {};

      if (err?.inner && err?.inner.length > 0)
        err.inner.forEach((error: yup.ValidationError) => {
          if (!errorDetails[error.path]) {
            errorDetails[error.path] = [];
          }
          errorDetails[error.path].push(error.message);
        });

      errorDetails[VALIDATION_ERROR] = [VALIDATION_ERROR];

      throw new BadRequestException(errorDetails);
    }
  }
}
