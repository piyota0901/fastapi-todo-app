<script setup lang="ts">
import { ref } from 'vue';
import TodoList from './TodoList.vue';
import Header from './Header.vue';
import Footer from './Footer.vue';
import DoneList from './DoneList.vue'
import { CaretRightOutlined } from '@ant-design/icons-vue';

const isActive = ref(false)

</script>
<template>
  <a-layout class="layout">
    <Header />
    <a-layout-content class="main-content">
      <div class="todolist-content">
        <TodoList />
      </div>
      <div class="donelist-content" ghost>
        <div class="collapse">
          <h3>
            <CaretRightOutlined
              :rotate="isActive ? 90 : 0"
              v-on:click="isActive = !isActive"
            />
            Done
          </h3>
        </div>
        <template v-if="isActive">
          <DoneList />
        </template>
      </div>
    </a-layout-content>
    <Footer />
  </a-layout>
</template>
<style scoped>
.layout {
  height: 100%;
}

.todolist-content {
  width: 60%;
  height: 480px;
  margin: auto;
}

.donelist-content {
  width: 60%;
  margin: auto;
}

.collapse  {
    margin-bottom: 10.5px;
}

</style>