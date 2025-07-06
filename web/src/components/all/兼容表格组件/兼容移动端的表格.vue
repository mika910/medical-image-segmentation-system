<template>
  <el-table
    :data="props.data"
    @selection-change="selectionChange"
    :border="props.border"
    v-if="counter.device == '电脑端'"
  >
    <slot></slot>
  </el-table>

  <div v-else>
    <template v-for="(item, i) in props.data" :key="item.id">
      <el-card shadow="never">
        <el-form
          label-position="top"
          label-width="100px"
          style="max-width: 460px"
        >
          <el-checkbox
            v-model="item['_checked']"
            label="选中"
            @change="handleSelectionChange"
            v-if="isNeedSelection"
          />
          <template v-for="citem in proxy.$slots['default']()" :key="citem">
            <template v-if="citem.props">
              <template v-if="citem.props.type === 'index'"> </template>
              <template v-else-if="citem.props.type === 'expand'"> </template>
              <template v-else-if="citem.props.type === 'selection'">
              </template>
              <el-form-item v-else :label="citem.props.label">
                <template v-if="citem && citem.children">
                  <component
                    :is="citem"
                    :scope="item"
                    :prop="citem.props.prop"
                  ></component>
                </template>
                <template v-else>
                  <component :is="citem" :scope="item">
                    {{ item[citem.props.prop] }}</component
                  >
                </template>
                <!-- <el-divider></el-divider> -->
              </el-form-item>
            </template>
          </template>
        </el-form>
      </el-card>
      <el-divider v-if="i + 1 != props.data.length"></el-divider>
    </template>
  </div>
</template>

<script setup>
import { getCurrentInstance, reactive, ref, computed } from "vue";
import { useCounterStore } from "@/stores/counter";
const counter = useCounterStore();



const { proxy } = getCurrentInstance(); // 获取实例中的proxy

// console.log(proxy);
// console.log(proxy.$slots["default"]());
// console.log(proxy.$slots["default"]()[0].type.render());

const props = defineProps({
  data: {
    type: Array,
    default: function () {
      return [];
    },
  },
  size: String,
  width: [String, Number],
  height: [String, Number],
  maxHeight: [String, Number],
  fit: {
    type: Boolean,
    default: true,
  },
  stripe: Boolean,
  border: Boolean,
  rowKey: [String, Function],
  context: {},
  showHeader: {
    type: Boolean,
    default: true,
  },
  showSummary: Boolean,
  sumText: String,
  summaryMethod: Function,
  rowClassName: [String, Function],
  rowStyle: [Object, Function],
  cellClassName: [String, Function],
  cellStyle: [Object, Function],
  headerRowClassName: [String, Function],
  headerRowStyle: [Object, Function],
  headerCellClassName: [String, Function],
  headerCellStyle: [Object, Function],
  highlightCurrentRow: Boolean,
  currentRowKey: [String, Number],
  emptyText: String,
  expandRowKeys: Array,
  defaultExpandAll: Boolean,
  defaultSort: Object,
  tooltipEffect: String,
  spanMethod: Function,
  selectOnIndeterminate: {
    type: Boolean,
    default: true,
  },
  indent: {
    type: Number,
    default: 16,
  },
  treeProps: {
    type: Object,
    default() {
      return {
        hasChildren: "hasChildren",
        children: "children",
      };
    },
  },

  lazy: Boolean,

  load: Function,

});

const indexList = ref([]);

const selectionChange = (selection) => {
  proxy.$emit("selectionChange", selection);
};

const handleSelectionChange = () => {
  const selection = props.data.filter((item) => item["_checked"]);
  //   console.log(selection);
  selectionChange(selection);
};

const isNeedSelection = computed(() => {
  let result = proxy.$slots["default"]().filter((item) => {
    if (item && item.props && item.props.type === "selection") {
      return true;
    }
    return false;
  });
  return result.length > 0;
});
</script>
