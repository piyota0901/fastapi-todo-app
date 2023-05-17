<script setup lang="ts">
import {useTodoStore} from '@/stores/todo';
import { computed,ref } from 'vue';
import {DeleteOutlined,FormOutlined, CheckOutlined} from '@ant-design/icons-vue'
import type { Todo } from '@/interfaces';

const todoStore = useTodoStore()
const getDoneList = computed((): Array<Todo> => {
  return todoStore.getDoneList;
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
const tmpHoverStateUpdate = (): void => {
  todoStore.todoList.forEach((todo: Todo) => {
    tmpHoverState.value.set(todo.id, 'primary')
  })
}

// pushed
const onDoneButtonClick = (id: string) => {
  todoStore.chageStatus(id)
  tmpHoverStateUpdate()
  console.log(`${id} is changed status.`)
  console.log(todoStore.todoList.filter(todo => todo.id == id))
}


</script>
<template>
  <a-table
    :columns="columns"
    :data-source="getDoneList"
    :loading="isLoading"
    :pagination="{ pageSize: 5 }"
    :scroll="{y: 200}"
    class="todolist"
    :showHeader="false"
  >
    <template #bodyCell="{ column, record }">
      <template v-if="column.dataIndex === 'Done'">
        <a-button 
          type="primary" 
          shape="circle" 
          size="small"
          v-on:click="onDoneButtonClick(record.id)"
        >
          <template #icon>
            <CheckOutlined v-if="record.isDone" :style="{fontSize: '14px'}"/>
          </template>
        </a-button>
      </template>
      <template v-if="column.dataIndex === 'edit'">
        <a-button shape="circle" disabled>
          <template #icon>
            <FormOutlined :style="{fontSize: '18px'}"/>
          </template>
        </a-button>
      </template>
      <template v-if="column.dataIndex === 'delete'">
        <a-button shape="circle" danger disabled>
          <template #icon>
            <DeleteOutlined :style="{fontSize: '18px'}"/>
          </template>
        </a-button>
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