
var infofirst = document.getElementById('info0');
var infosecond = document.getElementById('info2');
var arr = [];
var arr2 = [];
var arr3 = [];
var arr4 = [];
var arr5 = [];
var brr = [];
var brr2 = [];
var brr3 = [];
var brr4 = [];
var brr5 = [];
var out = "";
var out2 = "";
var st = 1;
var xiaoxi = document.getElementsByClassName('xiaoxi')[0];
var acity = document.getElementById('citySelect');
var bcity = document.getElementById('citySelect1');
var time0 = document.getElementsByClassName('input')[0];
var time2 = document.getElementsByClassName('input')[1];
var str;
var str2;
//上面不用管，这是写的去程和返程的转换
//封装ajax；
//搜索触发的接口
// var app = angular.module('app',["wui.date"]);
// var exit = document.getElementById('exit');
function reqfirst() {

    if (st == 1) {
        $.ajax({
            // headers: {"X-CSRFToken", csrf_token},
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
                    showbodyf.innerHTML = "<span>" + "服务器正在更新" + "<p>" + "<img" + " " + "src=" + "../static/s-other/1(1).png" + ">" + "</span>";
                    arr = [];
                    arr2 = [];
                    arr3 = [];
                    arr4 = [];
                    arr5 = [];
                }
                if (data['string'] === "1") {
                    showbodyf.innerHTML = "<span>" + "没有航班了呦" + "<p>" + "<img" + " " + "src=" + "../static/s-other/1(1).png" + ">" + "</span>";
                    arr = [];
                    arr2 = [];
                    arr3 = [];
                    arr4 = [];
                    arr5 = [];
                }
                if (data['string'] === "2") {
                    arr = data['common'];
                    arr = JSON.parse(arr);
                    arr2 = data['go_sort'];
                    arr2 = JSON.parse(arr2);
                    arr3 = data['arrival_sort'];
                    arr3 = JSON.parse(arr3);
                    arr4 = data['First_class'];
                    arr4 = JSON.parse(arr4);
                    arr5 = data['economy_class'];
                    arr5 = JSON.parse(arr5);
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
                }
            }
        });
    }
    //    2
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
                    showbodyf.innerHTML = "<span>" + "服务器正在更新" + "<p>" + "<img" + " " + "src=" + "../static/s-other/1(1).png" + ">" + "</span>";
                    showbodys.innerHTML = "<span>" + "服务器正在更新" + "<p>" + "<img" + " " + "src=" + "../static/s-other/1(1).png" + ">" + "</span>";
                    arr = [];
                    arr2 = [];
                    arr3 = [];
                    arr4 = [];
                    arr5 = [];
                    brr = [];
                    brr2 = [];
                    brr3 = [];
                    brr4 = [];
                    brr5 = [];
                }
                if (data['string'] === "1") {
                    showbodyf.innerHTML = "<span>" + "没有航班了呦" + "<p>" + "<img" + " " + "src=" + "../static/s-other/1(1).png" + ">" + "</span>";
                    showbodys.innerHTML = "<span>" + "没有航班了呦" + "<p>" + "<img" + " " + "src=" + "../static/s-other/1(1).png" + ">" + "</span>";
                    arr = [];
                    arr2 = [];
                    arr3 = [];
                    arr4 = [];
                    arr5 = [];
                    brr = [];
                    brr2 = [];
                    brr3 = [];
                    brr4 = [];
                    brr5 = [];
                }
                if (data['string'] === "2") {
                    arr = data['a_common'];
                    arr = JSON.parse(arr);
                    console.log(arr);
                    arr2 = data['a_go_sort'];
                    arr2 = JSON.parse(arr2);
                    arr3 = data['a_arrival_sort'];
                    arr3 = JSON.parse(arr3);
                    arr4 = data['a_First_class'];
                    arr4 = JSON.parse(arr4);
                    arr5 = data['a_economy_class'];
                    arr5 = JSON.parse(arr5);
                    brr = data['b_common'];
                    brr = JSON.parse(brr);
                    brr2 = data['b_go_sort'];
                    brr2 = JSON.parse(brr2);
                    brr3 = data['b_arrival_sort'];
                    brr3 = JSON.parse(brr3);
                    brr4 = data['b_First_class'];
                    brr4 = JSON.parse(brr4);
                    brr5 = data['b_economy_class'];
                    brr5 = JSON.parse(brr5);
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
                            "<td>" + arr[i][9] +  `<input type="radio" name="a" class="radio" value="${str}">` + "</td>" +
                            "<td>" + arr[i][8] + `<input type="radio" name="a" class="radio" value="${str2}">`+ "</td>" +
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
                            "<td>" + brr[i][9] +  `<input type="radio" name="b" class="radio" value="${str}">` + "</td>" +
                            "<td>" + brr[i][8] +  `<input type="radio" name="b" class="radio" value="${str2}">` + "</td>" +
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
    //    3
    if (st == 3) {
        $.ajax({
            // headers: {"X-CSRFFoken", csrf_token},
            type: 'post',
            url: '/index_ajax3',
            data: { "acity": acity.value, "bcity": bcity.value, "adate": time0.value, "bdate": time2.value },
            dataType: 'json',
            async: false,
            error: function (request) {
                alert('cuowu');
            },
            success: function (data) {

            }
        });
    }
}
var timeend = document.getElementsByClassName('time-end')[0];
var dan = document.getElementById("dan");
var shuang = document.getElementById("shuang");
var duo = document.getElementById('duo');
var show = document.getElementsByClassName('show-nav-span')[0];
var show2 = document.getElementsByClassName('show-nav-span2')[0];
dan.addEventListener('click', function () {
    timeend.className = "time-end";
    st = 1;
    show2.style.zIndex = 2
    show.style.zIndex = 1;
})
shuang.addEventListener('click', function () {
    timeend.className = "time-end2";
    st = 2;
    show.style.zIndex = 2
    show2.style.zIndex = 1;
})
duo.addEventListener('click', function () {
    st = 3;
})
var cha = document.getElementsByClassName('cha')[0];
var jingbao = document.getElementsByClassName('jingbao')[0];
var tixing = document.getElementsByClassName('tixing')[0];
var cover = document.getElementsByClassName('cover')[0];
tixing.addEventListener('click', function () {
    jingbao.className = 'jingbao2';
    cover.style.height = document.body.clientHeight + 'px';
    cover.className = 'cover2';
})
cha.addEventListener('click', function () {
    jingbao.className = 'jingbao';
    cover.style.height = document.body.clientHeight + 'px';
    cover.className = 'cover';
})
//show
var but = document.getElementsByClassName('but');
var but2 = document.getElementsByClassName('but2');
for (let k = 0; k < but.length; k++) {
    but[k].addEventListener('click', function () {
        for (let j = 0; j < but.length; j++) {
            but[j].style.backgroundColor = 'powderblue';
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
                    "<td>" + arr2[i][9] +  `<input type="radio" name="a" class="radio" value="${str}">`+ "</td>" +
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
                    "<td>" + arr3[i][9] +  `<input type="radio" name="a" class="radio" value="${str}">`+ "</td>" +
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
                    "<td>" + arr4[i][9] +  `<input type="radio" name="a" class="radio" value="${str}">`+ "</td>" +
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
                    "<td>" + arr5[i][9] + `<input type="radio" name="a" class="radio" value="${str}">`+ "</td>" +
                    "<td>" + arr5[i][8] +`<input type="radio" name="a" class="radio" value="${str2}">` + "</td>" +
                    "</table>" +
                    "</div>" +
                    "</div>"
            }
            if (arr.length == 0) {
                showbodyf.innerHTML = "<span>" + "没有航班了呦" + "<p>" + "<img" + " " + "src=" + "../static/s-other/1(1).png" + ">" + "</span>";
            }
            else {
                showbodyf.innerHTML = out;
            }
            out = "";
        }
    })
}
// 2

