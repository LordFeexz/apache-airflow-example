import { Injectable } from "@nestjs/common";
import { ThirdPartyRequest } from "src/base/axios.base";
import { DataProps } from "./pipes/data.pipe";

@Injectable()
export class AppService extends ThirdPartyRequest {
  constructor() {
    super("http://localhost:6000", {
      validateStatus: () => true,
    });
  }

  public async sendData(datas: DataProps[]) {
    return this.Mutation({
      url: "/trigger",
      method: "POST",
      data: { datas },
    });
  }
}
