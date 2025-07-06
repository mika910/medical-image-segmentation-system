<template>
  <div class="global">
    <div class="login_frame">
      <div class="logo">
        <img src="/login_icon.jpg" alt="" srcset="" />
      </div>
      <div class="title">注册</div>
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

        <div>
          <input
            type="password"
            v-model="form.pwd"
            placeholder="请确认密码"
          />
        </div>

      </form>
      <button class="button_group" @click="register">注册</button>


      <router-link to="/admin/login" class="register_point">登录</router-link>
    </div>
  </div>
</template>

<script setup>
import { reactive } from "vue";
import { useRoute, useRouter } from "vue-router";
import { ElMessage ,ElMessageBox} from "element-plus";
import { api_Register } from "@/api/api";

const Router = useRouter();


const form = reactive({
  username: "",
  password: "",
  pwd:""
});
//注册
const register = () => {
  if (form.password != form.pwd ){
    ElMessage.error("确认密码与输入密码不一致");
    return
  }

  api_Register(form).then((res) => {
    if (res.data.code === 200) {
      ElMessage({
        message: res.data.msg,
        type: "success",
      });
      Router.push("/admin/login");
    } else {
      ElMessage.error(res.data.msg);
    }
  });
};
</script>

<style scoped>
.global {
  width: 100%;
  height: 100%;
  background-color: aliceblue;
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

.logo {
  margin-top: 5rem;
  margin-bottom: 2.5rem;
}
.logo img {
  width: 6.25rem;
  height: 6.25rem;
  border-radius: 50%;
}
.title {
  font-size: 2rem;
  font-weight: 500;
}
.form {
  margin-top: 3.125rem;
}

.form div {
  margin-bottom: 2.5rem;
}

.form input {
  width: 18.75rem;
  height: 2.75rem;
  border-radius: 0.312rem;
  border: 0px;
  box-shadow: 0px 0px 2px rgb(146, 146, 146);
  font-size: 1.5rem;
  text-indent:1.5625rem;
  color: #333;
  caret-color: rgb(146, 146, 146);
}
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

.register_point {
  width: 18.75rem;
  margin-top: 3.125rem;
}
</style>
