//选择去程航班时的展示
var gobtn = document.getElementById('gobtn');//去程选择按钮
var nav_first = document.getElementsByClassName('nav0')[0];
var nav_second = document.getElementsByClassName('nav2')[0];
gobtn.addEventListener('click', function () {
    nav_first.className = "nav0";
    nav_second.className = "nav2";
    gobtn.style.backgroundColor = 'black';
    backbtn.style.backgroundColor = '';
    showbodys.className = 'show-body2';
    showbodyf.className = 'show-body0';
});
var acity = document.getElementsByClassName('citySelect')[0];//出发地
var bcity = document.getElementsByClassName('citySelect1')[0];//目的地
var time0 = document.getElementsByClassName('time0')[0];//去程时间
var time2 = document.getElementsByClassName('time2')[0];//返程时间
//选择返程航班时的展示
var backbtn = document.getElementById('backbtn');//返程选择按钮
var showbodyf = document.getElementsByClassName('show-body0')[0];//去程的航班展示
var showbodys = document.getElementsByClassName('show-body2')[0];//返程的航班展示
backbtn.addEventListener('click', function () {
    nav_second.className = "nav0";
    nav_first.className = "nav2";
    backbtn.style.backgroundColor = 'black';
    gobtn.style.backgroundColor = '';
    showbodys.className = 'show-body0';
    showbodyf.className = 'show-body2';
});
function check(){
    for(let i=0;i<city_first.length;i++)
    {
        if(city_first[i].value=="城市名"||city_second[i].value=="城市名"||time_first[i].value=="")
        {
            return 1;
        }
    }
    return 0;
}
// 查询时所触发的事件
var discover_btn = document.getElementsByClassName('btn')[0];//查询按钮
var search_animation = document.getElementsByClassName('ifa')[0];//查询时的动画
var alarm = document.getElementsByClassName('xiaoxi')[0];//搜索信息未完整提示内容
var information = document.getElementsByClassName('tishi')[0];//搜索信息未完整提示框
discover_btn.addEventListener('click', function () {
    package();//调用多程数据打包函数
    if (st == 1 && (acity.value == '城市名' || bcity.value == '城市名' || time0.value == '')) {
        alarm.innerHTML = '请把搜索信息填写完整';
        information.className = 'tishi2';
    }
    else if (st == 2 && (acity.value == '城市名' || bcity.value == '城市名' || time0.value == '' || time2.value == '')) {
        alarm.innerHTML = '请把搜索信息填写完整';
        information.className = 'tishi2';
    }
    else if (acity.value == bcity.value && st != 3) {
        alarm.innerHTML = '出发地和目的地相同啦';
        information.className = 'tishi2';
    }
    else if(check()&&st==3)
    {
        alarm.innerHTML = '请把搜索信息填写完整';
    }
    else {
        alarm.innerHTML = '';
        information.className = 'tishi';
        cover.style.height = document.body.clientHeight + 'px';
        cover.className = 'cover2';
        search_animation.className = 'ifa2';
        setTimeout(function () {
            cover.className = 'cover';
            search_animation.className = 'ifa';//计算动画时间，时间到将其关闭
            reqfirst();//发送ajax请求获取数据
            refound();//数据请求完成，添加事件
        }, 2000);
    }
})
// 查询出来的航班，为他们添上监听事件，为后续判断是否勾选做准备
var order1, order2, radio, radio2;
function refound() {
    radio = document.getElementsByClassName('radio');
    for (let i = 0; i < radio.length - 1; i++) {
        radio[i].addEventListener("click", function () {
            order1 = 1;
        })
    }
    if (st == 2) {
        radio2 = document.getElementsByClassName('radio2');
        for (let i = 0; i < radio.length - 1; i++) {
            radio2[i].addEventListener("click", function () {
                order2 = 1;
            })
        }
    }
}
//购买告知
var hidden = document.getElementsByClassName('cha')[0];
var alarm_buy = document.getElementsByClassName('jingbao')[0];
var inform = document.getElementsByClassName('tixing')[0];
var cover = document.getElementsByClassName('cover')[0];//遮罩层
inform.addEventListener('click', function () {
    alarm_buy.className = 'jingbao2';
    cover.style.height = document.body.clientHeight + 'px';
    cover.className = 'cover2';
})
hidden.addEventListener('click', function () {
    alarm_buy.className = 'jingbao';
    cover.style.height = document.body.clientHeight + 'px';
    cover.className = 'cover';
})
//优先条件排序
var btn_go = document.getElementsByClassName('but');//去程优先条件按钮数组
var btn_back = document.getElementsByClassName('but2');//返程优先条件按钮数组
//去程条件排序
for (let k = 0; k < btn_go.length; k++) {
    btn_go[k].addEventListener('click', function () {
        for (let j = 0; j < btn_go.length; j++) {
            btn_go[j].style.backgroundColor = 'powderblue';
        }
        this.style.backgroundColor = 'darkgray';
        console.log(k);
        if (k == 0) {
            for (let i = 0; i < arr2.length; i++) {
                str = arr2[i] + ',g';
                str2 = arr2[i] + ',j';
                out += "<div" + " " + "class=" + "xinxi" + ">" +
                    "<div" + " " + "class=" + "tab" + ">" +
                    "<table" + " " + "border=" + "1px" + ">" +
                    "<tr" + " " + "class=" + "tr1" + ">" + "<td" + ">航空公司</td>" +
                    "<td>航班</td>" +
                    "<td>机型</td>" +
                    "<td>出发时间</td>" +
                    "<td>抵达时间</td>" +
                    "<td>余票</td>" + "<td>公务舱</td>" + "<td>经济舱</td>" + "</tr>" +
                    "<tr" + " " + "class=" + "tr2" + "><td>" + arr2[i][1] + "</td>" +
                    "<td>" + arr2[i][2] + "</td>" +
                    "<td>" + arr2[i][3] + "</td>" +
                    "<td>" + arr2[i][4] + "</td>" +
                    "<td>" + arr2[i][5] + "</td>" +
                    "<td>" + arr2[i][10] + "</td>" +
                    "<td>" + arr2[i][9] + `<input type="radio" name="a" class="radio" value="${str}">` + "</td>" +
                    "<td>" + arr2[i][8] + `<input type="radio" name="a" class="radio" value="${str2}">` + "</td>" +
                    "</table>" +
                    "</div>" +
                    "</div>"
            }
            if (arr.length == 0) {
                showbodyf.innerHTML = "<span>" + "没有航班了呦" + "<p>" + "<img" + " " + "src=" + "../static/s-other/1(1).png" + ">" + "</span>";
            }
            else {
                showbodyf.innerHTML = out;
                refound();//数据请求完成，添加事件
            }
            out = "";
        }
        if (k == 1) {
            for (let i = 0; i < arr3.length; i++) {
                str = arr3[i] + ',g';
                str2 = arr3[i] + ',j';
                out += "<div" + " " + "class=" + "xinxi" + ">" +
                    "<div" + " " + "class=" + "tab" + ">" +
                    "<table" + " " + "border=" + "1px" + ">" +
                    "<tr" + " " + "class=" + "tr1" + ">" + "<td" + ">航空公司</td>" +
                    "<td>航班</td>" +
                    "<td>机型</td>" +
                    "<td>出发时间</td>" +
                    "<td>抵达时间</td>" +
                    "<td>余票</td>" + "<td>公务舱</td>" + "<td>经济舱</td>" + "</tr>" +
                    "<tr" + " " + "class=" + "tr2" + "><td>" + arr3[i][1] + "</td>" +
                    "<td>" + arr3[i][2] + "</td>" +
                    "<td>" + arr3[i][3] + "</td>" +
                    "<td>" + arr3[i][4] + "</td>" +
                    "<td>" + arr3[i][5] + "</td>" +
                    "<td>" + arr3[i][10] + "</td>" +
                    "<td>" + arr3[i][9] + `<input type="radio" name="a" class="radio" value="${str}">` + "</td>" +
                    "<td>" + arr3[i][8] + `<input type="radio" name="a" class="radio" value="${str2}">` + "</td>" +
                    "</table>" +
                    "</div>" +
                    "</div>"
            }
            if (arr.length == 0) {
                showbodyf.innerHTML = "<span>" + "没有航班了呦" + "<p>" + "<img" + " " + "src=" + "../static/s-other/1(1).png" + ">" + "</span>";
            }
            else {
                showbodyf.innerHTML = out;
                refound();//数据请求完成，添加事件
            }
            out = "";
        }
        if (k == 2) {
            for (let i = 0; i < arr4.length; i++) {
                str = arr4[i] + ',g';
                str2 = arr4[i] + ',j';
                out += "<div" + " " + "class=" + "xinxi" + ">" +
                    "<div" + " " + "class=" + "tab" + ">" +
                    "<table" + " " + "border=" + "1px" + ">" +
                    "<tr" + " " + "class=" + "tr1" + ">" + "<td" + ">航空公司</td>" +
                    "<td>航班</td>" +
                    "<td>机型</td>" +
                    "<td>出发时间</td>" +
                    "<td>抵达时间</td>" +
                    "<td>余票</td>" + "<td>公务舱</td>" + "<td>经济舱</td>" + "</tr>" +
                    "<tr" + " " + "class=" + "tr2" + "><td>" + arr4[i][1] + "</td>" +
                    "<td>" + arr4[i][2] + "</td>" +
                    "<td>" + arr4[i][3] + "</td>" +
                    "<td>" + arr4[i][4] + "</td>" +
                    "<td>" + arr4[i][5] + "</td>" +
                    "<td>" + arr4[i][10] + "</td>" +
                    "<td>" + arr4[i][9] + `<input type="radio" name="a" class="radio" value="${str}">` + "</td>" +
                    "<td>" + arr4[i][8] + `<input type="radio" name="a" class="radio" value="${str2}">` + "</td>" +
                    "</table>" +
                    "</div>" +
                    "</div>"
            }
            if (arr.length == 0) {
                showbodyf.innerHTML = "<span>" + "没有航班了呦" + "<p>" + "<img" + " " + "src=" + "../static/s-other/1(1).png" + ">" + "</span>";
            }
            else {
                showbodyf.innerHTML = out;
                refound();//数据请求完成，添加事件
            }
            out = "";
        }
        if (k == 3) {
            for (let i = 0; i < arr5.length; i++) {
                str = arr5[i] + ',g';
                str2 = arr5[i] + ',j';
                out += "<div" + " " + "class=" + "xinxi" + ">" +
                    "<div" + " " + "class=" + "tab" + ">" +
                    "<table" + " " + "border=" + "1px" + ">" +
                    "<tr" + " " + "class=" + "tr1" + ">" + "<td" + ">航空公司</td>" +
                    "<td>航班</td>" +
                    "<td>机型</td>" +
                    "<td>出发时间</td>" +
                    "<td>抵达时间</td>" +
                    "<td>余票</td>" + "<td>公务舱</td>" + "<td>经济舱</td>" + "</tr>" +
                    "<tr" + " " + "class=" + "tr2" + "><td>" + arr5[i][1] + "</td>" +
                    "<td>" + arr5[i][2] + "</td>" +
                    "<td>" + arr5[i][3] + "</td>" +
                    "<td>" + arr5[i][4] + "</td>" +
                    "<td>" + arr5[i][5] + "</td>" +
                    "<td>" + arr5[i][10] + "</td>" +
                    "<td>" + arr5[i][9] + `<input type="radio" name="a" class="radio" value="${str}">` + "</td>" +
                    "<td>" + arr5[i][8] + `<input type="radio" name="a" class="radio" value="${str2}">` + "</td>" +
                    "</table>" +
                    "</div>" +
                    "</div>"
            }
            if (arr.length == 0) {
                showbodyf.innerHTML = "<span>" + "没有航班了呦" + "<p>" + "<img" + " " + "src=" + "../static/s-other/1(1).png" + ">" + "</span>";
            }
            else {
                showbodyf.innerHTML = out;
                refound();//数据请求完成，添加事件
            }
            out = "";
        }
    })
}
// 返程条件排序
for (let k = 0; k < btn_back.length; k++) {
    btn_back[k].addEventListener('click', function () {
        for (let j = 0; j < btn_back.length; j++) {
            btn_back[j].style.backgroundColor = 'powderblue';
        }
        this.style.backgroundColor = 'darkgray';
        console.log(k);
        if (k == 0) {
            for (let i = 0; i < brr2.length; i++) {
                str = brr2[i] + ',g';
                str2 = brr2[i] + ',j';
                out += "<div" + " " + "class=" + "xinxi" + ">" +
                    "<div" + " " + "class=" + "tab" + ">" +
                    "<table" + " " + "border=" + "1px" + ">" +
                    "<tr" + " " + "class=" + "tr1" + ">" + "<td" + ">航空公司</td>" +
                    "<td>航班</td>" +
                    "<td>机型</td>" +
                    "<td>出发时间</td>" +
                    "<td>抵达时间</td>" +
                    "<td>余票</td>" + "<td>公务舱</td>" + "<td>经济舱</td>" + "</tr>" +
                    "<tr" + " " + "class=" + "tr2" + "><td>" + brr2[i][1] + "</td>" +
                    "<td>" + brr2[i][2] + "</td>" +
                    "<td>" + brr2[i][3] + "</td>" +
                    "<td>" + brr2[i][4] + "</td>" +
                    "<td>" + brr2[i][5] + "</td>" +
                    "<td>" + brr2[i][10] + "</td>" +
                    "<td>" + brr2[i][9] + `<input type="radio" name="b" class="radio2" value="${str}">` + "</td>" +
                    "<td>" + brr2[i][8] + `<input type="radio" name="b" class="radio2" value="${str2}">` + "</td>" +
                    "</table>" +
                    "</div>" +
                    "</div>"
            }
            if (brr.length == 0) {
                showbodys.innerHTML = "<span>" + "没有航班了呦" + "<p>" + "<img" + " " + "src=" + "../static/s-other/1(1).png" + ">" + "</span>";
            }
            else {
                showbodys.innerHTML = out2;
                refound();//数据请求完成，添加事件
            }
            out2 = "";
        }
        if (k == 1) {
            for (let i = 0; i < brr3.length; i++) {
                str = brr3[i] + ',g';
                str2 = brr3[i] + ',j';
                out += "<div" + " " + "class=" + "xinxi" + ">" +
                    "<div" + " " + "class=" + "tab" + ">" +
                    "<table" + " " + "border=" + "1px" + ">" +
                    "<tr" + " " + "class=" + "tr1" + ">" + "<td" + ">航空公司</td>" +
                    "<td>航班</td>" +
                    "<td>机型</td>" +
                    "<td>出发时间</td>" +
                    "<td>抵达时间</td>" +
                    "<td>余票</td>" + "<td>公务舱</td>" + "<td>经济舱</td>" + "</tr>" +
                    "<tr" + " " + "class=" + "tr2" + "><td>" + brr3[i][1] + "</td>" +
                    "<td>" + brr3[i][2] + "</td>" +
                    "<td>" + brr3[i][3] + "</td>" +
                    "<td>" + brr3[i][4] + "</td>" +
                    "<td>" + brr3[i][5] + "</td>" +
                    "<td>" + brr3[i][10] + "</td>" +
                    "<td>" + brr3[i][9] + `<input type="radio" name="b" class="radio2" value="${str}">` + "</td>" +
                    "<td>" + brr3[i][8] + `<input type="radio" name="b" class="radio2" value="${str2}">` + "</td>" +
                    "</table>" +
                    "</div>" +
                    "</div>"
            }
            if (brr.length == 0) {
                showbodys.innerHTML = "<span>" + "没有航班了呦" + "<p>" + "<img" + " " + "src=" + "../static/s-other/1(1).png" + ">" + "</span>";
            }
            else {
                showbodys.innerHTML = out2;
                refound();//数据请求完成，添加事件
            }
            out2 = "";
        }
        if (k == 2) {
            for (let i = 0; i < brr4.length; i++) {
                str = brr4[i] + ',g';
                str2 = brr4[i] + ',j';
                out += "<div" + " " + "class=" + "xinxi" + ">" +
                    "<div" + " " + "class=" + "tab" + ">" +
                    "<table" + " " + "border=" + "1px" + ">" +
                    "<tr" + " " + "class=" + "tr1" + ">" + "<td" + ">航空公司</td>" +
                    "<td>航班</td>" +
                    "<td>机型</td>" +
                    "<td>出发时间</td>" +
                    "<td>抵达时间</td>" +
                    "<td>余票</td>" + "<td>公务舱</td>" + "<td>经济舱</td>" + "</tr>" +
                    "<tr" + " " + "class=" + "tr2" + "><td>" + brr4[i][1] + "</td>" +
                    "<td>" + brr4[i][2] + "</td>" +
                    "<td>" + brr4[i][3] + "</td>" +
                    "<td>" + brr4[i][4] + "</td>" +
                    "<td>" + brr4[i][5] + "</td>" +
                    "<td>" + brr4[i][10] + "</td>" +
                    "<td>" + brr4[i][9] + `<input type="radio" name="b" class="radio2" value="${str}">` + "</td>" +
                    "<td>" + brr4[i][8] + `<input type="radio" name="b" class="radio2" value="${str2}">` + "</td>" +
                    "</table>" +
                    "</div>" +
                    "</div>"
            }
            if (brr.length == 0) {
                showbodys.innerHTML = "<span>" + "没有航班了呦" + "<p>" + "<img" + " " + "src=" + "../static/s-other/1(1).png" + ">" + "</span>";
            }
            else {
                showbodys.innerHTML = out2;
                refound();//数据请求完成，添加事件
            }
            out2 = "";
        }
        if (k == 3) {
            for (let i = 0; i < brr5.length; i++) {
                str = brr5[i] + ',g';
                str2 = brr5[i] + ',j'
                out2 += "<div" + " " + "class=" + "xinxi" + ">" +
                    "<div" + " " + "class=" + "tab" + ">" +
                    "<table" + " " + "border=" + "1px" + ">" +
                    "<tr" + " " + "class=" + "tr1" + ">" + "<td" + ">航空公司</td>" +
                    "<td>航班</td>" +
                    "<td>机型</td>" +
                    "<td>出发时间</td>" +
                    "<td>抵达时间</td>" +
                    "<td>余票</td>" + "<td>公务舱</td>" + "<td>经济舱</td>" + "</tr>" +
                    "<tr" + " " + "class=" + "tr2" + "><td>" + brr5[i][1] + "</td>" +
                    "<td>" + brr5[i][2] + "</td>" +
                    "<td>" + brr5[i][3] + "</td>" +
                    "<td>" + brr5[i][4] + "</td>" +
                    "<td>" + brr5[i][5] + "</td>" +
                    "<td>" + brr5[i][10] + "</td>" +
                    "<td>" + brr5[i][9] + `<input type="radio" name="b" class="radio2" value="${str}">` + "</td>" +
                    "<td>" + brr5[i][8] + `<input type="radio" name="b" class="radio2" value="${str2}">` + "</td>" +
                    "</div>" +
                    "</div>"
            }
            if (brr.length == 0) {
                showbodys.innerHTML = "<span>" + "没有航班了呦" + "<p>" + "<img" + " " + "src=" + "../static/s-other/1(1).png" + ">" + "</span>";
            }
            else {
                showbodys.innerHTML = out2;
                refound();//数据请求完成，添加事件
            }
            out2 = "";
        }
    })
}

