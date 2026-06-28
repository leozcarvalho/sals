import { ApiClient } from './genericApi'

class ReceitasClient extends ApiClient {
  constructor() {
    super("/receitas")
  }

  async gerar(data_base, considerar_fracao_liquida = false) {
    try {
      const response = await this.api.post(`${this.path}/gerar`, null, {
        params: { data_base, considerar_fracao_liquida }
      })
      return response.data
    } catch (error) {
      return error.response
    }
  }

  async getProduzir(receita_id) {
    try {
      const response = await this.api.get(`${this.path}/${receita_id}/produzir`)
      return response.data
    } catch (error) {
      return error.response
    }
  }

  async getDistribuicao(receita_id) {
    try {
      const response = await this.api.get(`${this.path}/${receita_id}/distribuicao`)
      return response.data
    } catch (error) {
      return error.response
    }
  }
}

export { ReceitasClient }
