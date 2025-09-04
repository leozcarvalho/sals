import axios from "axios";
import { isLoggedIn, loggout } from "../helpers/userSession";

let api;

export function createApi() {
  api = axios.create({
    baseURL: import.meta.env.VITE_FAST_API,
    withCredentials: true,
  });

  api.interceptors.request.use((config) => {
    if (isLoggedIn) {
      config.headers = {
        ...config.headers,
        Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
      };
    }
    return config;
  });

  api.interceptors.response.use(
    (response) => response, // Passa as respostas bem-sucedidas
    (error) => {
      if (error.response?.status === 401) {
        loggout();
        const currentPath = window.location.pathname;
        if (currentPath !== '/login' && currentPath !== '/') {
          window.location.href = '/login';
        }
      }
      return Promise.reject(error); // Para garantir que o erro seja tratado corretamente
    }
  );
  return api;
}

export function useApi() {
  if (!api) {
    createApi();
  }
  return api;
}

/*
const handle = async (promise) => {
    try {
      const response = await promise;
      return response.data; // já retorna o ApiResponse
    } catch (error) {
      // aqui você pode padronizar o erro
      return {
        success: false,
        data: null,
        error: error.response?.data?.error || error.message || "Erro desconhecido",
      };
    }
  };
*/