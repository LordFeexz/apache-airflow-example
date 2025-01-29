import {
  type ArgumentMetadata,
  Injectable,
  type PipeTransform,
} from "@nestjs/common";
import { BaseValidation } from "src/base/validation.base";
import * as yup from "yup";

export interface DataProps {
  name: string;
  age: number;
}

export interface Body {
  datas: DataProps[];
}

@Injectable()
export class DataValidationPipe
  extends BaseValidation
  implements PipeTransform<any, Promise<Body>>
{
  public async transform(value: any, _: ArgumentMetadata) {
    return await this.validate<Body>(
      yup.object().shape({
        datas: yup
          .array()
          .of(
            yup.object({
              name: yup
                .string()
                .typeError("[TYPE_ERROR]")
                .required("[REQUIRED]"),
              age: yup
                .number()
                .typeError("[TYPE_ERROR]")
                .required("[REQUIRED]"),
            })
          )
          .min(1, "[MIN:1]")
          .max(100, "[MAX:100]")
          .required("[REQUIRED]"),
      }),
      value
    );
  }
}
