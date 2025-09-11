import axios from "axios";
import { useUserStore } from "../stores/userStore";

let api;

export function createApi() {
  api = axios.create({
    baseURL: import.meta.env.VITE_FAST_API,
    withCredentials: true,
  });

  // Interceptor de respostas
  api.interceptors.response.use(
    (response) => response,
    (error) => {
      const status = error.response?.status;
      const currentPath = window.location.pathname;

      if (status === 401) {
        const userStore = useUserStore();
        userStore.logout();
        if (currentPath !== '/login' && currentPath !== '/') {
          window.location.href = '/login';
        }
      } else if (status === 403) {
        // Redireciona para página de erro / acesso negado
        if (currentPath !== '/errors/403') {
          window.location.href = '/errors/403';
        }
      }

      return Promise.reject(error);
    }
  );

  return api;
}

// Hook para usar a instância
export function useApi() {
  if (!api) {
    createApi();
  }
  return api;
}

/*
// Função utilitária para padronizar chamadas de API
const handle = async (promise) => {
  try {
    const response = await promise;
    return response.data; // já retorna ApiResponse
  } catch (error) {
    return {
      success: false,
      data: null,
      error: error.response?.data?.error || error.message || "Erro desconhecido",
    };
  }
};
*/
