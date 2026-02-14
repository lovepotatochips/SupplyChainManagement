<template>
  <!-- router-view是Vue Router提供的组件 -->
  <!-- 用于根据当前路由路径动态渲染对应的页面组件 -->
  <!-- 这是应用的根组件，所有页面都会在这里渲染 -->
  <router-view />
</template>

<script setup lang="ts">
// 使用<script setup>语法糖，这是Vue 3推荐的方式
// 所有在<script setup>中定义的变量和函数都会自动暴露给模板使用
// 不需要手动导出，编译时会自动处理
</script>

<style>
/* 全局样式重置 */

* {
  /* 清除所有元素的外边距 */
  margin: 0;
  /* 清除所有元素的内边距 */
  padding: 0;
  /* 盒模型设置为border-box，元素的宽高包含padding和border */
  /* 这样设置后，padding和border不会增加元素的实际宽高 */
  box-sizing: border-box;
}

html, body, #app {
  /* 设置html、body和#app容器的宽度为100% */
  width: 100%;
  /* 设置高度为100%，让应用占满整个视口 */
  height: 100%;
}
</style>
