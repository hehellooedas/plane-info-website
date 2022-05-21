
var list=document.getElementById('list_hang');
var zongjia=document.getElementsByClassName('zongjia')[0];
var str,cang,money,date,date2;
var sum=0;
var cang2=[10];
var money2=[10];
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
        error: function (request) {
          alert("Connection error");
        },
        success: function (data) {
          st = data['st'];
          table = JSON.parse(data['table']);
          email = data['email'];
          add();
        }
      }
    )
  })();

