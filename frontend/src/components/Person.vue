<template>
  <div class="person-card">
    <h2 class="center-text">{{person.name}}</h2>
    <p>Должность: {{person.position}}</p>
    <div
      v-if="false && person.children.length !== 0"
      class="children-wrapper"
    >
      <p>Подчинённые:</p>
      <div
        v-for="child in person.children"
        :key="child.id"
        v-on:click="goToPerson(child)"
        class="sub-person"
      >
        <p>{{child.name}}</p>
      </div>
    </div>
    <div class="tasks-wrapper">
      <p>Задачи</p>
      <!--      v-for="task in person.tasks"-->
      <task
        v-for="task in tasks"
        :task="task"
        class="task"
      ></task>
    </div>
  </div>
</template>

<script>
import Task from './Task.vue';
import {getRequest} from "../base/http-work";
import {CONST} from "./consts";

export default {
  name: "Person",
  components: {
    'task': Task
  },
  props: {
    person: {
      type: Object,
      required: true
    }
  },
  data: () => {
    return {
      tasks: [],
      backendURL: CONST.backedRoute,

      oldPersonId: -1,
    }
  },
  methods: {
    goToPerson(person) {
      this.$emit('go-to-person', person);
    },
    updateTasks() {
      getRequest(`${this.backendURL}/api/task`, { assigner_id: this.person.id }, {})
        .then(
          (res) => {
            if (!res['status'] || !res['body']['status']) {
              alert('Всё плохо)')
              return
            }
            console.log(res);
            this.tasks = res['body']['tasks'];
          }
        )
    }
  },
  created() {
    this.updateTasks();
  },

  updated() {
    if (this.oldPersonId !== this.person.id) {
      this.oldPersonId = this.person.id;
      this.updateTasks();
    }
  }
}
</script>

<style scoped>
p {
  margin: 0;
}
.person-card {
  margin: 1em;
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 0.6em;
}
.center-text {
  text-align: center;
}
.children-wrapper {
  border: 2px solid #2196f3;
  padding: 0.6em;
  border-radius: 6px;
}
.tasks-wrapper {
  padding: 0.6em;
  height: 36em;
  min-height: 300px;
  overflow-y: auto;
  border: 2px solid #2196f3;
  border-radius: 6px;

  display: flex;
  flex-direction: column;
  gap: 0.4em;
}
.sub-person {
  border-radius: 6px;
  margin: 0.4em 0;
  background: #ffffff;
  box-shadow: 0 2px 4px 0 #cdcdcd;
  padding: 0.6em;
}
</style>
