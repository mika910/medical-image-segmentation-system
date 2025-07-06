<template>
    <img :src="props.mid" alt="图片">
</template>
<script setup>

const props = defineProps({
  //接受父组件传值
  mid: String,
});

/*
使用方法
在main.js中
import MyImgShow from './components/ImgShow.vue'
const app =createApp(App)
app.component("my-img",MyImgShow)    //将本组件导入全局
app.mount('#app')

使用
<my-img :mid="r"></my-img>      //传入图片的mid即可

*/

</script>
<style>
</style>
