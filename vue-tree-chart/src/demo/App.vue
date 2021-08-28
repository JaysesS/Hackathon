<template>
  <v-app>
    <v-toolbar>
      <v-toolbar-side-icon></v-toolbar-side-icon>
      <v-toolbar-title>Структура организации</v-toolbar-title>
      <v-btn
        class="menu-item"
        :to="Cons.CANVAS_TREE"
        text
        style="margin-left: 32px;"
        :color="selectedMenu === 'canvas' ? 'info' : ''"
        >Canvas Chart</v-btn
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
      if (this.$route.path === `/${Cons.CANVAS_TREE}`) {
        this.selectedMenu = 'canvas'
      } else {
        this.selectedMenu = 'svg'
      }
    }
  }
}
</script>

<style lang="less" scoped>
.menu-item {
  display: inline-block;
  display: flex;
  height: 100%;
  margin: 0;
}
</style>
