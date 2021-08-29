<template>
  <v-app>
    <v-toolbar>
      <v-btn
        class="menu-item"
        :to="Cons.CANVAS_TREE"
        text
        style="margin-left: 32px;"
        :color="selectedMenu === 'canvas' ? 'info' : ''"
        >Структура организации</v-btn
      >
      <v-btn
        class="menu-item"
        :to="Cons.TASK_CREATION"
        text
        style="margin-left: 32px;"
        :color="selectedMenu === 'creation' ? 'info' : ''"
        >Создание задачи</v-btn
      >
      <v-btn
        class="menu-item"
        :to="Cons.TASK_LIST"
        text
        style="margin-left: 32px;"
        :color="selectedMenu === 'taskList' ? 'info' : ''"
        >Активные задачи</v-btn
      >
    </v-toolbar>
    <router-view style="width: 100%; height: 100%;" />
  </v-app>
</template>

<script lang="ts">
import * as Cons from './router/constant'

export default {
  name: 'App',
  data() {
    return {
      Cons,
      selectedMenu: 'canvas'
    }
  },
  watch: {
    $route() {
      this.updateSelectedMenu()
    }
  },
  created() {
    this.updateSelectedMenu()
  },
  methods: {
    backtoMenu() {
      this.$router.push('main')
    },
    updateSelectedMenu() {
      switch (this.$route.path) {
        case `/${Cons.CANVAS_TREE}`:
          this.selectedMenu = 'canvas'
          break
        case `/${Cons.TASK_CREATION}`:
          this.selectedMenu = 'creation'
          break
        case `/${Cons.TASK_LIST}`:
          this.selectedMenu = 'taskList'
          break


        default:
          this.selectedMenu = 'canvas'
          break
      }
    }
  }
}
</script>

<style lang="less" scoped>
.menu-item {
  display: flex;
  height: 100%;
  margin: 0;
}
</style>
