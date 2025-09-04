import { useApi } from "./useApi";

class ApiClient {
  constructor(path) {
    this.path = path;
    this.api = useApi();
  }

  async getList(filter = {}) {
    try {
      const response = await this.api.get(this.path, {
        params: {
          ...filter,
        },
      });
      return response.data;
    } catch (error) {
      return error.response;
    }
  }

  async get(id) {
    try {
      const response = await this.api.get(`${this.path}/${id}`);
      return response.data;
    } catch (error) {
      return error.response;
    }
  }

  async save(data) {
    try {
      const response = await this.api.post(this.path, data);
      return response.data;
    } catch (error) {
      return error.response;
    }
  }

  async update(id, data) {
    try {
      const response = await this.api.put(`${this.path}/${id}`, data);
      return response.data;
    } catch (error) {
      return error.response;
    }
  }

  async delete(id) {
    try {
      const response = await this.api.delete(`${this.path}/${id}`);
      return response.data;
    } catch (error) {
      return error.response;
    }
  }

  async downloadFile(fileUrl, fileName) {
    const link = document.createElement('a');
    link.href = fileUrl;
    link.download = fileName;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }

  async deleteFile(fileId) {
    try {
      const response = await this.api.delete(`/s3/${fileId}`);
      return response;
    } catch (error) {
      return error.response;
    }
  }
}

export { ApiClient };