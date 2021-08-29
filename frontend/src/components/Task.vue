<template>
  <div class="task-wrapper">
    <h2>{{ task.name }}</h2>
    <p>Процесс: {{ task.process_name }}</p>
    <div class="task-time-wrapper">
      <span>
        Начало задачи:
        {{ new Date(task.start_time * 1000).toLocaleString('Ru') }}
      </span>
      <span>
        Срок задачи: {{ new Date(task.due_time * 1000).toLocaleString('Ru') }}
      </span>
    </div>
    <div
      v-if="task.assigner_id"
    >
      <p>Ответственный</p>
      <input disabled :value="assignerName" />
    </div>
    <div>
      <p>Задачу создал</p>
      <input disabled :value="ownerName" />
    </div>
    <p>Приоритет: {{ task.priority }}</p>
    <p>Количество переменных: {{ task.var_count }}</p>
<!--    <button class="main-btn" @click="setTask">Назначить задачу</button>-->
  </div>
</template>

<script>
// {
//             "assigner_id": 19,
//             "due_time": 1630216753,
//             "end_time": 1630209553,
//             "id": 1,
//             "name": "Фикс чего-то там",
//             "owner_id": 13,
//             "priority": 75,
//             "process_name": "Поддержка",
//             "start_time": 1630187953,
//             "started": false,
//             "var_count": 2
//         }
import { CONST } from './consts'
import { getRequest } from '../base/http-work'
import * as Cons from '../demo/router/constant'

export default {
  name: 'Task',
  props: {
    task: {
      type: Object,
      required: true
    }
  },
  data: () => {
    return {
      backendURL: CONST.backedRoute,
      assignerName: '',
      ownerName: '',
      assigner: null,
      owner: null
    }
  },
  methods: {
    getUsersById(assignerId, ownerId) {
      getRequest(`${this.backendURL}/api/tree`, { id: assignerId }, {}).then(
        (res) => {
          if (!res['status'] || !res['body']['status']) {
            alert('Всё плохо)')
            return
          }
          console.log(res)
          this.assignerName = res['body']['node']['name']
          this.assigner = res['body']['node']
        }
      )
      getRequest(`${this.backendURL}/api/tree`, { id: ownerId }, {}).then(
        (res) => {
          if (!res['status'] || !res['body']['status']) {
            alert('Всё плохо)')
            return
          }
          console.log(res)
          this.ownerName = res['body']['node']['name']
          this.owner = res['body']['node']
        }
      )
    },
    setTask() {
      // this.$router.push({
      //   name: Cons.CANVAS_TASK_SET,
      //   params: { 'users-list': ['user'] }
      // })
    }
  },
  created() {
    this.getUsersById(this.task.assigner_id, this.task.owner_id)
  }
}
</script>

<style scoped>
p {
  margin: 0;
}
.task-wrapper {
  border-radius: 6px;
  background: #ffffff;
  box-shadow: 0 2px 4px 0 #cdcdcd;
  padding: 0.4em 0.6em;

  display: flex;
  flex-direction: column;
  gap: 0.265em;
}
.center-text {
  text-align: center;
}
.task-time-wrapper {
  display: flex;
  flex-direction: column;
  gap: 0.185em;
}
input {
  border-radius: 6px;
  border: 2px solid #e0e0e0;
  line-height: 2em;
  width: 100%;
  padding: 0.2em 0.4em;
}
.main-btn {
  color: #ffffff;
  background-color: #2196f3;
  padding: 0.265em 2em;
  cursor: pointer;
  border-radius: 6px;
}
.main-btn:hover {
  background-color: #2c3e50;
}
</style>
