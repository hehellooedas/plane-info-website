var csrf_token = $("[name='_csrf_token']").val();
var use_email = document.getElementById('username');
var password = document.getElementById('password');
var register = document.getElementById("reg");//注册按钮
var sendbtn = document.getElementsByClassName('send-btn')[0];
var databack,information,time = 60;
//正则表达式；
var reg2 = /^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/;
var use = document.getElementById('username');
var info = document.getElementsByClassName('info')[0];
var codefail = document.getElementsByClassName('codefail')[0];
//验证码发送验证用户信息
sendbtn.addEventListener('click', function () {
	if (!reg2.test(use.value)) {
		info.innerText = '输入格式错误';
	}
	else {
		information = { 'email': use_email.value };
		$.ajax({
			type: "POST",
			url: '/register_ajax1',
			data: information,
			dataType: 'json',
			async: false,
			headers: {"X-CSRFToken":csrf_token},
			error: function (request) {
				alert("Connection error");
			},
			success: function (data) {
				if (data['string'] == '1') {
					sendbtn.className = "send-btn3";
					info.innerText = '你的邮箱已经注册,请重新填写';
				}
				else {
				    databack = data['Code'];
					info.innerHTML = '<p>&nbsp</p>';
					sendbtn.className = "send-btn2";
					info.innerText = '邮件已发送，请注意查收';
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
//注册验证
register.addEventListener('click', function () {
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

