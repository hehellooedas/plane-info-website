
var infofirst = document.getElementById('info0');
var infosecond = document.getElementById('info2');
var arr = [];
var arr2 = [];
var out = "";
var st = 1;
var acity = document.getElementById('citySelect');
var bcity = document.getElementById('citySelect1');
var time0 = document.getElementsByClassName('input')[0];
var time2 = document.getElementsByClassName('input')[1];
//上面不用管，这是写的去程和返程的转换
//封装ajax；
//搜索触发的接口
// var app = angular.module('app',["wui.date"]);
// var exit = document.getElementById('exit');
// exit.onclick = function(){
//     location.href = {{ exit_url }};
// };
function reqfirst() {
    if (st == 1) {
        $.ajax({
            // headers: {"X-CSRFToken", csrf_token},
            type: 'post',
            url: '/index_ajax1',
            data: { "acity": acity.value, "bcity": bcity.value, "adata": time0.value },
            dataType: 'json',
            async: false,
            error: function (request) {
                alert('cuowu');
            },
            success: function (data) {
                arr = data;
                for (let i = 0; i < arr.length; i++) {
                    out += "<div" + " " + "class=" + "xinxi" + ">" +
                        "<div" + " " + "class=" + "tab" + ">" +
                        "<table" + " " + "border=" + "1px" + ">" +
                        "<tr" + " " + "class=" + "tr1" + ">" + "<td" + ">航空公司</td>" +
                        "<td>航班</td>" +
                        "<td>机型</td>" +
                        "<td>出发时间</td>" +
                        "<td>抵达时间</td>" +
                        "<td>余票</td>"+"<td>公务舱</td>"+"<td>经济舱</td>"+"</tr>" +
                        "<tr" + " " + "class=" + "tr2" + "><td>" + arr[i][1] + "</td>" +
                        "<td>" + arr[i][2] + "</td>" +
                        "<td>" + arr[i][3] + "</td>" +
                        "<td>" + arr[i][4] + "</td>" +
                        "<td>" + arr[i][5] + "</td>" +
                        "<td>" + arr[i][10] + "</td>" +
                        "<td>" + arr[i][9] + "<input" + " " + "type=" + "radio" + " " + "name=" + "a" + " " + "class=" + "radio" + ">" + "</td>" +
                        "<td>" + arr[i][8] + "<input" + " " + "type=" + "radio" + " " + "name=" + "a" + " " + "class=" + "radio" + ">" + "</td>" +
                        "</table>" +
                        "</div>" +
                        "</div>"
                }
                showbodyf.innerHTML = out;
                out = "";
            }
        });
    }
    //    2
    if (st == 2) {
        $.ajax({
            // headers: {"X-CSRFToken", csrf_token},
            type: 'post',
            url: '/index_ajax2',
            data: { "acity": acity.value, "bcity": bcity.value, "adata": time0.value, 'bdata': time2.value },
            dataType: 'json',
            async: false,
            error: function (request) {
                alert('cuowu');
            },
            success: function (data) {
                arr2 = data;
                // for(let j=0;j<arr.length;j++){
                //     out+="<li>"+arr[j].city+"</li>";//data自定义
                // }
                // infofirst.innerHTML=out;
                // out='';
                console.log(arr2);
            }
        });
    }
    //    3
    if (st == 3) {
        $.ajax({
            // headers: {"X-CSRFFoken", csrf_token},
            type: 'post',
            url: '/index_ajax3',
            data: { "acity": acity.value, "bcity": bcity.value, "adata": time0.value, "bdata": time2.value },
            dataType: 'json',
            async: false,
            error: function (request) {
                alert('cuowu');
            },
            success: function (data) {
                arr2 = data;
                // for(let j=0;j<arr.length;j++){
                //     out+="<li>"+arr[j].city+"</li>";//data自定义
                // }
                // infofirst.innerHTML=out;
                // out='';
                console.log(arr2);
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
    show2.style.zIndex=2
    show.style.zIndex=1;
})
shuang.addEventListener('click', function () {
    timeend.className = "time-end2";
    st = 2;
    show.style.zIndex=2
    show2.style.zIndex=1;
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
var out;
var but=document.getElementsByClassName('but')[0];
//show0.innerHTML;
var arr = [[3710, '厦门航空', 'MF8083', '波音737', '2022-12-21 07:45:00', '2022-12-21 09:50:00', '福州', '济南', 1480.0, 3700.0, 400, 400], [3710, '厦门航空', 'MF8083', '波音737', '2022-12-21 07:45:00', '2022-12-21 09:50:00', '福州', '济南', 1480.0, 3700.0, 400, 400], [3710, '厦门航空', 'MF8083', '波音737', '2022-12-21 07:45:00', '2022-12-21 09:50:00', '福州', '济南', 1480.0, 3700.0, 400, 400], [3710, '厦门航空', 'MF8083', '波音737', '2022-12-21 07:45:00', '2022-12-21 09:50:00', '福州', '济南', 1480.0, 3700.0, 400, 400], [3710, '厦门航空', 'MF8083', '波音737', '2022-12-21 07:45:00', '2022-12-21 09:50:00', '福州', '济南', 1480.0, 3700.0, 400, 400], [3710, '厦门航空', 'MF8083', '波音737', '2022-12-21 07:45:00', '2022-12-21 09:50:00', '福州', '济南', 1480.0, 3700.0, 400, 400], [3710, '厦门航空', 'MF8083', '波音737', '2022-12-21 07:45:00', '2022-12-21 09:50:00', '福州', '济南', 1480.0, 3700.0, 400, 400]];
 but.addEventListener('click',function(){
     console.log('sss')
    let p = 0;
    for (let i = 0; i < arr.length; i++) {
        out += "<div" + " " + "class=" + "xinxi" + ">" +
            "<div" + " " + "class=" + "tab" + ">" +
            "<table" + " " + "border=" + "1px" + ">" +
            "<tr" + " " + "class=" + "tr1" + ">" + "<td" + ">航空公司</td>" +
            "<td>航班</td>" +
            "<td>机型</td>" +
            "<td>出发时间</td>" +
            "<td>抵达时间</td>" +
            "<td>余票</td>"+"<td>公务舱</td>"+"<td>经济舱</td>"+"</tr>" +
            "<tr" + " " + "class=" + "tr2" + "><td>" + arr[i][1] + "</td>" +
            "<td>" + arr[i][2] + "</td>" +
            "<td>" + arr[i][3] + "</td>" +
            "<td>" + arr[i][4] + "</td>" +
            "<td>" + arr[i][5] + "</td>" +
            "<td>" + arr[i][10] + "</td>" +
            "<td>" + arr[i][9] + "<input" + " " + "type=" + "radio" + " " + "name=" + "a" + " " + "class=" + "radio" + ">" + "</td>" +
            "<td>" + arr[i][8] + "<input" + " " + "type=" + "radio" + " " + "name=" + "a" + " " + "class=" + "radio" + ">" + "</td>" +
            "</table>" +
            "</div>" +
            "</div>"
    }
    console.log(out);
    showbodyf.innerHTML = out;
    out = "";
});