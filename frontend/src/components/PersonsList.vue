<template>
  <div class="person-list-wrapper">
    <div
      v-for="person in personList"
      :class="['person-card', {ranked: person.rank}]"
    >
      <h3>{{person.name}}</h3>
      <p>Должность: {{person.position}}</p>
      <p>Количество текущих задач: {{person.task_count}}</p>
      <span
        v-if="person.rank"
        class="ranked"
      ></span>
      <p
        v-if="person.rank"
        class="person-rank"
      >
        {{getRecText(person.rank)}}
      </p>
      <v-btn
        @click="setTask(person.id)"
      >Назначить задачу</v-btn>
    </div>
  </div>
</template>

<script>
import {CONST} from "./consts";
import {postRequest} from "../base/http-work";

export default {
  name: "PersonsList",
  props: {
    personList: {
      type: Array,
      default: []
    },
    taskId: {
      type: Number
    }
  },
  data: () => {
    return {
      BACKEND_URL: CONST.backedRoute
    }
  },
  methods: {
    getRecText(rank){
      switch (rank){
        case 3:
          return 'Лучше всего подходит для выполнения задачи';
        case 2:
          return 'Хорошо подходит для выполнения задачи';
        case 1:
          return 'Подходит для выполнения задачи';

        default:
          return 'error';
      }
    },
    setTask(id){
    //    {
    //     "id": int, // required task id
    //     "assigner_id": int, // optional
    //     "owner_id": int, // optional
    //     "state" : "start" or "stop" // optional
    // }
      const body = {
        id: this.taskId,
        assigner_id: id
      };
      postRequest(`${this.BACKEND_URL}/api/task/manage`, body)
        .then( r => {
          this.$router.push('/');
        });
    }
  }
}
</script>

<style scoped>
p {
  margin: 0;
}
.person-list-wrapper {
  display: flex;
  flex-direction: column;
  gap: 1em;
}
.person-card {
  border-radius: 6px;
  background: #ffffff;
  box-shadow: 0 2px 4px 0 #cdcdcd;
  padding: 0.4em 1.6em 0.4em 0.6em;
  position: relative;
}
.person-card.ranked {
}
.person-rank {
  color: darkgreen;
}
span.ranked {
  background-image: url("../assets/checked.jpg");
  display: block;
  width: 1.2em;
  height: 1.2em;
  background-size: contain;
  position: absolute;
  right: 0.4em;
  top: 0.4em;
}
</style>
