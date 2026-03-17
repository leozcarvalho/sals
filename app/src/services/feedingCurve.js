import { ApiClient } from './genericApi'

class FeedingCurveClient extends ApiClient {
  constructor() {
    super("/feeding-curves");
  }

  async clone(feedingCurveId) {
    try {
      const response = await this.api.post(`${this.path}/clone/${feedingCurveId}`);
      return response.data;
    } catch (error) {
      return error.response;
    }
  }
}

export { FeedingCurveClient };
