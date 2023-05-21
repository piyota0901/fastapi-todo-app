<script setup lang="ts">
import {useTodoStore} from '@/stores/todo';
import { reactive } from 'vue';
import type { UnwrapRef } from 'vue';
import type { NewTodo } from '@/interfaces';
import { PlusOutlined } from '@ant-design/icons-vue';

const todoStore = useTodoStore()

const formState: UnwrapRef<NewTodo> = reactive({
  title: '',
  comment: ''
})

const handleFinish = (): void => {
  const newTodo = {...formState}
  todoStore.add(newTodo)
  formState.title = ''
  formState.comment = ''
}


</script>
<template>
  <a-form
    layout="inline"
    :model="formState"
    @finish="handleFinish"
  >
    <a-form-item>
      <a-button
        type="primary"
        html-type="submit"
        shape="circle"
        :disabled="formState.title === '' && formState.title === ''"
      >
      <template #icon>
        <PlusOutlined />
      </template>
      </a-button>
    </a-form-item>
    <a-form-item>
      <a-input
        v-model:value="formState.title"
        placeholder="Title"
        addonBefore="Title"
        >
      </a-input>
    </a-form-item>
    <a-form-item>
      <a-input
        v-model:value="formState.comment"
        placeholder="Comment"
        addonBefore="Comment"
      >
      </a-input>
    </a-form-item>
  </a-form>
</template>
<style scoped>
</style>