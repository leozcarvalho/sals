import { ApiClient } from './genericApi'

class SVGClient extends ApiClient {
  constructor() {
    super("/svgs");
  }

  async get(id, replaceVariables=false) {
    try {
      const response = await this.api.get(`${this.path}/${id}?replace_variables=${replaceVariables}`);
      return response.data;
    } catch (error) {
      return error.response;
    }
  }

  async options(id) {
    try {
      const response = await this.api.get(`${this.path}/${id}/options`);
      return response.data;
    } catch (error) {
      return error.response;
    }
  }

  async variables(id) {
    try {
      const response = await this.api.get(`${this.path}/${id}/variables`);
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
