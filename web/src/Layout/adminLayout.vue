<template>
  <div class="layout-global-css">
    <div class="layout-top" ref="layoutTopRef">
      <div class="layout-top-logo" v-if="anime">医学图像分割系统</div>

      <div class="layout-top-main">
        <div style="display: flex; align-items: center">
          <div class="layout-top-main-sw" @click="menu_show_hide" title="菜单">
            <el-icon v-show="anime" class="show-hide-anime-css"
              ><Switch
            /></el-icon>
            <el-icon v-show="!anime" class="show-hide-anime-css"
              ><Switch
            /></el-icon>
          </div>
          <div title="返回">
            <el-icon class="show-hide-anime-css" @click="router_back"
              ><Back
            /></el-icon>
          </div>

          <!--页面名称-->
          <div
            style="margin-left: 1rem"
            :title="route.name"
            class="layout-top-route-name"
          >
            {{ route.name }}
          </div>

          <!--标签栏-->
          <many-tab ref="tabsRef"></many-tab>
        </div>

        <div class="layout-top-main-user-div">
          <div class="layout-top-main-user-text">
            {{ datas.name }}
          </div>
        </div>
      </div>
    </div>

    <div class="layout-middle">
      <div class="layout-side" ref="layoutSideRef">
        <div class="layout-side-div">
          <div v-for="(item, index) in datas.menu" class="layout-side-item">
            <!--一级菜单-有二级菜单的 -->
            <div
              v-if="item.link == '' && item.level <= datas.level"
              class="layout-side-item-A"
              @click="menu_click(index)"
            >
              <!-- <img class="layout-side-icon" :src="item.icon" alt="" /> -->
              <img v-if="item.icon" class="layout-side-icon" :src="item.icon" alt="" />
              <div class="layout-side-title">{{ item.title }}</div>
            </div>

            <!--一级菜单-无二级菜单的-->
            <router-link
              v-else
              :to="item.link"
              class="layout-side-item-A"
              v-if="item.level <= datas.level"
            >
              <!-- <img class="layout-side-icon" :src="item.icon" alt="" /> -->
              <img v-if="item.icon" class="layout-side-icon" :src="item.icon" alt="" />
              <div class="layout-side-title">{{ item.title }}</div>
            </router-link>

            <!--二级菜单-->
            <div v-show="item.show" class="layout-side-item-B">
              <div v-for="(B_item, B_index) in item.children">
                <router-link
                  :to="B_item.link"
                  class="layout-side-item-C"
                  v-if="B_item.level <= datas.level"
                >
                  <!-- <img class="layout-side-icon" :src="B_item.icon" alt="" /> -->
                  <img v-if="B_item.icon" class="layout-side-icon" :src="B_item.icon" alt="" />
                  <div class="layout-side-title">{{ B_item.title }}</div>
                </router-link>
              </div>
            </div>
          </div>

          <div class="layout-side-item">
            <div class="layout-side-item-A" @click="outlog">
              <!-- <img class="layout-side-icon" src="/icon/tuichu.png" alt="" /> -->
              <!-- 已删除图标元素 -->
              <!-- <i class="remixicon-css layout-side-icon" style="font-size: 2rem"
                >&#xEEDB;</i
              > -->

              <div class="layout-side-title" style="">退出系统</div>
            </div>
          </div>
        </div>
      </div>

      <div class="layout_main">
        <div class="pages-web-main-css">
          <router-view />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import {
  Menu as IconMenu,
  Switch,
  SwitchButton,
  Back,
} from "@element-plus/icons-vue";

import manyTab from "./manyTab.vue";

const router = useRouter();
const route = useRoute();

//标签栏元素
const tabsRef = ref(null);

const layoutSideRef = ref(null);
const layoutTopRef = ref(null);

const anime = ref(true);
const middleWidth = ref("12.5rem"); //菜单栏宽度
const mainWidth = ref("100%"); //页面操作区宽度

const mainHeight = ref("94vh"); //操作区高度
const mainTopHeight = ref("3.4375rem"); //顶部导航栏高度

