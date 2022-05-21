var csrf_token = $("[name='_csrf_token']").val();
var email1 = document.getElementById('username');
var password = document.getElementById('password');
var reg = document.getElementById("reg");//这里名字改了以下 
var sendbtn = document.getElementsByClassName('send-btn')[0];
var databack;
var time = 60;
var information;
var info = document.getElementsByClassName('info')[0];
var codefail = document.getElementsByClassName('codefail')[0];
sendbtn.addEventListener('click', function () {
	if (!reg2.test(use.value)) {
		info.innerText = '输入格式错误';
	}
	else {
		information = { 'email': email1.value };
		$.ajax({
			type: "POST",
			url: '/login_ajax1',
			data: information,
			dataType: 'json',
			async: false,
			headers: {"X-CSRFToken":csrf_token},
			error: function (request) {
				alert("Connection error");
			},
			success: function (data) {
				if (data == '1') {
					sendbtn.className = "send-btn3";
					info.innerText = '你的邮箱已经注册,请重新填写';
				}
				else {
					info.innerHTML = '<p>&nbsp</p>';
					sendbtn.className = "send-btn2";
					var ss = setInterval(function () {
						time--;
						sendbtn.value = "等待" + time + "s";
						if (time === 0) {
							time = 60;
							sendbtn.value = "发送";
							sendbtn.className = "send-btn3";
							clearInterval(ss);
						}
					}, 1000);
				}
			}
		});
	}
})
sendbtn.addEventListener('click', function () {

});
//注册成功和注册失败的消息闪现
reg.addEventListener('click', function () {
	if (databack == password.value) {
		codefail.className = 'codefail2';
		codefail.innerText = '注册成功';
	}
	else { codefail.innerText = '验证码输入错误，请重新输入' }
	$.ajax({
		type: "POST",
		url: '/register_ajax2',
		data: information,
		async: false,
		headers: {"X-CSRFToken":csrf_token},
		error: function (request) {
			alert("Connection error");
		},
		success: function (data) {
			setTimeout(function () {
				location.replace(data);//等一秒在跳转吧
			}, 1000);
		}
	});
});
//正则表达式；
var reg2 = /^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/;
var use = document.getElementById('username');
use.addEventListener('blur', function () {

})