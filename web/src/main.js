import { createApp } from 'vue'
import App from './App.vue'
import route from './route'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import locale from 'element-plus/lib/locale/lang/zh-cn' //加载中文包
import componentsPlugin from './components/componentsPlugin';
import './myCss/my.css';
import {
    createPinia
} from 'pinia'
import {
    useCounterStore
}
from './stores/counter.js'
import './route/qxcl.js'

//加载状态数据
const pinia = createPinia()
const myStore = useCounterStore(pinia);
myStore.initLoad();


const app =createApp(App)
app.use(pinia)
app.use(route)
app.use(ElementPlus, {
    locale
})
app.use(componentsPlugin);



app.mount('#app')


