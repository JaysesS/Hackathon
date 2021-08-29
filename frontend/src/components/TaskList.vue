<template>
  <div class="task-list-wrapper">
    <task v-for="task in tasks" :key="task.id" :task="task"></task>
  </div>
</template>

<script>
import Task from './Task.vue'
import { CONST } from './consts'
import { getRequest } from '../base/http-work'

export default {
  name: 'TaskList',
  components: {
    task: Task
  },
  data: () => {
    return {
      tasks: [],
      backendURL: CONST.backedRoute
    }
  },
  methods: {},
  created() {
    getRequest(`${this.backendURL}/api/task`, { started: false }, {}).then(
      (res) => {
        if (!res['status'] || !res['body']['status']) {
          alert('Всё плохо)')
          return
        }
        console.log(res)
        this.tasks = res['body']['tasks']
      }
    )
  }
}
</script>

<style scoped>
.task-list-wrapper {
  padding: 2em;

  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  gap: 1em;
  justify-content: flex-start;
  align-items: flex-start;
}
</style>
