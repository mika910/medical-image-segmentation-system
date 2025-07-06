//时间格式化
export const formatTime = (inputTimeString) => {
    const dateObject = new Date(inputTimeString);
    const year = dateObject.getFullYear();
    const month = (dateObject.getMonth() + 1).toString().padStart(2, "0");
    const day = dateObject.getDate().toString().padStart(2, "0");
    const hours = dateObject.getHours().toString().padStart(2, "0");
    const minutes = dateObject.getMinutes().toString().padStart(2, "0");
    const seconds = dateObject.getSeconds().toString().padStart(2, "0");
    if (year == 1) {
        return "";
    }
    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
};