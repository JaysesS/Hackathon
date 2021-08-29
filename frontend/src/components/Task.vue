<template>
  <div class="task-wrapper">
    {{task}}
  </div>
</template>

<script>
export default {
  name: "Task",
  props: {
    task: {
      type: Object,
      required: true
    }
  }
}
</script>

<style scoped>
.task-wrapper {
  width: 100%;
  border-radius: 6px;
  margin: 0.4em 0;
  background: #ffffff;
  box-shadow: 0 2px 4px 0 #cdcdcd;
  padding: 0.6em;
}
</style>
