
var infofirst=document.getElementById('info0');
var infosecond=document.getElementById('info2');
var arr=[];
var arr2=[];
var out="";
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
aaa.addEventListener('mouseup',function(){
    console.log(aaa.value)
})

function reqfirst() {
   if(st==1){
    $.ajax({
        // headers: {"X-CSRFToken", csrf_token},
        type: 'post',
        url: '/index_ajax1',
        data: {"acity":aaa.value,"bcity":lll.value,"adata":time.value},
        // dataType: 'json',
        async: false,
        error: function (request) {
            alert('cuowu');
        },
        success: function (data) {
           arr=data;
           for(let i=0;i<1;i++)
           {
            out+="<div"+" "+ "class=" + "xinxi" +">"+
            "<div" +" "+"class="+"gou"+">"+
                "<input"+" "+"type="+"radio"+" "+"name="+"a"+" "+"class="+"radio"+">"+
            "</div>"+
                "<div"+" "+"class="+"tab"+">"+                           
                    "<table"+" "+"border="+"1px"+">"+
                        "<tr"+" "+"class="+"tr1"+">"+"<td"+">航空公司</td>"+
                        "<td>航班</td>"+
                        "<td>机型</td>"+
                        "<td>出发时间</td>"+
                        "<td>抵达时间</td>"+
                        "<td>价格</td>"+
                        "<td>余票</td></tr>"+
                        "<tr"+" "+"class="+"tr2"+"><td>"+arr[i][1]+"</td>"+
                            "<td>"+arr[i][2]+"</td>"+
                            "<td>"+arr[i][3]+"</td>"+
                            "<td>"+arr[i][4]+"</td>"+
                            "<td>"+arr[i][5]+"</td>"+
                            "<td>"+arr[i][8]+"</td>"+
                            "<td>"+arr[i][10]+"</td>"+
                    "</table>"+
                    "</div>"+
            "</div>"
           }
           show0.innerHTML=out;
           out="";
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
        data: {"acity":'北京',"bcity":'上海',"adata":'2022-12-21','bdata':'2022-12-25'},
        // dataType: 'json',
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
//show
var out;
var show0=document.getElementsByClassName('show-body0')[0];
//show0.innerHTML;
var a1=[];
var a2=[];
var a3=[];
var f1=[];
var f2=[];
var f3=[];
var s1=[];
var s2=[];
var s3=[];
var t1=[];
var t2=[];
var t3=[];
let p=0;
var arr=[[3710, '厦门航空', 'MF8083', '波音737', '2022-12-21 07:45:00', '2022-12-21 09:50:00', '福州', '济南', 1480.0, 3700.0, 400, 400], [3711, '厦门航空', 'MF8041', '波音738', '2022-12-21 12:30:00', '2022-12-21 14:45:00']];
function reqsecond(x){  
    let p=0;
    for(let i=0;i<arr.length;i++)
    {
        out+="<div"+" "+ "class=" + "xinxi" +">"+
        "<div" +" "+"class="+"gou"+">"+
            "<input"+" "+"type="+"radio"+" "+"name="+"a"+" "+"class="+"radio"+">"+
        "</div>"+
            "<div"+" "+"class="+"tab"+">"+                           
                "<table"+" "+"border="+"1px"+">"+
                    "<tr"+" "+"class="+"tr1"+">"+"<td"+">航空公司</td>"+
                    "<td>航班</td>"+
                    "<td>机型</td>"+
                    "<td>出发时间</td>"+
                    "<td>抵达时间</td>"+
                    "<td>价格</td>"+
                    "<td>余票</td></tr>"+
                    "<tr"+" "+"class="+"tr2"+"><td>"+arr[i][1]+"</td>"+
                        "<td>"+arr[i][2]+"</td>"+
                        "<td>"+arr[i][3]+"</td>"+
                        "<td>"+arr[i][4]+"</td>"+
                        "<td>"+arr[i][5]+"</td>"+
                        "<td>"+arr[i][8]+"</td>"+
                        "<td>"+arr[i][10]+"</td>"+
                "</table>"+
                "</div>"+
        "</div>"
    }
    console.log(out);
    show0.innerHTML=out;
    out="";
}
var date=new Date(arr[0][4]);
console.log(date);
function reqsecond2(x){  
    let p=0;
      for(let i=0;i<a1.length;i++)
      {
         if('MF8083'===a1[i][1])
         {
             a2[p]=a1[i];
             p++;
         }
      }
}

function reqsecond3(x){  
    let p=0;
      for(let i=0;i<a1.length;i++)
      {
         if('MF8083'===a1[i][1])
         {
             a2[p]=a1[i];
             p++;
         }
      }
}
