import { defineStore } from "pinia";
import type { Todo } from "@/interfaces";
import axios from "axios";

export const useTodoStore = defineStore("todo", {
  state: () => {
    return {
      todoList: new Array<Todo>(),
      isLoding: true,
    };
  },
  getters: {
    getTodoList(): Array<Todo> {
      return this.todoList.filter((todo) => !todo.isDone);
    },
    getDoneList(): Array<Todo> {
      return this.todoList.filter((todo: Todo) => todo.isDone);
    },
    getById: (state) => {
      return (id: string): Todo => {
        const todo = state.todoList.filter((todo: Todo) => todo.id === id)[0];
        return todo;
      };
    },
  },
  actions: {
    async fetchTodoList() {
      const todoListURL = "http://localhost:8000/todo/todos";
      const response = await axios.get(todoListURL);
      let todoListArray = response.data;
      todoListArray.forEach((todo: Todo) => {
        // 日付のみ抽出: 2023-05-06T14:09:11.746865 ⇒ 2023-05-06
        todo.createAt = todo.createAt.split("T")[0];
      });
      const _sleep = (ms: number) =>
        new Promise((resolve) => setTimeout(resolve, ms));
      await _sleep(1000);
      this.todoList = todoListArray;
      this.isLoding = false;
    },
    async deleteById(id: string) {
      this.todoList = this.todoList.filter((todo: Todo) => todo.id !== id);
      console.log(`${id} is deleted.`);
    },
    async chageStatus(id: string) {
      this.todoList = this.todoList.map((todo) =>
        todo.id === id ? { ...todo, isDone: !todo.isDone } : todo
      );
    },
  },
});
