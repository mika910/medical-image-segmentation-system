<template>
  <el-table-column
    v-if="counter.device == '电脑端' && props.type === 'index'"
    type="index"
    :label="props.label"
    :width="props.width"
    :align="props.align"

  />
  <el-table-column
    v-else-if="counter.device == '电脑端' && props.type === 'selection'"
    type="selection"
    :label="props.label"
    :width="props.width"
    :align="props.align"

  />
  <el-table-column
    v-else-if="counter.device == '电脑端'"
    :type="props.type"
    :label="props.label"
    :align="props.align"
    :prop="props.prop"
    :show-overflow-tooltip="props.showOverflowTooltip"
    :width="props.width"
    :fixed="props.fixed"

  >
    <template #default="scope">
      <slot :row="scope.row">
        <div>
          {{ scope.row[props.prop] }}
        </div>
      </slot>
    </template>
  </el-table-column>
  <div v-else>
    <slot :row="props.scope">
      <div>
        {{ props.scope[props.prop] }}
      </div>
    </slot>
  </div>
</template>

<script setup>
import {reactive } from "vue";
import { useCounterStore } from "@/stores/counter";
const counter = useCounterStore();


const props = defineProps({
  scope: {},
  type: {
    type: String,
    default: "default",
  },
  label: String,
  className: String,
  labelClassName: String,
  property: String,
  prop: String,
  width: {},
  minWidth: {},
  renderHeader: Function,
  sortable: {
    type: [Boolean, String],
    default: false,
  },
  sortMethod: Function,
  sortBy: [String, Function, Array],
  resizable: {
    type: Boolean,
    default: true,
  },
  columnKey: String,
  align: String,
  headerAlign: String,
  showTooltipWhenOverflow: Boolean,
  showOverflowTooltip: Boolean,
  fixed: [Boolean, String],
  formatter: Function,
  selectable: Function,
  reserveSelection: Boolean,
  filterMethod: Function,
  filteredValue: Array,
  filters: Array,
  filterPlacement: String,
  filterMultiple: {
    type: Boolean,
    default: true,
  },
  index: [Number, Function],
  sortOrders: {
    type: Array,
    default() {
      return ["ascending", "descending", null];
    },
    validator(val) {
      return val.every(
        (order) => ["ascending", "descending", null].indexOf(order) > -1
      );
    },
  },

});





</script>
