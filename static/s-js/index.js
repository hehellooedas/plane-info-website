var gobtn = document.getElementById('gobtn');
var backbtn = document.getElementById('backbtn');
var navf = document.getElementsByClassName('nav0')[0];
var navs = document.getElementsByClassName('nav2')[0];
var showbodyf = document.getElementsByClassName('show-body0')[0];
var showbodys = document.getElementsByClassName('show-body2')[0];
gobtn.addEventListener('click', function () {
    navf.className = "nav0";
    navs.className = "nav2";
    gobtn.style.backgroundColor = 'red';
    backbtn.style.backgroundColor = '';
    showbodys.className = 'show-body2';
    showbodyf.className = 'show-body0';
});
backbtn.addEventListener('click', function () {
    navs.className = "nav0";
    navf.className = "nav2";
    backbtn.style.backgroundColor = 'red';
    gobtn.style.backgroundColor = '';
    showbodys.className = 'show-body0';
    showbodyf.className = 'show-body2';
});
var infofirst=document.getElementById('info0');
var infosecond=document.getElementById('info2');
var arr=[];
var arr2=[];
var out;
//上面不用管，这是写的去程和返程的转换
//封装ajax；
//搜索触发的接口
function reqfirst() {
    $.ajax({
        type: 'post',
        url: '',
        data: '',
        dataType: 'json',
        async: false,
        error: function (request) {
            alert('cuowu');
        },
        success: function (data) {
             arr=data;
             for(let i=0;i<arr.length;i++){
                 out+="<li>"+arr[i].city+"</li>";//data自定义
             }
             infofirst.innerHTML=out;
             out='';
        }
    });
}
//选择舱位时的接口，只要更改菜单值就会触发
//事件我已绑定好
function reqsecond(){
    $.ajax({
        type: 'post',
        url: '',
        data: '',
        dataType: 'json',
        async: false,
        error: function (request) {
            alert('cuowu');
        },
        success: function (data) {
            arr2=data;
            for(let j=0;j<arr.length;j++){
                out+="<li>"+arr[j].city+"</li>";//data自定义
            }
            infofirst.innerHTML=out;
            out='';
        }
    });
}
