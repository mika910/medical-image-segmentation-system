import {
    defineStore
} from 'pinia'

export const useCounterStore = defineStore('counter', {
    state: () => {
        return {
            device: "电脑端"
        }
    },
    actions: {
        initLoad() {
            //初始化时加载数据
            let device = localStorage.getItem("device")
            if (device) {
                this.device = device
            } else {
                this.device = "电脑端"
            }
        },
        deviceSwitch() {
            //设备切换
            if (this.device == '电脑端') {
                this.device = '移动端'
            } else {
                this.device = '电脑端'
            }
            localStorage.setItem("device", this.device)
        },
    },
})