for (let k = 0; k < but2.length; k++) {
    but2[k].addEventListener('click', function () {
        for (let j = 0; j < but2.length; j++) {
            but2[j].style.backgroundColor = 'powderblue';
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
                    "<td>" + brr2[i][9] + `<input type="radio" name="b" class="radio" value="${str}">` + "</td>" +
                    "<td>" + brr2[i][8] + `<input type="radio" name="b" class="radio" value="${str2}">` + "</td>" +
                    "</table>" +
                    "</div>" +
                    "</div>"
            }
            if (brr == []) {
                showbodys.innerHTML = "<span>" + "没有航班了呦" + "<p>" + "<img" + " " + "src=" + "../static/s-other/1(1).png" + ">" + "</span>";
            }
            else {
                showbodys.innerHTML = out2;
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
                    "<td>" + brr3[i][9] + `<input type="radio" name="b" class="radio" value="${str}">` + "</td>" +
                    "<td>" + brr3[i][8] + `<input type="radio" name="b" class="radio" value="${str2}">` + "</td>" +
                    "</table>" +
                    "</div>" +
                    "</div>"
            }
            if (brr.length == 0) {
                showbodys.innerHTML = "<span>" + "没有航班了呦" + "<p>" + "<img" + " " + "src=" + "../static/s-other/1(1).png" + ">" + "</span>";
            }
            else {
                showbodys.innerHTML = out2;
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
                    "<td>" + brr4[i][9] + `<input type="radio" name="b" class="radio" value="${str}">`  + "</td>" +
                    "<td>" + brr4[i][8] + `<input type="radio" name="b" class="radio" value="${str2}">` + "</td>" +
                    "</table>" +
                    "</div>" +
                    "</div>"
            }
            if (brr.length == 0) {
                showbodys.innerHTML = "<span>" + "没有航班了呦" + "<p>" + "<img" + " " + "src=" + "../static/s-other/1(1).png" + ">" + "</span>";
            }
            else {
                showbodys.innerHTML = out2;
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
                    "<td>" + brr5[i][9] + `<input type="radio" name="b" class="radio" value="${str}">` + "</td>" +
                    "<td>" + brr5[i][8] + `<input type="radio" name="b" class="radio" value="${str2}">` + "</td>" +
                    "</div>" +
                    "</div>"
            }
            if (brr.length == 0) {
                showbodys.innerHTML = "<span>" + "没有航班了呦" + "<p>" + "<img" + " " + "src=" + "../static/s-other/1(1).png" + ">" + "</span>";
            }
            else {
                showbodys.innerHTML = out2;
            }
            out2 = "";
        }
    })
}
var cang;
var a1;
var b1;
var app;
var bpp;
var send = [100];
var nav_tishi = document.getElementsByClassName('nav_tishi')[0];
var nav_tishi3 = document.getElementsByClassName('nav_tishi3')[0];
pay.addEventListener('click', function () {
    if (order1 !== 1) {
        nav_tishi3.innerText = '请选择去程的机票';
        nav_tishi3.className = 'nav_tishi4';
    }
    if (order2 !== 1 && st == 2) {
        nav_tishi.innerText = '请选择返程的机票';
        nav_tishi.className = 'nav_tishi2';
    }
    if (order1 == 1 && st == 1) {
        nav_tishi3.className = 'nav_tishi3';
        jiesuan();
    }
    if (order1 == 1 && st == 2 & order2 == 1) {
        nav_tishi.className = 'nav_tishi';
        nav_tishi3.className = 'nav_tishi3';
        jiesuan();
    }
});
function jiesuan() {
    app = document.getElementsByName('a');
    bpp = document.getElementsByName('b');
    if (st == 1) {
        for (let i = 0; i < app.length; i++) {
            if (app[i].checked) {
                a1 = app[i].value;
                break;
            }
        }
        if (a1.indexOf('g')=='g') {
            cang = ['1'];
        }
        a1 = a1.split(',');
        send = a1;
        $.ajax(
            {
                url: '/index_ajax4',
                type: 'POST',
                data: { "table": JSON.stringify(send), "cabin": JSON.stringify(cang), "st": "1" },
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
        for (let i = 0; i < app.length; i++) {
            if (app[i].checked) {
                a1 = app[i].value;
                break;
            }
        }
        for (let i = 0; i < bpp.length; i++) {
            if (bpp[i].checked) {
                b1 = bpp[i].value;
                break;
            }
        }
        if (a1.indexOf('g') != -1) {
            cang[0] = '1';
        }
        if (a1.indexOf('j') != -1) {
            cang[0] = '0';
        }
        if (b1.indexOf('g') != -1) {
            cang[1] = '1';
        }
        if (b1.indexOf('j') != -1) {
            cang[1] = '0';
        }
        a1 = a1.split(',');
        b1 = b1.split(',');
        send[0] = a1;
        send[1] = b1;
        $.ajax(
            {
                url: '/index_ajax4',
                type: 'POST',
                data: {"table": JSON.stringify(send),"cabin": JSON.stringify(cang),"st": "2"},
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
}