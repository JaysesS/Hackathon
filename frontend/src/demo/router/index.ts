import Vue from 'vue';
import Router from 'vue-router';
import CanvasTree from '../../components/CanvasTree.vue';
import TaskCreation from '../../components/TaskCreation.vue';
import TaskList from '../../components/TaskList.vue';
import * as Cons from './constant';

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      redirect: Cons.CANVAS_TREE
    },
    {
      path: '/' + Cons.CANVAS_TREE,
      name: Cons.CANVAS_TREE,
      component: CanvasTree
    },
    {
      path: '/' + Cons.TASK_CREATION,
      name: Cons.TASK_CREATION,
      component: TaskCreation
    },
    {
      path: '/' + Cons.TASK_LIST,
      name: Cons.TASK_LIST,
      component: TaskList
    },
  ]
})
