import { useUserStore } from "../stores/userStore";

export const isLoggedIn = () => {
  const userStore = useUserStore();
  return Boolean(userStore.accessToken);
}

export const logout = () => {
  const userStore = useUserStore();
  userStore.logout();
}

export const getCookie = (name) => {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

export function loadUserFromCookie() {
  const userStore = useUserStore();
  const cookie = getCookie("session");
  if (!cookie) return;
  try {
    const jsonString = cookie.replace(/\\054/g, ",");
    const firstParse = JSON.parse(jsonString);
    const data = typeof firstParse === "string" ? JSON.parse(firstParse) : firstParse;
    if (data?.user_id) {
      userStore.setUser({
        id: data.user_id,
        permissions: data.permissions || [],
      });
    }
  } catch (err) {
    console.error("Erro ao carregar cookie:", err);
  }
}

export function can(permission) {
  console.log("Checking permission:", permission);
  if (!permission) return true;
  const userStore = useUserStore();
  console.log("User permissions:", userStore.permissions);
  return userStore.permissions.includes(permission);
}