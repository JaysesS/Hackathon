<template>
  <div class="creation-task-view">
    <!--    <h2>Создание задачи</h2>-->
    <div class="task-inputs">
      <div class="input-wrapper">
        <p
        >
          Название задачи
        </p>
        <input
          type="text"
          class="input"
          v-model="name"
        >
      </div>
      <div class="input-wrapper">
        <p
        >
          Название процесса
        </p>
        <input
          type="text"
          class="input"
          v-model="processName"
        >
      </div>
      <div class="input-wrapper">
        <p>
          Время начала задачи
        </p>
        <div class="time-input-wrapper">
          <input
            type="date"
            class="input"
            v-model="startDateString"
          >
          <input
            type="time"
            class="input"
            v-model="startTimeString"
          >
        </div>
      </div>
      <div class="input-wrapper">
        <p>
          Выполнить до
        </p>
        <div class="time-input-wrapper">
          <input
            type="date"
            class="input"
            v-model="dueDateString"
          >
          <input
            type="time"
            class="input"
            v-model="dueTimeString"
          >
        </div>
      </div>
      <div class="input-wrapper">
        <p
        >
          Приоритет
        </p>
        <select
          class="input"
          v-model="priority"
        >
          <option
            v-for="pr in Array.from({length: 10}, (_, i) => i + 1)"
            :value="pr"
          >{{pr}}</option>
        </select>
      </div>
      <div class="input-wrapper">
        <p
        >
          Количество переменных
        </p>
        <input
          type="number"
          class="input"
          v-model="varCount"
          min="0"
        >
      </div>
      <div class="input-wrapper">
        <p
        >
          Постановщик задачи
        </p>
        <select
          class="input"
          v-model="owner_id"
        >
          <option
            v-for="person in persons"
            :value="person.id"
          >{{person.name}}</option>
        </select>
      </div>
      <div class="input-wrapper">
        <p
        >
          Ответственный
        </p>
        <select
          class="input"
          v-model="assigner_id"
        >
          <option
            v-for="person in persons"
            :value="person.id"
          >{{person.name}}</option>
        </select>
      </div>
      <button
        :class="['main-btn', {'disabled': disabled}]"
        :disabled="disabled || taskCreated"
        v-on:click="createTask"
      >Создать задачу</button>
      <span
        v-if="taskCreated"
        class="task-created-msg"
      >
        Задача успешно создана
      </span>
    </div>

  </div>
</template>

<script>
// name = fields.Str(required=True, allow_none=False)
//   process_name = fields.Str(required=True, allow_none=False)
//   start_time = fields.Int(required=True, allow_none=False)
//   due_time = fields.Int(required=True, allow_none=False)
//   priority = fields.Int(required=True, allow_none=False)
//   var_count = fields.Int(required=True, allow_none=False) кол-во переменных
//   owner_id = fields.Int(required=True, allow_none=False) кто поставил
//   assigner_id = fields.Int(required=True, allow_none=False) кто выполняет
import {getRequest, postRequest} from "../base/http-work";
import {CONST} from "./consts";

export default {
  name: "TaskCreation",
  data: () => {
    return {
      persons: [],
      name: '',
      processName: '',
      startDateString: '',
      startTimeString: '',
      dueDateString: '',
      dueTimeString: '',
      priority: 0,
      varCount: 0,
      owner_id: null,
      assigner_id: null,

      backendURL: CONST.backedRoute,

      taskCreated: false

    }
  },
  methods: {
    createTask() {
      const startTime = new Date(`${this.startDateString}T${this.startTimeString}`).getTime() / 1000;
      const dueTime = new Date(`${this.dueDateString}T${this.dueTimeString}`).getTime() / 1000;
      const body = {
        name: this.name,
        process_name: this.processName,
        start_time: startTime,
        due_time: dueTime,
        priority: +this.priority,
        var_count: +this.varCount,
        owner_id: +this.owner_id,
        assigner_id: +this.assigner_id
      }
      postRequest(`${this.backendURL}/api/task`, body)
        .then( res => {
          if (!res['status'] || !res['body']['status']) {
            alert('Всё плохо)');
            return;
          }
          this.taskCreated = true;
        })
    }
  },
  created() {
    getRequest(`${this.backendURL}/api/structure`, {flat: true}, {}).then((res) => {
      if (!res['status'] || !res['body']['status']) {
        alert('Всё плохо)')
        return
      }
      console.log(res);
      this.persons = res['body']['users'];
    })
  },
  computed: {
    disabled: function (){
      return this.name.length === 0 ||
        this.processName.length === 0 ||
        this.startTimeString.length === 0 ||
        this.startDateString.length === 0 ||
        this.dueTimeString.length === 0 ||
        this.dueDateString.length === 0 ||
        this.priority === 0 ||
        this.varCount < 0 ||
        !this.owner_id ||
        !this.assigner_id;
    }
  }
}
</script>

<style scoped>
p {
  margin: 0;
}
.creation-task-view {
  padding: 2em 2em;
}
.task-inputs {
  border-radius: 6px;
  background: #ffffff;
  box-shadow: 0 2px 4px 0 #cdcdcd;
  padding: 1em;

  display: flex;
  flex-direction: column;
  gap: 0.4em;
  width: 26em;
}
.input-wrapper {
  padding: 0.2em;
  width: 100%;
}
.input {
  border-radius: 6px;
  border: 2px solid #e0e0e0;
  line-height: 2em;
  width: 100%;
}
.time-input-wrapper {
  width: 100%;
  display: flex;
  flex-direction: row;
}
.main-btn {
  padding: 1em 4em;
  width: 100%;
  background: #2196f3;
  border-radius: 6px;

  color: #FFFFFF;
  font-size: 1.2em;
}
.main-btn.disabled {
  background: #a7a7a7;
}
.main-btn.disabled:hover {
  background: #a7a7a7;
}
.main-btn:hover {
  background: #2c3e50;
}
.task-created-msg {
  font-size: 1.2em;
  color: darkgreen;
  font-weight: bold;
}
</style>
