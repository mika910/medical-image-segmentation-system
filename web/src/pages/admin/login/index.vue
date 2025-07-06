<template>
  <div class="global">
    <div class="login_frame">
      <div class="title">登录</div>
      <form class="form">
        <div>
          <input
            type="text"
            v-model="form.username"
            placeholder="请输入用户名"
          />
        </div>
        <div>
          <input
            type="password"
            v-model="form.password"
            placeholder="请输入密码"
          />
        </div>
      </form>
      <button class="button_group" @click="login">登录</button>

      <div class="bottom-links">
        <router-link to="/admin/register" class="register_point">注册</router-link>
        <router-link to="/admin/forgot-password" class="forgot-password">忘记密码</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive } from "vue"; // 删除ref导入
import { useRoute, useRouter } from "vue-router";
import { ElMessage, ElMessageBox } from "element-plus";
import { api_Login } from "@/api/api";

const Router = useRouter();

// 删除验证码相关变量

const form = reactive({
  username: "",
  password: "",
  // 删除captcha字段
});

// 删除刷新验证码方法

//登录
const login = () => {
  // 验证表单
  if (!form.username) {
    ElMessage.error('请输入用户名');
    return;
  }
  if (!form.password) {
    ElMessage.error('请输入密码');
    return;
  }
  // 删除验证码验证
  
  // 调用登录API
  api_Login(form).then((res) => {
    if (res.data.code === 200) {
      ElMessage({
        message: res.data.msg,
        type: "success",
      });
      localStorage.setItem("token", res.data.data.token);
      localStorage.setItem("name", res.data.data.name);
      localStorage.setItem("level", res.data.data.level);
      localStorage.setItem("username", res.data.data.username);

      Router.push("/describe");
    } else {
      ElMessage.error(res.data.msg);
      // 删除刷新验证码代码
    }
  });
};
</script>

<style scoped>
.global {
  width: 100%;
  height: 100%;
  background-color: #e8f4fc; /* 修改背景颜色aliceblue */
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: auto;
}
.login_frame {
  width: 35rem;
  height: 42.5rem;
  background-color: rgb(255, 255, 255);
  border-radius: 15px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.title {
  font-size: 2rem;
  font-weight: 500;
  margin-top: 5rem;
}
.form {
  margin-top: 3.125rem;
}

.form div {
  margin-bottom: 2.5rem;
}

.form input {
  width: 18.75rem;
  height: 3.75rem;
  border-radius: 0.312rem;
  border: 0px;
  box-shadow: 0px 0px 2px rgb(146, 146, 146);
  font-size: 1.5rem;
  text-indent:1.5625rem;
  color: #333;
  caret-color: rgb(146, 146, 146);
}

/* 删除验证码相关样式 */

.form input:focus {
  outline: none;
  border: 0px;
  box-shadow: 0px 0px 2px rgb(16, 104, 236);
}
.button_group {
  width: 18.75rem;
  height: 2.1875rem;
  font-size: 1.25rem;
  border: none;
  border-radius: 2.1875rem;
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: 600;
  background-color: black;
  color: #fff;
}

.button_group:hover {
  cursor: pointer;
}

.button_group:active {
  transform: scale(0.98);
}

/* 底部链接样式 */
.bottom-links {
  width: 18.75rem;
  margin-top: 2rem;
  display: flex;
  justify-content: space-between;
}

.register_point, .forgot-password {
  color: #1066ec;
  text-decoration: none;
}

.register_point:hover, .forgot-password:hover {
  text-decoration: underline;
}
</style>