//预订时判断用户是否已经勾选票
var nav_tishi = document.getElementsByClassName('nav_tishi')[0];
var nav_tishi3 = document.getElementsByClassName('nav_tishi3')[0];
var pay = document.getElementsByClassName('pay')[0];
pay.addEventListener('click', function () {
    if (order1 != 1 && (st == 1 || st == 3)) {
        nav_tishi3.innerText = '请选择机票';
        nav_tishi3.className = 'nav_tishi4';
    }
    if (order1 !== 1 && st == 2) {
        nav_tishi3.innerText = '请选择去程的机票';
        nav_tishi3.className = 'nav_tishi4';
    }
    if (order2 !== 1 && st == 2) {
        nav_tishi.innerText = '请选择返程的机票';
        nav_tishi.className = 'nav_tishi2';
    }
    if (order1 == 1 && (st == 1 || st == 3)) {
        nav_tishi3.className = 'nav_tishi3';
        settlement();
    }
    if (order1 == 1 && st == 2 & order2 == 1) {
        nav_tishi.className = 'nav_tishi';
        nav_tishi3.className = 'nav_tishi3';
        settlement();
    }
});
//发送用户选择的航班数据ajax
var cang, num = -1, go_data, back_data, go_radio, back_radio, send = [100];
function settlement() {
    go_radio = document.getElementsByName('a');
    back_radio = document.getElementsByName('b');
    if (st == 1) {
        for (let i = 0; i < go_radio.length; i++) {
            if (go_radio[i].checked) {
                go_data = go_radio[i].value;
                break;
            }
        }
        go_data = go_data.split(',');
        send = go_data;
        $.ajax(
            {
                url: '/index_ajax4',
                type: 'POST',
                data: { "table": JSON.stringify(send), "st": "1" },
                async: false,
                error: function (request) {
                    alert('hello-cuowu');
                },
                success: function (data) {
                    location.replace(data);
                }
            }
        )
    }
    if (st == 2) {
        for (let i = 0; i < go_radio.length; i++) {
            if (go_radio[i].checked) {
                go_data = go_radio[i].value;
                break;
            }
        }
        for (let i = 0; i < back_radio.length; i++) {
            if (back_radio[i].checked) {
                back_data = back_radio[i].value;
                break;
            }
        }
        go_data = go_data.split(',');
        back_data = back_data.split(',');
        send[0] = go_data;
        send[1] = back_data;
        $.ajax(
            {
                url: '/index_ajax4',
                type: 'POST',
                data: { "table": JSON.stringify(send), "st": "2" },
                async: false,
                error: function (request) {
                    alert('hello-cuowu');
                },
                success: function (data) {
                    location.replace(data);
                }
            }
        )
    }
    if (st == 3) {
        num++;//记录选啦几次
        for (let i = 0; i < go_radio.length; i++) {
            if (go_radio[i].checked) {
                go_data = go_radio[i].value;
                break;
            }
        }
        go_data = go_data.split(',');
        send = go_data;
        ////选的次数与预选航班数一致
        if (num == count) {
            $.ajax(
                {
                    url: '/index_ajax4',
                    type: 'POST',
                    data: { "table": JSON.stringify(send),"st": "3"},
                    async: false,
                    error: function (request) {
                        alert('hello-cuowu');
                    },
                    success: function (data) {
                      location.replace(data);
                    }
                })
        }
        else{
            $.ajax(
                {
                    url: '/index_ajax32',
                    type: 'POST',
                    data: { "table": JSON.stringify(send) },
                    async: false,
                    error: function (request) {
                        alert('hello-cuowu');
                    },
                    success: function (data) {
                        if (data['string'] === "0") {
                            showbodyf.innerHTML = "<span>" + "服务器正在更新" + "<p>" + "<img" + " " + "src=" + "../static/s-other/error.png" + ">" + "</span>";
                            arr = [], arr2 = [], arr3 = [], arr4 = [], arr5 = [];//清空数据
                        }
                        if (data['string'] === "1") {
                            showbodyf.innerHTML = "<span>" + "没有航班了呦" + "<p>" + "<img" + " " + "src=" + "../static/s-other/error.png" + ">" + "</span>";
                            arr = [], arr2 = [], arr3 = [], arr4 = [], arr5 = [];//清空数据
                        }
                        if (data['string'] === "2") {
                            arr = JSON.parse(data['common']);
                            arr2 = JSON.parse(data['go_sort']);
                            arr3 = JSON.parse(data['arrival_sort']);
                            arr4 = JSON.parse(data['First_class']);
                            arr5 = JSON.parse(data['economy_class']);
                            for (let i = 0; i < arr.length; i++) {
                                str = arr[i] + ',g';
                                str2 = arr[i] + ',j';
                                out += "<div" + " " + "class=" + "xinxi" + ">" +
                                    "<div" + " " + "class=" + "tab" + ">" +
                                    "<table" + " " + "border=" + "1px" + ">" +
                                    "<tr" + " " + "class=" + "tr1" + ">" + "<td" + ">航空公司</td>" +
                                    "<td>航班</td>" +
                                    "<td>机型</td>" +
                                    "<td>出发时间</td>" +
                                    "<td>抵达时间</td>" +
                                    "<td>余票</td>" + "<td>公务舱</td>" + "<td>经济舱</td>" + "</tr>" +
                                    "<tr" + " " + "class=" + "tr2" + "><td>" + arr[i][1] + "</td>" +
                                    "<td>" + arr[i][2] + "</td>" +
                                    "<td>" + arr[i][3] + "</td>" +
                                    "<td>" + arr[i][4] + "</td>" +
                                    "<td>" + arr[i][5] + "</td>" +
                                    "<td>" + arr[i][10] + "</td>" +
                                    "<td>" + arr[i][9] + `<input type="radio" name="a" class="radio" value="${str}">` + "</td>" +
                                    "<td>" + arr[i][8] + `<input type="radio" name="a" class="radio" value="${str2}">` + "</td>" +
                                    "</table>" +
                                    "</div>" +
                                    "</div>"
                            }
                            showbodyf.innerHTML = out;
                            pay.value = "选为第" + (num + 2) + "程";
                            refound();
                            out = "";//清空out数据
                        }
                    }
                }
            )
        }
    }
}
// 多程代码部分
var search_many = document.getElementsByClassName('search_many')[0];
var search_single = document.getElementsByClassName('search_single')[0];
var arrive_start = document.getElementsByClassName('arrive_start');
var arrive_end = document.getElementsByClassName('arrive_end');
var decline = document.getElementsByClassName('decline');
var addition = document.getElementsByClassName('addition')[0];
var trips = document.getElementsByClassName('trips');
var up = document.getElementsByClassName('up')[0];
// 改变单选，往返，多程状态
var single = document.getElementById("dan");
var double = document.getElementById("shuang");
var more = document.getElementById('duo');
var time_back = document.getElementsByClassName('time-end')[0];//返程时间
var show = document.getElementsByClassName('show-nav-span')[0];//往返与单程按钮切换
var show2 = document.getElementsByClassName('show-nav-span2')[0];
more.addEventListener('click', function () {
    search_many.className = "search_many2";
    st = 3;
    time_back.className = "time-end";
    show2.style.zIndex = 2
    show.style.zIndex = 1;
    pay.value = "选为第1程";
})
single.addEventListener('click', function () {
    time_back.className = "time-end";
    search_many.className = "search_many";
    st = 1;
    show2.style.zIndex = 2
    show.style.zIndex = 1;
    pay.value = "￥预订";
})
double.addEventListener('click', function () {
    time_back.className = "time-end2";
    search_many.className = "search_many";
    st = 2;
    show.style.zIndex = 2;
    show2.style.zIndex = 1;
    pay.value = "￥预订";
})
//addition是添加按钮，再加一程
addition.addEventListener('click', function () {
    search_many.appendChild(search_many.children[0].cloneNode(true));
    up.value = "︿";
    search_many.className = "search_many2";
    count += 1;
    time_first[count].value = "";
    city_first[count].value = "城市名";
    city_second[count].value = "城市名";
    var test = new Vcity.CitySelector({ input: 'city_first', site: count });
    var test = new Vcity.CitySelector({ input: 'city_second', site: count });
    decline[count].value = "第 " + (count + 1) + " 程";
    if(count==5){
        addition.className="hidden";
    }
})
// 将多程航班信息展示缩小按钮
var counter=0;
up.addEventListener('click', function () {
    counter++;
    if(counter%2==0)
    {
        up.value = "︿";
        search_many.className = "search_many2";
    }
    else{
        up.value = "    ﹀";
        search_many.className = "search_many3";
    }
})
//ajax请求数据获取
var arr = [], arr2 = [], arr3 = [], arr4 = [], arr5 = [];//去程
var brr = [], brr2 = [], brr3 = [], brr4 = [], brr5 = [];//返程
var out = "", out2 = "", st = 1;// 规定单程已经勾选 out展示去程，out2展示返程，模板字符串
var str, str2;//用于添加g,j;
// 针对单程和往返

