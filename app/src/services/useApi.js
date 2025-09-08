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
      if (error.response?.status === 401) {
        const userStore = useUserStore();
        userStore.logout();
        router.push({ name: "auth-signin" });
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
