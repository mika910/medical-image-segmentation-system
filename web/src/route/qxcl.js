//权限处理

import router from './index'

// 修改权限控制逻辑
router.beforeEach((to, from, next) => {
    let isLogin = localStorage.getItem('token')
    if (isLogin) {
        next()
    } else {
        if (to.path == '/login' || to.path == '/admin/login' || 
            to.path == '/admin/register' || to.path == '/admin/forgot-password' || 
            to.path == '/m/login') {
            next(); // 登录、注册、忘记密码页面，放行
        } else {
            let ok = adminLoginverify(to.path)
            if (ok) {
                //需要转跳到管理员登录页面
                next({
                    path: '/admin/login'
                })
            } else {
                //默认放行
                next()
            }
        }
    }
})
//验证是否转跳到管理员登录页面
function adminLoginverify(path) {
    let paths = path.split("/")
    if (paths.length <= 1) {
        return false
    }
    if (paths[1] == "admin") {
        //需要转跳到管理员登录页面
        return true
    }
    return false
}