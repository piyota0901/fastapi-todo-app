export interface Todo {
  id: string;
  title: string;
  comment: string;
  isDone: boolean;
  createAt: string;
}

export interface NewTodo {
  title: string;
  comment: string;
}
