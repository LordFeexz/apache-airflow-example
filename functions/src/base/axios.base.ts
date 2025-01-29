import Axios, {
  type CreateAxiosDefaults,
  type AxiosInstance,
  type AxiosResponse,
} from "axios";

export interface Query {
  url: string;
  headers?: any;
  params?: any;
}

export interface Mutation {
  url: string;
  headers?: any;
  params?: any;
  method: "POST" | "PATCH" | "DELETE" | "PUT";
  data?: any;
}

export abstract class ThirdPartyRequest {
  private readonly client: AxiosInstance;
  constructor(baseURL: string, opts?: Omit<CreateAxiosDefaults, "baseURL">) {
    this.client = Axios.create({ ...opts, baseURL });
  }

  protected async Query<T = any>({
    url,
    headers,
    params,
  }: Query): Promise<AxiosResponse<T>> {
    const { signal } = new AbortController();
    return this.client<T>({
      url,
      headers,
      method: "GET",
      params,
      signal,
    });
  }

  protected async Mutation<T = any>({
    url,
    headers,
    data,
    method,
    params,
  }: Mutation): Promise<AxiosResponse<T>> {
    const { signal } = new AbortController();
    return this.client<T>({
      url,
      headers,
      method,
      data,
      params,
      signal,
    });
  }
}
