import { ApiClient } from './genericApi'

class ProfilesClient extends ApiClient {
  constructor() {
    super("/profiles"); // chama o construtor da classe pai
  }

  async getPermissions() {
    try {
      const response = await this.api.get(`${this.path}/permissions/all`);
      return response.data;
    } catch (error) {
      return error.response;
    }
  }
}

export { ProfilesClient };
