import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import { DatePicker } from "ant-design-vue";

const app = createApp(App);

app.use(createPinia());
app.use(DatePicker);

app.mount("#app");
