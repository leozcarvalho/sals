import axios from "axios";

export async function validateCompanyData(data) {
  const payload = { company: data };
  const path = `${import.meta.env.VITE_FAST_API}/companies/validate_data`;
  let response = null;
  try {
    response = await axios.post(path, payload);
    if (response.data.status === "error") {
      return false;
    } else {
      return true;
    }
  } catch (error) {
    response = { message: error.message, status: "error" };
    return response;
  }
}