//获取多程数据的数组
var city_first = document.getElementsByClassName('city_first');
var city_second = document.getElementsByClassName('city_second');
var time_first = document.getElementsByClassName('time_first');
//打包多程航班数据
var send_data = [], count = 0;//count 计算用户选了几程 ，send_data数组里的元素是 航班数据json对象
function package() {
    // for (let i = 0; i < city_first.length; i++) {
    //     send_data[i] = {
    //         "acity": city_first[i].value, "bcity": city_second[i].value, "adate": time_first[i].value
    //     }
    // }
    for (let i = 0; i < city_first.length; i++) {
        send_data[i] = [
            city_first[i].value, city_second[i].value, time_first[i].value
        ]
    }
}
// ajax请求数据
function reqfirst() {
    // 单程数据ajax
    if (st == 1) {
        $.ajax({
            type: 'post',
            url: '/index_ajax1',
            data: { "acity": acity.value, "bcity": bcity.value, "adate": time0.value },
            dataType: 'json',
            async: false,
            error: function (request) {
                alert('cuowu');
            },
            success: function (data) {
                if (data['string'] === "0") {
                    showbodyf.innerHTML = "<span>" + "服务器正在更新" + "<p>" + "<img" + " " + "src=" + "../static/s-other/error.png" + ">" + "</span>";
                    arr = [], arr2 = [], arr3 = [], arr4 = [], arr5 = [];//清空数据
                }
                if (data['string'] === "1") {
                    showbodyf.innerHTML = "<span>" + "没有航班了呦" + "<p>" + "<img" + " " + "src=" + "../static/s-other/error.png" + ">" + "</span>";
                    arr = [], arr2 = [], arr3 = [], arr4 = [], arr5 = [];//清空数据
                }
                if (data['string'] === "2") {
                    arr = JSON.parse(data['common']);
                    arr2 = JSON.parse(data['go_sort']);
                    arr3 = JSON.parse(data['arrival_sort']);
                    arr4 = JSON.parse(data['First_class']);
                    arr5 = JSON.parse(data['economy_class']);
                    for (let i = 0; i < arr.length; i++) {
                        str = arr[i] + ',g';
                        str2 = arr[i] + ',j';
                        out += "<div" + " " + "class=" + "xinxi" + ">" +
                            "<div" + " " + "class=" + "tab" + ">" +
                            "<table" + " " + "border=" + "1px" + ">" +
                            "<tr" + " " + "class=" + "tr1" + ">" + "<td" + ">航空公司</td>" +
                            "<td>航班</td>" +
                            "<td>机型</td>" +
                            "<td>出发时间</td>" +
                            "<td>抵达时间</td>" +
                            "<td>余票</td>" + "<td>公务舱</td>" + "<td>经济舱</td>" + "</tr>" +
                            "<tr" + " " + "class=" + "tr2" + "><td>" + arr[i][1] + "</td>" +
                            "<td>" + arr[i][2] + "</td>" +
                            "<td>" + arr[i][3] + "</td>" +
                            "<td>" + arr[i][4] + "</td>" +
                            "<td>" + arr[i][5] + "</td>" +
                            "<td>" + arr[i][10] + "</td>" +
                            "<td>" + arr[i][9] + `<input type="radio" name="a" class="radio" value="${str}">` + "</td>" +
                            "<td>" + arr[i][8] + `<input type="radio" name="a" class="radio" value="${str2}">` + "</td>" +
                            "</table>" +
                            "</div>" +
                            "</div>"
                    }
                    showbodyf.innerHTML = out;
                    out = "";//清空out数据
                }
            }
        });
    }
    //往返数据ajax
    if (st == 2) {
        $.ajax({
            // headers: {"X-CSRFToken", csrf_token},
            type: 'post',
            url: '/index_ajax2',
            data: { "acity": acity.value, "bcity": bcity.value, "adate": time0.value, 'bdate': time2.value },
            dataType: 'json',
            async: false,
            error: function (request) {
                alert('cuowu');
            },
            success: function (data) {
                if (data['string'] === "0") {
                    showbodyf.innerHTML = "<span>" + "服务器正在更新" + "<p>" + "<img" + " " + "src=" + "../static/s-other/error.png" + ">" + "</span>";
                    showbodys.innerHTML = "<span>" + "服务器正在更新" + "<p>" + "<img" + " " + "src=" + "../static/s-other/error.png" + ">" + "</span>";
                    arr = [], arr2 = [], arr3 = [], arr4 = [], arr5 = [];//清空数据
                    brr = [], brr2 = [], brr3 = [], brr4 = [], brr5 = [];
                }
                if (data['string'] === "1") {
                    showbodyf.innerHTML = "<span>" + "没有航班了呦" + "<p>" + "<img" + " " + "src=" + "../static/s-other/error.png" + ">" + "</span>";
                    showbodys.innerHTML = "<span>" + "没有航班了呦" + "<p>" + "<img" + " " + "src=" + "../static/s-other/error.png" + ">" + "</span>";
                    arr = [], arr2 = [], arr3 = [], arr4 = [], arr5 = [];//清空数据
                    brr = [], brr2 = [], brr3 = [], brr4 = [], brr5 = [];
                }
                if (data['string'] === "2") {
                    arr = JSON.parse(data['a_common']);
                    arr2 = JSON.parse(data['a_go_sort']);
                    arr3 = JSON.parse(data['a_arrival_sort']);
                    arr4 = JSON.parse(data['a_First_class']);
                    arr5 = JSON.parse(data['a_economy_class']);
                    brr = JSON.parse(data['b_common']);
                    brr2 = JSON.parse(data['b_go_sort']);
                    brr3 = JSON.parse(data['b_arrival_sort']);
                    brr4 = JSON.parse(data['b_First_class']);
                    brr5 = JSON.parse(data['b_economy_class']);
                    for (let i = 0; i < arr.length; i++) {
                        str = arr[i] + ',g';
                        str2 = arr[i] + ',j';
                        out += "<div" + " " + "class=" + "xinxi" + ">" +
                            "<div" + " " + "class=" + "tab" + ">" +
                            "<table" + " " + "border=" + "1px" + ">" +
                            "<tr" + " " + "class=" + "tr1" + ">" + "<td" + ">航空公司</td>" +
                            "<td>航班</td>" +
                            "<td>机型</td>" +
                            "<td>出发时间</td>" +
                            "<td>抵达时间</td>" +
                            "<td>余票</td>" + "<td>公务舱</td>" + "<td>经济舱</td>" + "</tr>" +
                            "<tr" + " " + "class=" + "tr2" + "><td>" + arr[i][1] + "</td>" +
                            "<td>" + arr[i][2] + "</td>" +
                            "<td>" + arr[i][3] + "</td>" +
                            "<td>" + arr[i][4] + "</td>" +
                            "<td>" + arr[i][5] + "</td>" +
                            "<td>" + arr[i][10] + "</td>" +
                            "<td>" + arr[i][9] + `<input type="radio" name="a" class="radio" value="${str}">` + "</td>" +
                            "<td>" + arr[i][8] + `<input type="radio" name="a" class="radio" value="${str2}">` + "</td>" +
                            "</table>" +
                            "</div>" +
                            "</div>"
                    }
                    showbodyf.innerHTML = out;
                    out = "";
                    for (let i = 0; i < brr.length; i++) {
                        str = brr[i] + ',g';
                        str2 = brr[i] + ',j'
                        out2 += "<div" + " " + "class=" + "xinxi" + ">" +
                            "<div" + " " + "class=" + "tab" + ">" +
                            "<table" + " " + "border=" + "1px" + ">" +
                            "<tr" + " " + "class=" + "tr1" + ">" + "<td" + ">航空公司</td>" +
                            "<td>航班</td>" +
                            "<td>机型</td>" +
                            "<td>出发时间</td>" +
                            "<td>抵达时间</td>" +
                            "<td>余票</td>" + "<td>公务舱</td>" + "<td>经济舱</td>" + "</tr>" +
                            "<tr" + " " + "class=" + "tr2" + "><td>" + brr[i][1] + "</td>" +
                            "<td>" + brr[i][2] + "</td>" +
                            "<td>" + brr[i][3] + "</td>" +
                            "<td>" + brr[i][4] + "</td>" +
                            "<td>" + brr[i][5] + "</td>" +
                            "<td>" + brr[i][10] + "</td>" +
                            "<td>" + brr[i][9] + `<input type="radio" name="b" class="radio2" value="${str}">` + "</td>" +
                            "<td>" + brr[i][8] + `<input type="radio" name="b" class="radio2" value="${str2}">` + "</td>" +
                            "</table>" +
                            "</div>" +
                            "</div>"
                    }
                    showbodys.innerHTML = out2;
                    out2 = "";
                }
            }
        });
    }
    //  多程航班数据ajax
    if (st == 3) {
        $.ajax({
            type: 'post',
            url: '/index_ajax3',
            contentType: "application/json",
            data: JSON.stringify(send_data),
            dataType: 'json',
            async: false,
            error: function (request) {
                alert('cuowu');
            },
            success: function (data) {
                if (data['string'] === "0") {
                    showbodyf.innerHTML = "<span>" + "服务器正在更新" + "<p>" + "<img" + " " + "src=" + "../static/s-other/error.png" + ">" + "</span>";
                    arr = [], arr2 = [], arr3 = [], arr4 = [], arr5 = [];//清空数据
                }
                if (data['string'] === "1") {
                    showbodyf.innerHTML = "<span>" + "没有航班了呦" + "<p>" + "<img" + " " + "src=" + "../static/s-other/error.png" + ">" + "</span>";
                    arr = [], arr2 = [], arr3 = [], arr4 = [], arr5 = [];//清空数据
                }
                if (data['string'] === "2") {
                    arr = JSON.parse(data['common']);
                    arr2 = JSON.parse(data['go_sort']);
                    arr3 = JSON.parse(data['arrival_sort']);
                    arr4 = JSON.parse(data['First_class']);
                    arr5 = JSON.parse(data['economy_class']);
                    for (let i = 0; i < arr.length; i++) {
                        str = arr[i] + ',g';
                        str2 = arr[i] + ',j';
                        out += "<div" + " " + "class=" + "xinxi" + ">" +
                            "<div" + " " + "class=" + "tab" + ">" +
                            "<table" + " " + "border=" + "1px" + ">" +
                            "<tr" + " " + "class=" + "tr1" + ">" + "<td" + ">航空公司</td>" +
                            "<td>航班</td>" +
                            "<td>机型</td>" +
                            "<td>出发时间</td>" +
                            "<td>抵达时间</td>" +
                            "<td>余票</td>" + "<td>公务舱</td>" + "<td>经济舱</td>" + "</tr>" +
                            "<tr" + " " + "class=" + "tr2" + "><td>" + arr[i][1] + "</td>" +
                            "<td>" + arr[i][2] + "</td>" +
                            "<td>" + arr[i][3] + "</td>" +
                            "<td>" + arr[i][4] + "</td>" +
                            "<td>" + arr[i][5] + "</td>" +
                            "<td>" + arr[i][10] + "</td>" +
                            "<td>" + arr[i][9] + `<input type="radio" name="a" class="radio" value="${str}">` + "</td>" +
                            "<td>" + arr[i][8] + `<input type="radio" name="a" class="radio" value="${str2}">` + "</td>" +
                            "</table>" +
                            "</div>" +
                            "</div>"
                    }
                    showbodyf.innerHTML = out;
                    out = "";//清空out数据
                }
            }
        });
    }
}