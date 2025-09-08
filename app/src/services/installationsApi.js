import { ApiClient } from './genericApi'

class InstallationClient extends ApiClient {
  constructor() {
    super("/installations"); // chama o construtor da classe pai
  }

  async healthCheck(id) {
    try {
      const response = await this.api.post(`${this.path}/${id}/health-check`);
      return response.data;
    } catch (error) {
      return error.response;
    }
  }

  async restart(id) {
    try {
      const response = await this.api.post(`${this.path}/${id}/restart`);
      return response.data;
    } catch (error) {
      return error.response;
    }
  }

  async togglePin(id, pinNumber) {
    try {
      const response = await this.api.post(`${this.path}/${id}/toggle-pin/${pinNumber}`);
      return response.data;
    } catch (error) {
      return error.response;
    }
  }
}

export { InstallationClient };
