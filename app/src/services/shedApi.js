import { ApiClient } from './genericApi'

class ShedClient extends ApiClient {
  constructor() {
    super("/sheds");
  }

  async clone(shedId) {
    try {
      const response = await this.api.post(`${this.path}/clone/${shedId}`);
      return response.data;
    } catch (error) {
      return error.response;
    }
  }
}

export { ShedClient };
