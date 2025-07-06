<template>
  <div class="many-tab-main-div" v-if="showState">
    <div class="many-tab-div" ref="manyTabDivRef">
      <div
        v-for="(item, index) in datas.tabList"
        @click="switch_page_func(item, index)"
        :class="'many-tab-content-div ' + selectStyleIs(item, index)"
      >
        <div class="many-tab-content-div-title" :title="item.title">
          {{ item.title }}
        </div>

        <span
          class="remixicon-css"
          title="关闭"
          @click.stop="del_func(item, index)"
        >
          &#xEB99;
        </span>
      </div>
    </div>
  </div>
</template>
<script setup>
import { onMounted, reactive, watch, ref } from "vue";
import { useRouter, useRoute } from "vue-router";
const router = useRouter();
const route = useRoute();

//多标签组件
const emits = defineEmits([
  //设置可以调用的父组件方法
]);
const props = defineProps({
  //接受父组件传值
});
//初始化方法
const formInit = () => {};

const manyTabDivRef = ref(null);
const showWidth = ref("30vw"); //模块宽度

const datas = reactive({
  tabList: [],
});

//是否在这个页面
const selectStyleIs = (item, index) => {
  if (route.name == item.title) {
    return "many-tab-content-div-hit";
  }
  return "";
};

//转跳到点击的页面
const switch_page_func = (item, index) => {
  router.push(datas.tabList[index].link);
};

//从列表中删除元素
const del_func = (item, index) => {
  datas.tabList.splice(index, 1);

  //判断是不是当前页面 是当前页面 就转跳到这个元素的前一个页面  不是就不变
  if (route.name == item.title) {
    if (index <= 0) {
      //没有页面可以转跳了
      //判断后面还有没有元素 有就向后转跳
      if (datas.tabList.length != 0) {
        router.push(datas.tabList[0].link);
      }
    } else {
      //转跳到这个元素的前一个页面
      router.push(datas.tabList[index - 1].link);
    }
  }
};

//加入这个页面到标签组中
const add_func = () => {
  //检查是否重复
  let repeat = false; // true为重复  false为未重复
  let index = -1;

  for (let i = 0; i < datas.tabList.length; i++) {
    let item = datas.tabList[i];
    if (route.name == item.title) {
      //重复了
      repeat = true;
      index = i;
      break;
    }
  }

  //同一个页面 就更新储存的列表数据
  if (repeat) {
    datas.tabList[index] = { title: route.name, link: route.path };
    return;
  }

  //不重复 添加到标签列表中
  let dic = { title: route.name, link: route.path };
  datas.tabList.push(dic);
};
//开启监控
watch(
  () => route.name,
  (count, prevCount) => {
    add_func();
    setTimeout(() => {
      scrollPlaceSet();
    }, 100);
  }
);

//新标签需要转移进度条到最后   点击某一个标签 滚动条需要完全显示 这个标签
const scrollPlaceSet = () => {
  //长度除以列表数量 获取每一个元素的长度  然后根据index进行定位
  if (!manyTabDivRef.value) {
    return;
  }

  let oneWidth = manyTabDivRef.value.scrollWidth / datas.tabList.length; //单个宽度

  //获取索引
  let index = 0;
  for (let i = 0; i < datas.tabList.length; i++) {
    if (datas.tabList[i].title == route.name) {
      index = i;
    }
  }

  let w = oneWidth * (index + 1);
  w = w - manyTabDivRef.value.clientWidth;
  manyTabDivRef.value.scroll({
    top: 0,
    left: w,
    behavior: "smooth",
  });
};

//手机端不显示这个模块
const showState = ref(true);
const showStateSet = () => {
  //同时设置这个模块的宽度
  if (window.innerWidth >= 1920) {
    //100%缩放率
    showWidth.value = "55vw";
  }
  if (window.innerWidth < 1745) {
    //100%缩放率
    showWidth.value = "50vw";
  }
  if (window.innerWidth < 1536) {
    //150%缩放率
    showWidth.value = "45vw";
  }
  if (window.innerWidth < 1280) {
    //175%缩放率
    showWidth.value = "35vw";
  }

  if (window.innerWidth > 765) {
    //电脑
    showState.value = true;
  } else {
    //手机
    showState.value = false;
  }
};

onMounted(() => {
  add_func();
  showStateSet();

  window.addEventListener("resize", showStateSet);
  window.addEventListener("orientationchange", showStateSet); //屏幕发生转动时 触发的函数
});

//外部可调用方法
defineExpose({ formInit });
</script>
<style scoped>
.many-tab-main-div {
  max-width: v-bind(showWidth);

  height: 100%;
  align-items: center;
  margin-left: 1rem;
  margin-right: 1rem;
  font-size: 0.875rem;
  color: #353535;
  user-select: none; /*元素禁止选中*/
}

.many-tab-div {
  display: flex;
  align-items: center;
  height: 100%;

  overflow-x: auto; /* 显示横向滚动条 */
  overflow-y: hidden; /* 隐藏竖向滚动条 */
}

.many-tab-content-div {
  white-space: nowrap;
  line-height: 1;
  display: flex;
  align-items: center;
  padding: 0.25rem 0.75rem 0.25rem 0.75rem;
  margin: 0.25rem;
  box-shadow: 0 0 0.125rem rgba(95, 95, 95, 0.555);
  background-color: rgb(255, 255, 255);
  border-radius: 0.125rem;
  cursor: pointer;
}

@media (max-width: 1098px) {
  /*适配1080p下百分之175%缩放率*/
  .many-tab-content-div {
    padding: 0.1rem 0.75rem 0.1rem 0.75rem;
    margin: 0.25rem;
  }
}

.many-tab-content-div:hover {
  transform: scale(0.98);
  background-color: rgba(223, 222, 222, 0.418);
  cursor: pointer;
}

.many-tab-content-div-hit {
  box-shadow: 0 0 0.125rem rgba(64, 158, 255);
  color: rgb(64, 158, 255);
}

.many-tab-content-div-title {
  width: 6rem;
  overflow: hidden; /*让过长的文字变成...*/
  white-space: nowrap; /*文字不换行 */
  text-overflow: ellipsis; /*让超长文字变成 ...*/
}

.remixicon-css {
  margin-left: 0.5rem;
  font-size: 1.25rem;
}

.remixicon-css:hover {
  color: rgb(243, 98, 98);
}

/*滚动条样式*/
.many-tab-div::-webkit-scrollbar-track {
  background: rgb(255, 255, 255);
}

.many-tab-div::-webkit-scrollbar-thumb {
  background: rgba(88, 88, 88, 0.418);
  border-radius: 0.325rem;
}

.many-tab-div::-webkit-scrollbar-thumb:hover {
  background: rgb(77, 164, 211);
  cursor: pointer;
}
.many-tab-div::-webkit-scrollbar-thumb:active {
  background: rgb(68, 125, 156);
}

.many-tab-div::-webkit-scrollbar {
  height: 0.25rem;
}
</style>
