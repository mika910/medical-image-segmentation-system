import axios from 'axios'
import router from "./../route"

//后端接口

export const APIbaseUrl = 'http://127.0.0.1:8000/api'





axios.defaults.baseURL = APIbaseUrl
axios.interceptors.request.use((config) => { //请求之前的处理
    config.headers.Authorization = localStorage.getItem('token')
    return config //必须返回config
})

axios.interceptors.response.use((config) => { //请求之后的处理
    if (config.data.code == 401) {
        let currentPath = window.location.pathname;
        let result = loginPathVerify(currentPath)
        router.push(result + "/login")
    }
    return config
})

//查询需要转跳到那种登录页面
function loginPathVerify(path) {
    let paths = path.split("/")
    if (paths.length <= 1) {
        return ''
    }
    if (paths[1] == "admin") {
        //需要转跳到管理员登录页面
        return '/admin'
    }
    return '/admin'
}


export function api_Login(dic) {
    //登录
    return axios.post("/user/login", dic)
}

//注册
export function api_Register(dic) {
    return axios.post("/user/register", dic)
}


//查询个人信息
export function api_user_info_get(dic) {
    return axios.get("/user/info", {
        params: dic
    })
}
//修改个人信息
export function api_user_info_put(dic) {
    return axios.put("/user/info", dic)
}

//个人头像上传
export const userInfoImgLinkPost = APIbaseUrl + "/user/img"
//个人头像获取
export const userInfoImgLinkGet = APIbaseUrl + "/user/img?img="



//用户管理
export function api_admin_user_list_get(dic) {
    return axios.get("/admin/user", {
        params: dic
    })
}
export function api_admin_user_list_one_get(dic) {
    return axios.get("/admin/user/one", {
        params: dic
    })
}
export function api_admin_user_list_post(dic) {
    return axios.post("/admin/user", dic)
}
export function api_admin_user_list_put(dic) {
    return axios.put("/admin/user", dic)
}
export function api_admin_user_list_del(dic) {
    return axios.delete("/admin/user", {
        params: dic
    })
}




//检测管理

//进行检测
export function api_detection_post(dic) {
    return axios.post("/detection", dic)
}
//可以使用的模型和数据集
export function api_detection_model_list_get(dic) {
    return axios.get("/detection/model", {
        params: dic
    })
}


//历史检测列表
export function api_detection_list_get(dic) {
    return axios.get("/detection_list", {
        params: dic
    })
}

//历史检测数据删除
export function api_detection_list_del(dic) {
    return axios.delete("/detection_list", {
        params: dic
    })
}

//检测结果获取
export const detectionImgGet = APIbaseUrl + "/detection/img?mid="




//数据集添加请求管理
export function api_data_add_ask_list_get(dic) {
    return axios.get("/data_add_ask_list", {
        params: dic
    })
}
export function api_data_add_ask_one_get(dic) {
    return axios.get("/data_add_ask_one", {
        params: dic
    })
}
export function api_data_add_ask_list_post(dic) {
    return axios.post("/data_add_ask_list", dic)
}
export function api_data_add_ask_list_put(dic) {
    return axios.put("/data_add_ask_list", dic)
}
export function api_data_add_ask_list_del(dic) {
    return axios.delete("/data_add_ask_list", {
        params: dic
    })
}


// 验证用户身份
function api_verify_identity(dic) {
    return axios.post("/user/verify-identity", dic)
}

// 重置密码
function api_reset_password(dic) {
    return axios.post("/user/reset-password", dic)
}

// 导出
export {
    api_verify_identity,
    api_reset_password
}