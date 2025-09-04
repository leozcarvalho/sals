import { defineStore } from "pinia";

export const useUserStore = defineStore("user", {
  state: () => ({
    id: null,
    permissions: [],
    accessToken: null,
  }),
  actions: {
    setUser({ id, permissions, accessToken }) {
      this.id = id;
      this.permissions = permissions;
      this.accessToken = accessToken;
    },
    logout() {
      this.$reset();
    },
  },
});
