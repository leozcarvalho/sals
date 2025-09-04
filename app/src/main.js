import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";
import mdiVue from "mdi-vue/v3";
import * as mdijs from "@mdi/js";
import VueGoogleMaps from "vue-google-maps-community-fork";
import Vue3ColorPicker from "vue3-colorpicker";
import "vue3-colorpicker/style.css";

const options = {
  // You can set your default options here
};

import router from "./router";

// Template components
import BaseBlock from "@/components/BaseBlock.vue";
import BaseBackground from "@/components/BaseBackground.vue";
import BasePageHeading from "@/components/BasePageHeading.vue";
import VAsyncSelect from "@/components/VAsyncSelect.vue";

// Template directives
import clickRipple from "@/directives/clickRipple";

// Bootstrap framework
import * as bootstrap from "bootstrap";
window.bootstrap = bootstrap;

//datepicker
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css';

// Craft new application
const app = createApp(App);

// Register global components
app.component("BaseBlock", BaseBlock);
app.component("BaseBackground", BaseBackground);
app.component("BasePageHeading", BasePageHeading);
app.component('VueDatePicker', VueDatePicker);
app.component('VAsyncSelect', VAsyncSelect)

// Register global directives
app.directive("click-ripple", clickRipple);

// Google Maps component Library
app.use(VueGoogleMaps, {
  load: {
    key: `${import.meta.env.VITE_GOOGLE_API}`,
    libraries: "places",
    language: "pt-BR",
  },
});

// Use Pinia and Vue Router
app.use(createPinia());
app.use(Vue3ColorPicker)
app.use(router);
app.use(Toast, options);
app.use(mdiVue, {
  icons: mdijs,
});

app.mount("#app");
