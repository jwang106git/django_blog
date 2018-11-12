function WordsFollowMouseDOM(hintwords) {
    document.addEventListener("mousemove", function (e) {
        var myhint = document.getElementById("slider-hint");
        myhint.style.left = e.clientX - 18 + "px";
        myhint.style.top = e.clientY + 15 + "px";
        switch (hintwords) {
            case 1:
                myhint.innerHTML = "人生苦短 我用python";
                myhint.style.display = 'block';
                break;
            case 2:
                myhint.innerHTML = "代码改变世界";
                myhint.style.display = 'block';
                break;
            case 3:
                myhint.innerHTML = "技术成就人生";
                myhint.style.display = 'block';
                break;
            case 4:
                myhint.innerHTML = "stay hungry";
                myhint.style.display = 'block';
                break;
            case 5:
                myhint.innerHTML = "stay foolish";
                myhint.style.display = 'block';
                break;
            default:
                myhint.innerHTML = "";
                myhint.style.display = 'none';
                break;
        }
    });
}


$("#slider-1").hover(function () {
    WordsFollowMouseDOM(1);
    }, function () {
    WordsFollowMouseDOM(6);
});

$("#slider-2").hover(function () {
    WordsFollowMouseDOM(2);
    }, function () {
    WordsFollowMouseDOM(6);
});

$("#slider-3").hover(function () {
    WordsFollowMouseDOM(3);
    }, function () {
    WordsFollowMouseDOM(6);
});

$("#slider-4").hover(function () {
    WordsFollowMouseDOM(4);
    }, function () {
    WordsFollowMouseDOM(6);
});

$("#slider-5").hover(function () {
    WordsFollowMouseDOM(5);
    }, function () {
    WordsFollowMouseDOM(6);
});