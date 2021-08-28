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
          Количество переменным
        </p>
        <input
          type="number"
          class="input"
          v-model="varCount"
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
export default {
  name: "TaskCreation",
  props: {
    persons: {
      type: Array,
    },
  },
  data: () => {
    return {
      name: '',
      processName: '',
      startDateString: '',
      startTimeString: '',
      dueDateString: '',
      dueTimeString: '',
      priority: 0,
      varCount: 0,
      owner_id: 0,
      assigner_id: 0,
    }
  },
  methods: {

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
}
.input-wrapper {
  padding: 0.2em;
  width: 26em;
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
</style>
