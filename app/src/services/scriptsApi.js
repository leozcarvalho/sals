import { ApiClient } from './genericApi'

class ScriptsClient extends ApiClient {
  constructor() {
    super("/scripts"); // chama o construtor da classe pai
  }

  async execScript(scriptName, data) {
    const payload = {
      script_name: scriptName,
      params: data,
    };
    console.log(payload);
    try {
      const response = await this.api.post(`${this.path}/script-1`, payload);
      return response.data;
    } catch (error) {
      return error.response;
    }
  }
}

export { ScriptsClient };
