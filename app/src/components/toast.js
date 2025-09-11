import { useToast } from "vue-toastification";

const toast = useToast();

export const toastApi = (variant, message) => {
  if (variant == "success") toast.success(message);
  if (variant == "failed" || variant == "error") toast.error(message);
  if (variant == "warning") toast.warning(message);
};

export const handleApiToast = (response, successMessage = "Operação realizada com sucesso") => {
  if (response.success) {
    toastApi("success", successMessage);
  } else {
    const errorMessage =
      response.error || response?.data?.error || "Erro inesperado";
    toastApi("error", errorMessage);
  }
};