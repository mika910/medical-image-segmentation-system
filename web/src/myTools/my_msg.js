//自定义消息提醒
import DOMPurify from 'dompurify'; //防止xss攻击




let myMsgDiv = null
let myMsgtimeoutId = null;
//弹出消息弹窗
export function myMsgSend(options) {
  let { title, txt, imgLink,pageLink, msgType, site,timeout } = options;
  /*
  title为标题
  txt 为提示内容
  imgLink 为图片连接
  pageLink 点击转跳页面链接   不填写则不转跳
  msgType 消息类型   default/success/error/  三种类型 默认default为空即可
  site    出现位置   top/bottom/center           //顶部或顶部出现
  timeout  消失时间 默认3000毫秒
  */
  if (myMsgtimeoutId) {
    clearTimeout(myMsgtimeoutId);
  }

  if (myMsgDiv) {
    // 如果消息弹窗已存在，关闭或删除它
    document.body.removeChild(myMsgDiv);
    myMsgDiv = null;
  }

  if (!title){
    title = "消息提醒"
  }

  if (!txt){
    txt = ""
  }

  if (!imgLink) {
    imgLink = "/icon/prompt.png"
  }
  switch (msgType) {
    case "default":
      msgType = "msg-type-default"
      break;
    case "success":
      msgType = "msg-type-success"
      break;
    case "error":
      msgType = "msg-type-error"
      break;
    default:
      msgType = "msg-type-default"
  }

  switch (site) {
    case "top":
      site = "msg-site-top"
      break;
    case "bottom":
      site = "msg-site-bottom"
      break;
    case "center":
      site = "msg-site-center"
      break;
    default:
      site = "msg-site-bottom"
  }

  if (!timeout){
    timeout = 3000
  }

  if (pageLink){
    pageLink = `href="${pageLink}" `
  }

  myMsgDiv = document.createElement("div");
  // 设置该 div 的 innerHTML 为你提供的 HTML 结构字符串
  let userHtml = `
    <div class="msg-diolog-div ${msgType} ${site}">
      <div class="msg-diolog-main-div">
        <a class="msg-diolog-text-content-div" ${pageLink}>
          <div class="msg-diolog-text-title">
            ${title}
          </div>
          <div class="msg-diolog-text-txt">
          ${txt}
          </div>
        </a>
        <div class="msg-diolog-img-div">
          <img
            src="${imgLink}"
            alt="图片加载错误"
            class="msg-diolog-img"
          />
        </div>
      </div>
    </div>
  `;
  // 清理用户输入的内容，以确保安全
  var cleanHtml = DOMPurify.sanitize(userHtml);
  // 设置该 div 的 innerHTML 为清理后的内容
  myMsgDiv.innerHTML = cleanHtml;
  // 将该 div 元素添加到 body 中
  document.body.appendChild(myMsgDiv);
  myMsgtimeoutId = setTimeout(function () {
    //判断提示框 是否已经被删除了  未被删除的就需要删除提示框
    if (myMsgDiv) {
      document.body.removeChild(myMsgDiv);
      myMsgDiv = null
    }
    myMsgtimeoutId = null
  }, timeout);

}
/*
使用方法
  myMsgSend({
    title: "消息提示",
    txt: "有新的消息来了<br>点击查看",
    imgLink:
      "https://img.zetab.top/api/img?id=7dc13fc5-bf44-4e26-b321-be68a160944f.jpg",
    pageLink: "/",
    msgType: "success",
    site: "bottom",
    timeout: 10000,
  });
*/

