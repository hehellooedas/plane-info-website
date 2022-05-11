
var infofirst=document.getElementById('info0');
var infosecond=document.getElementById('info2');
var arr=[];
var arr2=[];
var out;
var aaa=document.getElementById('abc');
var lll=document.getElementById('lll');
var time=document.getElementsByClassName('input')[0];
//上面不用管，这是写的去程和返程的转换
//封装ajax；
//搜索触发的接口
// var app = angular.module('app',["wui.date"]);
// var exit = document.getElementById('exit');
// exit.onclick = function(){
//     location.href = {{ exit_url }};
// };
var arr=[['上海','经济舱']]
function reqfirst() {
   if(st==1){
    $.ajax({
        // headers: {"X-CSRFToken", csrf_token},
        type: 'post',
        url: '/index_ajax1',
        data: {"acity":aaa.value,"bcity":lll.value,"adata":input.value},
        dataType: 'json',
        async: false,
        error: function (request) {
            alert('cuowu');
        },
        success: function (data) {
            arr2=data;
            // for(let j=0;j<arr.length;j++){
            //     out+="<li>"+arr[j].city+"</li>";//data自定义
            // }
            // infofirst.innerHTML=out;
            // out='';
            console.log(arr2);
        }
    });
   }
//    2
   if(st==2)
   {
    $.ajax({
        // headers: {"X-CSRFToken", csrf_token},
        type: 'post',
        url: '/index_ajax2',
        data: {"acity":aaa.value,"bcity":lll.value,"adata":input.value,"bdata":input.value},
        dataType: 'json',
        async: false,
        error: function (request) {
            alert('cuowu');
        },
        success: function (data) {
            arr2=data;
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
   if(st==3)
   {
    $.ajax({
        // headers: {"X-CSRFFoken", csrf_token},
        type: 'post',
        url: '/index_ajax3',
        data: {"acity":aaa.value,"bcity":lll.value,"adata":input.value,"bdata":input.value},
        dataType: 'json',
        async: false,
        error: function (request) {
            alert('cuowu');
        },
        success: function (data) {
            arr2=data;
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
//选择舱位时的接口，只要更改菜单值就会触发
//事件我已绑定好
function reqsecond(x){
    
    // $.ajax({
    //     headers: {"X-CSRFToken", csrf_token},
    //     type: 'post',
    //     url: '/index_ajax',
    //     data: '',
    //     dataType: 'json',
    //     async: false,
    //     error: function (request) {
    //         alert('cuowu');
    //     },
    //     success: function (data) {
    //         arr2=data;
    //         for(let j=0;j<arr.length;j++){
    //             out+="<li>"+arr[j].city+"</li>";//data自定义
    //         }
    //         infofirst.innerHTML=out;
    //         out='';
    //     }
    // });
}
var timeend=document.getElementsByClassName('time-end')[0];
var dan=document.getElementById("dan");
var shuang=document.getElementById("shuang");
var duo=document.getElementById('duo');
var st;
var show=document.getElementsByClassName('show-nav-span')[0];
var show2=document.getElementsByClassName('show-nav-span2')[0];
dan.addEventListener('click',function(){
    timeend.className="time-end";
    st=1;
    show.className="showl";
    show2.className="show-nav-span2";
})
shuang.addEventListener('click',function(){
    timeend.className="time-end2";
    st=2;
    show2.className="showl";
    show.className="show-nav-span";
})
duo.addEventListener('click',function(){
   st=3;
})
var cha=document.getElementsByClassName('cha')[0];
var jingbao=document.getElementsByClassName('jingbao')[0];
var tixing=document.getElementsByClassName('tixing')[0];
tixing.addEventListener('click',function(){
      jingbao.className="jingbao2";
})
cha.addEventListener('click',function(){
    jingbao.className='jingbao';
})