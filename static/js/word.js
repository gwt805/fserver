function printword(data) {
    let index = 0; //data数组的下标
    let strIndex = 0; //data数组每一项字符串的下标
    let start = null; //开始的时间或是上一刻的时间
    let interval = 0; //上次操作与现在的时间间隔
    let change = 200; //每次变化的间隔
    let isDelete = false; //现在是否是删除状态
    function blink(time) {
        window.requestAnimationFrame(blink);
        if (!start) {
            start = time;
        }
        interval = time - start;
        if (interval > change) {
            //取出数组的某一个字符串
            let str = data[index];
            //不在删除状态
            if (!isDelete) {
                $("#quoteText").html(str.slice(0, ++strIndex));
                $("#quoteText .cursor").remove();
                $("<span class='cursor'>_</span>").appendTo("#quoteText");
            }
            else {
                $("#quoteText").html(str.slice(0, strIndex--));
            }
            start = time;
            if (strIndex == str.length) {
                isDelete = true;
                change = 200;
                start = time + 1000;
            }
            if (strIndex < 0) {
                isDelete = false;
                start = time + 200;
                index++;
            }
            if (index == data.length) {
                index = 0;
            }
        }
    }
    window.requestAnimationFrame(blink);
}