import { defineStore } from 'pinia';

export const useStore = defineStore({
  id: 'main',
  state: () => ({
    message: '',
    event: '',
    component: '',
    counter: 0,
  }),
  actions: {
    setMessage(newComponent, newEvent, newMessage) {
        this.component = newComponent;
        this.event = newEvent;
        this.message = newMessage;
    },
    incrementCounter() {
        this.counter++;
    },
  }
});