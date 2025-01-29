import { Body, Controller, HttpCode, Post } from "@nestjs/common";
import { Body as IBody, DataValidationPipe } from "./pipes/data.pipe";
import { AppService } from "./app.service";

@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}

  @Post("send")
  @HttpCode(200)
  public async sendData(@Body(DataValidationPipe) { datas }: IBody) {
    this.appService.sendData(datas); // let this process async

    return {
      code: 200,
      message: "ok",
      data: null,
    };
  }
}
