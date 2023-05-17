<script setup lang="ts">
import {useTodoStore} from '@/stores/todo';
import { computed,ref } from 'vue';
import {DeleteOutlined,FormOutlined, CheckOutlined} from '@ant-design/icons-vue'
import type { Todo } from '@/interfaces';

const todoStore = useTodoStore()
todoStore.fetchTodoList()
const getTodoList = computed((): Array<Todo> => {
  return todoStore.getTodoList;
})

const isLoading = computed((): boolean =>{
  return todoStore.isLoding
})

const columns = [
  {
    title: '',
    dataIndex: 'Done',
    key: 'Done',
    ellipsis: true,
    width: 60,
    align: 'center'
  },
  {
    title: 'Title',
    dataIndex: 'title',
    key: 'title',
  },
  {
    title: 'Comment',
    dataIndex: 'comment',
    key: 'comment',
    ellipsis: true,
  },
  {
    title: 'CreateAt',
    dataIndex: 'createAt',
    key: 'createAt',
    ellipsis: true,
    width: 120,
    align: 'center'
  },
  {
    title: 'Edit',
    dataIndex: 'edit',
    key: 'edit',
    ellipsis: true,
    width: 80,
    align: 'center'
  },
  {
    title: 'Delete',
    dataIndex: 'delete',
    key: 'delete',
    ellipsis: true,
    width: 80,
    align: 'center'
  },
];

// ------------------
// for Done Button
// ------------------
const tmpHoverState = ref(new Map<string, string>());
  todoStore.todoList.forEach((todo: Todo) => {
    tmpHoverState.value.set(todo.id, 'default')
})

// pushed
const onDoneButtonClick = (id: string) => {
  todoStore.chageStatus(id)
  tmpHoverState.value.set(id, 'default'); // 元に戻されたとき用
  console.log(`${id} is changed status.`)
  console.log(todoStore.getById(id))
}

// ------------------
// for Todo Deleting
// ------------------
const onDelete = (id: string) => {
  todoStore.deleteById(id)
};

</script>
<template>
  <h1>Todo List</h1>
  <a-table
    :columns="columns"
    :data-source="getTodoList"
    :loading="isLoading"
    :locale="{ emptyText: 'Loading' }"
    :pagination="{ pageSize: 5 }"
    class="todolist"
  >
    <template #bodyCell="{ column, record }">
      <template v-if="column.dataIndex === 'Done'">
        <a-button
          v-bind:type="tmpHoverState.get(record.id)"
          shape="circle"
          size="small"
          v-on:click="onDoneButtonClick(record.id)"
          v-on:mouseover="tmpHoverState.set(record.id, 'primary')"
          v-on:mouseleave="tmpHoverState.set(record.id, 'default')"
        >
          <template #icon>
            <CheckOutlined v-if="tmpHoverState.get(record.id) == 'primary'" :style="{fontSize: '14px'}"/>
            <p v-else></p>
          </template>
        </a-button>
      </template>
      <template v-if="column.dataIndex === 'edit'">
        <a-button type="primary" shape="circle">
          <template #icon>
            <FormOutlined :style="{fontSize: '18px'}"/>
          </template>
        </a-button>
      </template>
      <template v-if="column.dataIndex === 'delete'">
        <a-popconfirm
          title="Are you sure delete this todo?"
          ok-text="Yes"
          cancel-text="No"
          @confirm="onDelete(record.id)"
        >
          <a-button type="primary" shape="circle" danger>
            <template #icon>
              <DeleteOutlined :style="{fontSize: '18px'}"/>
            </template>
          </a-button>
        </a-popconfirm>
      </template>
    </template>
  </a-table>
</template>
<style scoped>
h1 {
  margin-left: 8px;
  margin-top: 8px;
  margin-bottom: 10.5px;
}

.todolist {
  text-align: center;
}
</style>