import { ApiClient } from './genericApi'

class SVGClient extends ApiClient {
  constructor() {
    super("/svgs");
  }

  async options(id) {
    try {
      const response = await this.api.get(`${this.path}/${id}/options`);
      return response.data;
    } catch (error) {
      return error.response;
    }
  }

  async getOwnerSvgId(ownerType, ownerId) {
    try {
      const response = await this.api.get(`${this.path}/owner/${ownerType}/${ownerId}`);
      return response.data;
    } catch (error) {
      return error.response;
    }
  }
}

export { SVGClient };