const datas = reactive({
  name: localStorage.getItem("name", ""),
  level: localStorage.getItem("level", "0"),
  menu: [
    {
      title: "系统介绍", //标签名
      icon: "", //icon图标路径，"/icon/系统介绍.png"
      level: 1, //可见等级
      link: "/describe", //转跳连接  有子菜单默认为空
      show: false, //是否显示子菜单 固定项为false
      children: [
        //子菜单
      ],
    },

    {
      title: "用户管理", //标签名
      icon: "", //icon图标路径，"/icon/yonghuguanli.png"
      level: 10, //可见等级
      link: "/admin/user_list", //转跳连接  有子菜单默认为空
      show: false, //是否显示子菜单 固定项为false
      children: [
        //子菜单
      ],
    },
    {
      title: "个人信息", //标签名
      icon: "", //icon图标路径，"/icon/个人信息.png"
      level: 1, //可见等级
      link: "/admin/user/info", //转跳连接  有子菜单默认为空
      show: false, //是否显示子菜单 固定项为false
      children: [
        //子菜单
      ],
    },
    {
      title: "医学图像分割", //标签名
      icon: "", //icon图标路径,"/icon/检测.png"
      level: 1, //可见等级
      link: "/admin/detection", //转跳连接  有子菜单默认为空
      show: false, //是否显示子菜单 固定项为false
      children: [
        //子菜单
      ],
    },

    {
      title: "历史记录", //标签名
      icon: "", //icon图标路径,"/icon/图片.png"
      level: 1, //可见等级
      link: "/admin/detection_list", //转跳连接  有子菜单默认为空
      show: false, //是否显示子菜单 固定项为false
      children: [
        //子菜单
      ],
    },

    {
      title: "数据集申请管理", //标签名
      icon: "", //icon图标路径,"/icon/数据集申请管理.png"
      level: 1, //可见等级
      link: "/admin/data_add_ask_list", //转跳连接  有子菜单默认为空
      show: false, //是否显示子菜单 固定项为false
      children: [
        //子菜单
      ],
    },
  ],
});

//侧边栏css
const bgCss = reactive({
  top_bg: "rgb(248, 249, 253)",
  top_text: "black",

  menu_bg: "rgb(84,92,100)", //菜单背景颜色
  text: "#fff", //菜单文字颜色
  hover_color: "rgb(66,72,78)", //鼠标移动到菜单上的颜色
  exact_active: "rgb(59,64,69)", //路由所在的颜色
});

//二级菜单切换
const menu_click = (index) => {
  datas.menu[index].show = !datas.menu[index].show;
};

//切换菜单栏背景颜色
const menu_bg_sw = (e) => {
  switch (e) {
    case "样式1": {
      bgCss.top_bg = "rgb(248, 249, 253)";
      bgCss.top_text = "black";
      bgCss.menu_bg = "rgb(84,92,100)";
      bgCss.text = "#fff";
      bgCss.hover_color = "rgb(66,72,78)";
      bgCss.exact_active = "rgb(59,64,69)";
      break;
    }
    case "样式2": {
      bgCss.top_bg = "#F7F9F9";
      bgCss.top_text = "black";
      bgCss.menu_bg = "#E3E3E3";
      bgCss.text = "black";
      bgCss.hover_color = "#C2C2C2";
      bgCss.exact_active = "#8A8D90";
      break;
    }
    case "样式3": {
      bgCss.top_bg = "#f5f5f5";
      bgCss.top_text = "black";
      bgCss.menu_bg = "#2F2F2F";
      bgCss.text = "#F7F7F7";
      bgCss.hover_color = "#8D8D8D";
      bgCss.exact_active = "#8D8D8D";
      break;
    }
    case "样式4": {
      bgCss.top_bg = "rgb(253,253,253)";
      bgCss.top_text = "black";
      bgCss.menu_bg = "rgb(0,25,45)";
      bgCss.text = "#F7F7F7";
      bgCss.hover_color = "#8D8D8D";
      bgCss.exact_active = "#8D8D8D";
      break;
    }

    default: {
      break;
    }
  }
};

//退出登录
const outlog = () => {
  localStorage.clear();
  router.push("/admin/login");
};

