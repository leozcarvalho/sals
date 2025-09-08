import { useApi } from "./useApi";

const userApi = {};

const api = useApi();

userApi.auth = async (email, password) => {
  let formData = new FormData();
  formData.append("username", email);
  formData.append("password", password);
  try {
    const response = await api.post("/login", formData);
    return response.data;
  } catch (error) {
    console.log("response error", error)
    return error;
  }
};

userApi.recoveryPassword = async (email) => {
  try {
    const response = await api.patch(
      "/users/recovery-password",
      {},
      {
        params: {
          email: email,
        },
      }
    );
    return response.data;
  } catch (error) {
    return error.response;
  }
};

userApi.createPassword = async (data) => {
  try {
    const response = await api.patch(`/users/update-password`, data);
    return response.data;
  } catch (error) {
    return error.response;
  }
};


userApi.saveUser = async (payload) => {
  try {
    const response = await api.post(`/users/save`, { user: payload });
    return response;
  } catch (error) {
    return error.response;
  }
};

userApi.updateUser = async (userId, payload) => {
  try {
    const response = await api.put(`/users/${userId}`, { user: payload });
    return response;
  } catch (error) {
    return error.response;
  }
};



userApi.getCurrentUser = async () => {
  try {
    const response = await api.get(`/users/current/self`);
    return response;
  } catch (error) {
    return error.response;
  }
};

export { userApi };
