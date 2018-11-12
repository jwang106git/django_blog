const nativeShare = new NativeShare();
const shareData = {
    title: '分享标题',
    desc: '',
    // 如果是微信该link的域名必须要在微信后台配置的安全域名之内的。
    link: 'http://39.107.64.193:3',
    icon: "{% static 'img/social/head.png' %}",
    // 不要过于依赖以下两个回调，很多浏览器是不支持的
    success: function () {
        console.log("success")
    },
    fail: function () {
        console.log("fail")
    }
};
nativeShare.setShareData(shareData);

function call(command) {
    try {
        nativeShare.call(command)
    } catch (err) {
        // 如果不支持，你可以在这里做降级处理
        alert(err.message)
        // console.log("err.message")
    }
};