// 判断是否有上一页
function hasBack() {
  if (window.history.state.back) {
    //可以返回上一页
    return true;
  } else {
    //没有上一页
    return false;
  }
}

//菜单返回
const router_back = () => {
  if (hasBack()) {
    router.back();
  } else {
    // console.log("没有上一页");
  }
};

//侧边导航栏显示或隐藏方法
const menu_show_hide = () => {
  anime.value = !anime.value;

  if (anime.value) {
    //显示
    middleWidth.value = "12.5rem";
    mainWidth.value =
      document.documentElement.clientWidth -
      layoutSideRef.value.offsetWidth +
      "px";
  } else {
    //不显示
    middleWidth.value = "0rem";
    mainWidth.value = document.documentElement.clientWidth + "px";
  }
};

//页面宽度初始化
const webInit = () => {
  middleWidth.value = "12.5rem";

  //显示区宽度 减去 侧边栏宽度  = 操作区宽度
  if (layoutSideRef.value) {
    mainWidth.value =
      document.documentElement.clientWidth -
      layoutSideRef.value.offsetWidth +
      "px";

    //显示区高度 减去 顶部高度  =  操作区高度
    mainHeight.value =
      document.documentElement.clientHeight -
      layoutTopRef.value.offsetHeight +
      "px";
  }
};

onMounted(() => {
  menu_bg_sw("样式4");
  webInit();
  setTimeout(() => {
    webInit();
  }, 100);

  window.addEventListener("resize", function () {
    webInit();
    setTimeout(() => {
      webInit();
    }, 100);
  });
});
</script>

<style scoped>
.layout-global-css {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  min-height: 100vh;
}
.layout-top {
  min-height: v-bind(mainTopHeight);
  background-color: v-bind("bgCss.top_bg");
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 1.25rem;
  overflow: hidden;
  color: v-bind("bgCss.top_text");
}

.layout-top-logo {
  width: v-bind(middleWidth);
  min-width: v-bind(middleWidth);
  max-width: v-bind(middleWidth);

  height: 100%;
  background-color: v-bind("bgCss.menu_bg");
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1.25rem;
  font-weight: bold;
  color: v-bind("bgCss.text");
}

.layout-top-main {
  width: v-bind(mainWidth);
  min-width: v-bind(mainWidth);
  max-width: v-bind(mainWidth);
  display: flex;
  height: 98%;
  justify-content: space-between;
  border-bottom: 0.0625rem solid rgba(165, 165, 165, 0.26);
}

.layout-top-main-sw {
  margin-left: 0rem;
  width: 3rem;
  display: flex;
  justify-content: center;
  align-items: center;
}

.show-hide-anime-css {
  width: 2rem;
  height: 2rem;
  font-size: 1.5rem;
  border-radius: 0.5rem;
  cursor: pointer;
  background-color: rgba(0, 225, 255, 0.151);
  animation: rotateButton 0.5s linear; /* 应用旋转动画 */
}

