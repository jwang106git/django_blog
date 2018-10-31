!function (L, N) {
    var O = window.jQuery || {}, e = N, G = window.document, i = "data-bind-login", g = N, h = "login-box",
        v = "login-mark";
    L.loginBox = L.loginBox ? L.loginBox : {}, O === window.jQuery ? ($selectorAll = function (e) {
        var t = [];
        return O(e).each(function (e, n) {
            t.push(n)
        }), t
    }, function (e) {
        return O(e).get(0)
    }, e = !0) : $selectorAll = function (e) {
        return document.querySelectorAll(e)
    }, O.LOGIN = O.LOGIN || {}, O.LOGIN.isInit = !0, L.loginBox.scope = O.LOGIN;
    var r = function () {
        O.LOGIN.docDom && (G.body.appendChild(O.LOGIN.oMark), G.body.appendChild(O.LOGIN.docDom), O.LOGIN.appendBox.isCreate = !0)
    }, o = L.loginBox.login = function (e) {
        var n, t, o, i, r, a, d, l, s, c, u, f, m, p, I = {
            domain: (e = e || {}).domain || "csdn.net",
            isRedirect: e.isRedirect || !document.createElement("iframe").sandbox,
            iframeName: e.iframeName || "passport_iframe",
            isIframe: e.isIframe === N || e.isIframe,
            frameWidth: e.frameWidth,
            frameHeight: e.frameHeight,
            append: e.append || "#passport-box",
            from: e.from,
            service: e.service,
            loginService: e.loginService,
            initRun: e.initRun || null,
            before: e.before || null,
            after: e.after || null,
            finished: e.finished || null
        };
        if (!I.loginService) throw new Error("login 处理 control错误！");
        return O.LOGIN.options = I, O.LOGIN.runStatus = !0, I.isIframe && (I.initRun && (O.LOGIN.runStatus = I.initRun()), O.LOGIN.runStatus && (O.LOGIN.runStatus = (i = (n = I).domain, r = n.from, a = n.append, d = n.service, l = n.isRedirect, s = n.loginService, c = n.isIframe, u = n.iframeName, f = n.frameWidth, m = n.frameHeight, (p = document.createElement("div")).className = v, G.domain = i || "csdn.net", r && (s = s + "?from=" + r, d && (s = s + "&service=" + d)), console.debug("处理service:", s), g = document.createDocumentFragment(), t = '<iframe  width="' + f + '" height="' + m + '" name="' + u + '" src="' + s + '" frameborder="0" scrolling="no"></iframe>', (o = document.createElement("div")).id = a.replace(/[#\.]/, ""), o.className = h, O.LOGIN.appendBox = o, O.LOGIN.markDom = p, c && (O.LOGIN.appendBox.innerHTML = t, O.LOGIN.iframeName = u, O.LOGIN.iframeDom = O.LOGIN.appendBox.firstElementChild || O.LOGIN.appendBox.firstChild), g && (g.appendChild(o), O.LOGIN.oMark = p, O.LOGIN.docDom = g), O.LOGIN.isRedirect = l, !0))), L.LOGIN
    }, a = function (e) {
        return O.LOGIN.runStatus = O.LOGIN.options[e] ? O.LOGIN.options[e]() : O.LOGIN.runStatus, O.LOGIN.runStatus
    }, d = function (e, n, t) {
        window.addEventListener ? e.addEventListener(n, t, !1) : e.attachEvent("on" + n, t)
    }, l = function (e, n) {
        var t;
        return t = "all" === e ? "none" : "block", "start" === e && (t = "block"), O.LOGIN.appendBox && (O.LOGIN.markDom.style.display = t, O.LOGIN.appendBox.style.display = t, O.LOGIN.appendBox.status = "block" === t || !(O.LOGIN.runStatus = !0)), O.LOGIN.appendBox.status && n && n(), L.LOGIN
    }, s = function () {
        O.LOGIN.oMark && !O.LOGIN.oMark.isClick && (d(O.LOGIN.oMark, "click", function (e) {
            var n = window.event || e;
            if (O.LOGIN.appendBox.status) return l("all"), n.cancelBubble ? n.cancelBubble = !0 : n.stopPropagation(), !1
        }), O.LOGIN.oMark.isClick = !0)
    };
    L.loginBox.close = function () {
        return O.LOGIN.appendBox.status && l("all"), L.LOGIN
    }, L.loginBox.show = function () {
        !O.LOGIN.appendBox.isCreate && r(), O.LOGIN.appendBox.status || (l("start"), s())
    };
    L.loginBox.support = function () {
        return L.LOGIN.isRedirect
    };
    var c, n = function () {
        var e, n, t;
        e = G.head, n = e.firstElementChild || e.firstChild, (t = document.createElement("style")).innerText = ".login-box{position: fixed;display: none;left: 50%;top: 50%;z-index: 10000;-webkit-transform: translate(-50%, -50%);-ms-transform: translate(-50%, -50%);-o-transform: translate(-50%, -50%);-moz-transform: translate(-50%, -50%);transform: translate(-50%, -50%);background-color: #fff;}.login-mark{position: fixed;top: 0;left: 0;z-index: 9999;background-color: rgba(0, 0, 0, 0.5);width: 100%;height: 100%;display: none;}", e.insertBefore(t, n), function () {
            O.LOGIN.loginBtn = $selectorAll("[data-bind-login=true]");
            var e, n, t = function (e) {
                var n = window.event || e, t = "true" === this.getAttribute(i), o = this.href;
                if (!O.LOGIN.runStatus && t) return console.error("开启loginbox失败!"), !1;
                !1 === O.LOGIN.isRedirect ? !0 === t && (O.LOGIN.options.isIframe && (!O.LOGIN.appendBox.isCreate && r(), a("before") && l(N, function () {
                    a("after")
                }), s()), n.cancelBubble ? n.cancelBubble = !0 : n.stopPropagation(), n.returnValue ? n.returnValue = !1 : n.preventDefault()) : o || (G.location.href = O.LOGIN.options.loginService)
            }, o = 0;
            if (!O.LOGIN.loginBtn || O.LOGIN.loginBtn.length <= 0) return;
            for (; O.LOGIN.loginBtn[o];) e = o, n = O.LOGIN.loginBtn[e], d(n, "click", t), o++
        }(), O.LOGIN.isInit && o({
            domain: "csdn.net",
            isIframe: !0,
            frameWidth: 400,
            frameHeight: 600,
            append: "#passportbox",
            from: window.location.href,
            loginService: "https://passport.csdn.net/account/loginbox"
        })
    }, t = function (e) {
        var n, t, o, i;
        document.addEventListener ? ~["complete", "loaded", "interactive"].indexOf(document.readyState) ? setTimeout(function () {
            e && e()
        }, 0) : (c = function () {
            document.removeEventListener("DOMContentLoaded", c, !1), e()
        }, document.addEventListener("DOMContentLoaded", c, !1)) : document.attachEvent && (n = e, t = !1, o = function () {
            t || (t = !0, n && n())
        }, (i = function () {
            try {
                G.documentElement.doScroll("left")
            } catch (e) {
                return void setTimeout(i, 50)
            }
            o()
        })(), G.onreadystatechange = function () {
            "complete" === G.readyState && (G.onreadystatechange = null, o())
        })
    };
    _ready = function () {
        e && O(function () {
            n()
        }) || t(n)
    }, _ready()
}(window.csdn = window.csdn || {}, void 0);