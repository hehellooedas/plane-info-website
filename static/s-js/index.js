
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
function reqfirst() {
    $.ajax({
        headers: {"X-CSRFToken", csrf_token},
        type: 'post',
        url: '/index_ajax',
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