/* 定义旋转动画 */
@keyframes rotateButton {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.layout-middle {
  display: flex;
  flex: 1;
}

.layout-side {
  width: v-bind(middleWidth);
  min-width: v-bind(middleWidth);
  height: v-bind(mainHeight);
  /* background-color: rgb(84, 92, 100); */
  background-color: v-bind("bgCss.menu_bg");
  font-size: 1rem;
  display: flex;
  flex-direction: column;
}

.layout_main {
  display: flex;
  width: v-bind(mainWidth);
  height: v-bind(mainHeight);
  border-radius: 0.3125rem;
  flex-direction: column;
  overflow: auto;
  border-radius: 1rem;
  /* background-color: rgb(249,249,249); */
  background-color: rgb(233, 233, 233);
  /* background-color: v-bind("bgCss.top_bg");  */
}

.layout-top-route-name {
  margin-left: 1rem;
  margin-right: 1rem;
  font-size: 0.875rem;
  color: #353535;
  width: 5rem;

  overflow: hidden; /*让过长的文字变成...*/
  white-space: nowrap; /*文字不换行 */
  text-overflow: ellipsis; /*让超长文字变成 ...*/
}

.pages-web-main-css {
  height: 100%;
  margin: 0.75rem 1rem 1rem 1rem;
  padding: 1rem;
  border: 0.125rem solid black;
  border-radius: 1rem;
  background-color: rgb(255, 255, 255);
  overflow: auto;
}

.layout-top-main-user-div {
  display: flex;
  /* justify-content: center; */
  align-items: center;
  margin-right: 1rem;
}

.layout-top-main-user-text {
  font-size: 1rem;
  width: 8rem;
  max-width: 8rem;
  min-width: 8rem;
  overflow: hidden; /*让过长的文字变成...*/
  white-space: nowrap; /*文字不换行 */
  text-overflow: ellipsis; /*让超长文字变成 ...*/
}

.layout-side-item {
  display: flex;
  flex-direction: column;
  color: v-bind("bgCss.text");
  text-shadow: 0.5px 0.5px 0 rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.layout-side-item-A {
  padding-top: 1rem;
  padding-bottom: 1rem;
  padding-left: 1rem;
  display: flex;
  align-items: center;

  color: v-bind("bgCss.text");
  font-size: 1rem;

  flex-wrap: wrap;
}

.layout-side-item-A > a {
  color: v-bind("bgCss.text");
}

.layout-side-item-B {
  animation-name: fadeInDown;
  animation-duration: 0.8s;
  animation-fill-mode: forwards;
  height: 0;

  overflow: hidden;
}

.layout-side-item-C {
  display: flex;
  align-items: center;
  padding-top: 1rem;
  padding-bottom: 1rem;
  padding-left: 2rem;
  color: v-bind("bgCss.text");
  font-size: 1rem;
  flex-wrap: wrap;
}

.layout-side-icon {
  width: 1.5rem;
  height: 1.5rem;
  margin-right: 1rem;
}

.layout-side-item-C > .layout-side-title {
  display: flex;
  justify-content: center;
  align-items: center;
  /* font-size: 0.875rem; */
  font-size: 1rem;
}

.layout-side-div::-webkit-scrollbar-track {
  /* background: rgb(255, 255, 255); */
  background-color: v-bind("bgCss.menu_bg");

  margin-top: 0.5rem;
  margin-bottom: 0.5rem;
  margin-right: 0.125rem;
  border-radius: 1rem;
}

.layout-side-div::-webkit-scrollbar-thumb {
  background-color: v-bind("bgCss.hover_color");
  border-radius: 0.3125rem;
}

.layout-side-div::-webkit-scrollbar {
  width: 0.5rem;
}

@keyframes fadeInDown {
  0% {
    height: 0;
  }

  100% {
    height: 100%;
  }
}

.layout-side-div {
  overflow: auto;
}

.layout-side-item-A:hover {
  background-color: v-bind("bgCss.hover_color");
}

.layout-side-item-C:hover {
  background-color: v-bind("bgCss.hover_color");
}

.layout-side-div::-webkit-scrollbar-thumb:hover {
  background-color: v-bind("bgCss.hover_color");
}

.router-link-exact-active {
  background-color: v-bind("bgCss.exact_active");
}

.v-enter-from {
  transform: translateY(-3.125rem);
  opacity: 0;
}

.v-enter-active {
  transition: 0.5s ease;
}
.v-enter-to {
  transform: translateY(0px);
  opacity: 1;
}

.v-leave-from {
  transform: translateY(0px);
  opacity: 1;
}
.v-leave-active {
  transition: 0.5s ease;
}

.v-leave-to {
  transform: translateY(50px);
  opacity: 0;
}

.pages-web-main-css::-webkit-scrollbar-track {
  background: rgb(255, 255, 255);
  margin-top: 0.5rem;
  margin-bottom: 0.5rem;
  margin-right: 0.125rem;
  border-radius: 1rem;
}

.pages-web-main-css::-webkit-scrollbar-thumb {
  background: rgb(83, 175, 223);
  border-radius: 0.3125rem;
}

.pages-web-main-css::-webkit-scrollbar-thumb:hover {
  background: rgb(55, 115, 148);
}

.pages-web-main-css::-webkit-scrollbar {
  width: 0.5rem;
}
</style>
