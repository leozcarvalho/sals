import { ApiClient } from './genericApi'

class BatchClient extends ApiClient {
  constructor() {
    super("/batches"); // chama o construtor da classe pai
  }

  async execMoviment(batchId, movimentData) {
    try {
      const response = await this.api.post(`${this.path}/${batchId}/moviment`, movimentData);
      return response.data;
    } catch (error) {
      return error.response;
    }
  }
}

export { BatchClient };
