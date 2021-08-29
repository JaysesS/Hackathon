<template>
  <div id="org-chart-container">
    <div :class="['menu-container', {'close': !panelOpen}]">
      <button
        ref="openClosePanelBtn"
        class="open-close-panel-btn open"
        @click="openClosePanel"
      ></button>
      <person
        v-if="personIsSelected && panelOpen"
        :person="selectedPerson"
        @go-to-person="selectPerson"
      ></person>
    </div>
  </div>
</template>

<script lang="ts">
import OrgChart from './org-chart';
import Vue from 'vue';
import { generateOrgChartData, Data } from '../base/data-generator';
import { getRequest } from '../base/http-work';
import Person from './Person.vue';
import {CONST} from './consts.js';

export default Vue.extend({
  name: 'org-chart',
  components: {
    'person': Person
  },
  data() {
    return {
      panelOpen: false,
      data: null,
      orgChart: null,
      selectedPerson : {},
      personIsSelected: false,

      backendURL: CONST.backedRoute
    }
  },
  created() {
    // this.data = generateOrgChartData(10);
  },
  mounted() {
    getRequest(`${this.backendURL}/api/structure`, '', {}).then((res) => {
      if (!res['status'] || !res['body']['status']) {
        alert('Всё плохо)')
        return
      }
      console.log(res)
      this.tree = res['body']['tree']
      this.data = this.tree[0]
      console.log(this.data);

      this.orgChart = new OrgChart(this);
      this.orgChart.draw(this.data);
    })
  },
  methods: {
    test() {
      this.orgChart.draw(this.data)
    },
    bigger() {
      this.orgChart.bigger()
    },
    smaller() {
      this.orgChart.smaller()
    },
    updateData(data) {
      this.data = data
      this.orgChart.draw(this.data)
    },
    selectPerson(person) {
      if (!this.panelOpen) this.$refs['openClosePanelBtn'].click();
      this.selectedPerson = person;
      this.personIsSelected = Object.keys(this.selectedPerson).length !== 0;
    },
    openClosePanel(e){
      e.target.classList.toggle('open');
      e.target.classList.toggle('close');
      this.panelOpen = !this.panelOpen;
    }
  }
})
</script>

<style scoped>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

.orgChart {
  border: 1px solid black;
  height: 100%;
}

.menu-container {
  position: absolute;
  display: flex;
  align-items: center;
  flex-direction: column;
  vertical-align: top;
  width: 30vw;
  min-width: 300px;
  height: 100%;
  background-color: #f5f5f5;
  border-right: 2px solid #2196f3;
  padding: 0.4em;
}
.menu-container.close {
  width: 2em;
  min-width: 2em;
}
.action-title {
  font-size: 28px;
}

.action-item {
  font-size: 24px;
}
.open-close-panel-btn {
  border: none;
  background-repeat: no-repeat;
  background-size: 2em;
  width: 2em;
  height: 2em;
  margin-left: auto;
}
.open-close-panel-btn.open {
  background-image: url("../assets/right-arrow.png");

}
.open-close-panel-btn.close {
  background-image: url("../assets/right-arrow.png");
  -webkit-transform: rotate(180deg);
  -moz-transform: rotate(180deg);
  -ms-transform: rotate(180deg);
  -o-transform: rotate(180deg);
  transform: rotate(180deg);
}
</style>
