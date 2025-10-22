import { ApiClient } from './genericApi'

class DevicePinsClient extends ApiClient {
  constructor() {
    super("/device-pins");
  }

  async togglePin(id) {
    try {
      const response = await this.api.patch(`${this.path}/${id}/toggle`);
      return response.data;
    } catch (error) {
      return error.response;
    }
  }
}

export { DevicePinsClient };
