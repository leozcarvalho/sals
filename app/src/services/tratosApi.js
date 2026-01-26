import { ApiClient } from './genericApi'

class TratosClient extends ApiClient {
  constructor() {
    super("/tratos"); // chama o construtor da classe pai
  }

  async bulkUpdate(data) {
    try {
      const response = await this.api.put(`${this.path}/bulk-update`, data);
      return response.data;
    } catch (error) {
      return error.response;
    }
  }
}

export { TratosClient };
