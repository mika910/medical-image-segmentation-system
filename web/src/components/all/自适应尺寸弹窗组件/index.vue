<template>
  <el-dialog
    v-model="props.dialogState"
    :title="props.title"
    :style="diologSize"
    :close-on-click-modal="false"
    :show-close="false"
    :modal="false"
    :append-to-body="true"
    draggable
  >


    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogClose" style="margin-right: 0.75rem"
          >关闭</el-button
        >
        <el-button type="primary" @click="submit" :disabled="shake_obj.submit">
            提交
          </el-button>
      </span>
    </template>
  </el-dialog>
</template>
<script setup>
import { reactive, computed } from "vue";

const emits = defineEmits([
  //设置可以调用的父组件方法
  "dataLoad",
  "close",
]);
const props = defineProps({
  //接受父组件传值
  dialogState: Boolean, //弹窗开 关
  title:String
});

const datas = reactive({

});

const form = reactive({});
//表单初始化方法 可以通过 ref.value.formInit()  来传入数据给组件
const formInit = (row) => {};


const dialogClose = () => {
  emits("dataLoad");
  emits("close");
};

//弹窗尺寸调整
const diologSize = computed(() => {
  let deviceWidth =
    window.innerWidth ||
    document.documentElement.clientWidth ||
    document.body.clientWidth;
  if (deviceWidth > 765) {
    //pc端
    return {
      width: "30vw",
      maxHeight: "95vh",
      overflow: "auto",
    };
  } else {
    //移动端
    return {
      width: "90%",
    };
  }
});

defineExpose({ formInit });

/*
使用方法

<组件名
    ref="ref变量"
    :dialogState="弹窗开关布尔类型变量"
    @close="关闭弹窗的方法"
/>
const ref变量 = ref(null)

const 打开弹窗的方法 = (row) => {
  弹窗开关布尔类型变量= true;
  ref变量.value.formInit(row);
};

const 关闭弹窗的方法 = () => {
  弹窗开关布尔类型变量 = false;
};


*/


</script>
<style scoped></style>
