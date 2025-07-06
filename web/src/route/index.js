import {
  createRouter,
  createWebHistory,
} from "vue-router";
import adminLayout from "@/Layout/adminLayout.vue"



const routes = [{
    path: "",
    name: "管理后台",
    component: adminLayout,
    children: [

      {
        path: "",
        name: "主页",
        component: () => import("@/pages/admin/home/index.vue")
      },

      {
        path: "/describe",
        name: "系统介绍",
        component: () => import("@/pages/admin/describe/index.vue")
      },

      {
        path: "/admin/user/info",
        name: "个人信息",
        component: () => import("@/pages/admin/user/info.vue")
      },
      {
        path: "/admin/user_list",
        name: "用户管理",
        component: () => import("@/pages/admin/user_list/index.vue")
      },
      {
        path: "/admin/user_list/add",
        name: "添加用户",
        component: () => import("@/pages/admin/user_list/add.vue")
      },
      {
        path: "/admin/user_list/put/:id",
        name: "修改用户信息",
        component: () => import("@/pages/admin/user_list/put.vue")
      },


      {
        path: "/admin/detection",
        name: "数据集检测",
        component: () => import("@/pages/admin/detection/index.vue")
      },


      {
        path: "/admin/detection_list",
        name: "检测历史管理",
        component: () => import("@/pages/admin/detection_list/index.vue")
      },

  




      {
        path: "/admin/data_add_ask_list",
        name: "数据集申请管理",
        component: () => import("@/pages/admin/data_add_ask_list/index.vue")
      },

      {
        path: "/admin/data_add_ask_list/add",
        name: "数据集-提交新的申请",
        component: () => import("@/pages/admin/data_add_ask_list/add.vue")
      },
      {
        path: "/admin/data_add_ask_list/put/:id",
        name: "数据集-数据修改",
        component: () => import("@/pages/admin/data_add_ask_list/put.vue")
      },
      {
        path: "/admin/data_add_ask_list/show/:id",
        name: "数据集-申请查看",
        component: () => import("@/pages/admin/data_add_ask_list/show.vue")
      },





    ]

  },
  {
    path: "/admin/login",
    name: "登录",
    component: () => import("@/pages/admin/login/index.vue")
  },
  {
    path: "/admin/register", 
    name: "注册",
    component: () => import("@/pages/admin/register/index.vue")
  },
  {
    path: "/admin/forgot-password", 
    name: "忘记密码",
    component: () => import("@/pages/admin/forgot-password/index.vue")
  },
  {
    path: "/:catchAll(.*)", //设置找不到地址的网页的指向页面
    name: "404",
    component: () => import("@/404/index.vue")
  }

];






const route = createRouter({
  //创建路由
  //   history: createWebHashHistory(), //哈希模式
  history: createWebHistory(),
  routes: routes,
});

export default route; //进行输出