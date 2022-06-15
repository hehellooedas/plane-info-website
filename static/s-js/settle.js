var csrf_token = $("[name='_csrf_token']").val();
var list=document.getElementById('list_hang');
var zongjia=document.getElementsByClassName('zongjia')[0];
var user=document.getElementsByClassName('user')[0];
var str=" ",cang,money,date,date2;
var sum=0;//计算总价
var cang2=[10];//对多个航程的舱位储存
var money2=[10];//对多个航程的价格储存
//添加乘客
var jia=document.getElementsByClassName('jia')[0];
var input=document.getElementsByName('input');
var pass=[];
function pack(){
    for (let i=0;i<input.length;i++){
        pass[i]=input[i].value;
    }
    console.log(pass);
}
var up =document.getElementsByClassName('up')[0];
    var passengersl=document.getElementsByClassName('passengersl')[0];
    var addl=document.getElementById('addl');
    addl.addEventListener('click',function (){
        passengersl.className='passengersl2';
        up.style.display='block';
        jia.style.display="flex";
    })
up.addEventListener('click',function (){
     passengersl.className='passengersl';
     up.style.display='none';
     jia.style.display="none";
})
function pan(){
    if(table[12]=="g")
            {
                cang="公务舱";
                money=table[9];
            }
            else{
                cang="经济舱";
                money=table[8];
            }
}
function pan2(){
    for(let i=0;i<table.length;i++)
    {
        if(table[i][12]=="g")
        {
           cang2[i]="公务舱";
           money2[i]=table[i][9];
        }
        else{
            cang2[i]="经济舱";
            money2[i]=table[i][8];
        }
    }
}
function add(){
    if(st=='1'){
            date=new Date(table[4]);
            date2=new Date(table[5]);
            pan();
            str=`<div class="show">
            <h4 style="width: 420px;height:80px;margin-left:20px;"><br>
              <p style="text-align:center ;font-size: large;">${date.toLocaleDateString()}</p>
              <p style="text-align:center ;color: #C4C4C4;">${table[3]} ${cang}</p>
            </h4>
            <div style="position: relative;">
              <div class="show-bot">
                <p style="text-align: center;font-style: italic;">${date.toLocaleTimeString()}</p>
                <p style="text-align: center;font-size:large;">${table[6]}</p>
              </div>
              <div class="show-bot2">

                <p style="text-align: center;font-style: italic;">${date2.toLocaleTimeString()}</p>
                <p style="text-align: center;font-size:large;">${table[7]}</p>
              </div>
              <div style="position:absolute;left:215px;top:10px;width: auto;height: auto;">
                <p style="margin-left:-65px;font-size: 18px;">${table[1]} ${table[2]}</p>
                <div style="width:30px;height:30px"><img src="../static/s-other/tl.png" alt=""
                    style="width:100%;height:100%;"></div>
              </div>
            </div>
            <div style="height:30px;width:100%;background-color: #C4C4C4;border-radius: 0 0 5px 5px;">
              <h4 style="float: right;margin-right: 5px;">￥${money}</h4>
            </div>
          </div>`;
          list.innerHTML=str;
          str=" ";
          zongjia.innerHTML="￥"+money+"";
    }
    // st=2
    if(st=='2'||st=='3'){
        pan2();
        for(let i=0;i<table.length;i++)
        {
            date=new Date(table[i][4]);
            date2=new Date(table[i][5]);
            sum=sum+parseInt(money2[i]);
            str+=`<div class="show">
            <h4 style="width: 420px;height:80px;margin-left:20px;"><br>
              <p style="text-align:center ;font-size: large;">${date.toLocaleDateString()}</p>
              <p style="text-align:center ;color: #C4C4C4;">${table[i][3]} ${cang2[i]}</p>
            </h4>
            <div style="position: relative;">
              <div class="show-bot">
                <p style="text-align: center;font-style: italic;">${date.toLocaleTimeString()}</p>
                <p style="text-align: center;font-size:large;">${table[i][6]}</p>
              </div>
              <div class="show-bot2">

                <p style="text-align: center;font-style: italic;">${date2.toLocaleTimeString()}</p>
                <p style="text-align: center;font-size:large;">${table[i][7]}</p>
              </div>
              <div style="position:absolute;left:215px;top:10px;width: auto;height: auto;">
                <p style="margin-left:-65px;font-size: 18px;">${table[i][1]} ${table[i][2]}</p>
                <div style="width:30px;height:30px"><img src="../static/s-other/tl.png" alt=""
                    style="width:100%;height:100%;"></div>
              </div>
            </div>
            <div style="height:30px;width:100%;background-color: #C4C4C4;border-radius: 0 0 5px 5px;">
              <h4 style="float: right;margin-right: 5px;">￥${money2[i]}</h4>
            </div>
          </div>`;
        }
        list.innerHTML=str;
        str=" ";
        zongjia.innerHTML="￥"+sum+"";
    }
}
var st,table,email;
  (function () {
    $.ajax(
      {
        type: 'POST',
        url: 'settlement_ajax',
        dataType: 'json',
        async: false,
        headers: { "X-CSRFToken": csrf_token },
        error: function (request) {
          alert("Connection error");
        },
        success: function (data) {
          st = data['st'];
          table = JSON.parse(data['table']);
          email = data['email'];
          var namepass=document.getElementsByClassName('namepass')[0];
          namepass.innerHTML='您本人:'+email;
          add();
        }
      }
    )
  })();
//勾选保险购买后对订单总价刷新
var reg=new RegExp("￥");//删除字符
var str5;
var on=0;
var buyname=document.getElementsByClassName('buyname')[0];
     buyname.addEventListener('click',function(){
         on++;
         if(on%2==0){
             str5=zongjia.innerHTML.replace(reg,"");
         str5=parseInt(str5)-100;
         zongjia.innerHTML="￥"+str5+"";
         }
         else {
             str5=zongjia.innerHTML.replace(reg,"");
         str5=parseInt(str5)+100;
         zongjia.innerHTML="￥"+str5+"";
         }
     })
//购票验证
var obj;
var pay=document.getElementsByClassName('pay')[0];
    pay.addEventListener('click',function(){
        pack();
        if(pass.length>0){
            obj={"emails":JSON.stringify(pass)};
        }
        else{
            obj={};
        }
      $.ajax({
        type: 'POST',
        url: '/settlement',
          data:obj,
        dataType: 'text',
        async: false,
        headers: { "X-CSRFToken": csrf_token },
        error: function (request) {
          alert("Connection error");
        },
        success: function (data) {
          alert('购票成功!');
          location.replace(data);
        }
      })
    })
// 用户返回
 var  settle_back=document.getElementsByClassName('settle_back')[0];
 settle_back.addEventListener('click',function(){
    $.ajax({
        type: 'DELETE',
        url: '/settlement_ajax',
        data:{"emails":JSON.stringify(pass)},
        dataType: 'text',
        async: false,
        headers: { "X-CSRFToken": csrf_token },
        error: function (request) {
          alert("Connection error");
        },
        success: function (data) {
          location.replace(data);
        }
    })
 })
