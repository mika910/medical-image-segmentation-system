<template>
  <el-upload
    :action="''"
    :on-success="onSuccess"
    :on-error="onError"
    :headers="headers"
    :drag="props.drag"
  >
    <el-button>上传图片</el-button>
  </el-upload>
</template>
<script setup>
//图片上传模块


import { myMsgSend } from "@/myTools/my_msg";

const emits = defineEmits([
  //设置可以调用的父组件方法
  "success",
]);
const props = defineProps({
  //接受父组件传值
  drag: Boolean,
});
const headers = {
  Authorization: localStorage.getItem("token"),
};
const onSuccess = (res) => {
  if (res.code == 200) {
    myMsgSend({
      txt: res.msg,
      msgType: "success",
      site:"center"
    });
    emits("success", res.data);
  } else {
    myMsgSend({
      txt: res.msg,
      msgType: "error",
      site:"center"
    });
  }
};
const onError = (res) => {
  console.log(res);
  myMsgSend({
    txt: "上传图片失败",
    msgType: "error",
    site:"center"
  });
};

/*
使用方法 

在main.js中
import MyImgUpdate from './components/ImgUpdata.vue'
const app =createApp(App)
app.component("my-imgup",MyImgUpdate)      //将本组件导入全局
app.mount('#app')


使用
<template>
<my-imgup @success="scc"/>        //使用上面导入的组件名称 来调用组件
</template>


import { ref } from "vue";
const r = ref("图片地址")
const scc= (res)=>{
    r.value = res
}
*/
</script>
<style scoped></style>
