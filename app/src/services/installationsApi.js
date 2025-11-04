import { ApiClient } from './genericApi'

class InstallationClient extends ApiClient {
  constructor() {
    super("/installations");
  }

  async execAction(id, action, payload = {}) {
    try {
      const response = await this.api.post(`${this.path}/${id}/action/${action}`, payload);
      return response.data;
    } catch (error) {
      return error.response;
    }
  }

  async updateDevicePins(installationId, data) {
    try {
      const response = await this.api.put(`${this.path}/${installationId}/update-device-pins`, data);
      return response.data;
    } catch (error) {
      return error.response;
    }
  }
}

export { InstallationClient };
