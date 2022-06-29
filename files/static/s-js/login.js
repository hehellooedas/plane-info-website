var csrf_token = $("[name='_csrf_token']").val();
var use_email = document.getElementById('username');
var password = document.getElementById('password');
var login_btn = document.getElementById("login-btn");
var send_btn = document.getElementsByClassName('send-btn')[0];
var info = document.getElementsByClassName('info')[0];
var codefail = document.getElementsByClassName('codefail')[0];
var databack,information,time = 60;
//正则表达式；
var reg = /^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/;
var use = document.getElementById('username');
//验证码发送验证信息
send_btn.addEventListener('click', function () {
	if (!reg.test(use.value)) {
		info.innerText = '输入格式错误';
	}
	else {
		information = { 'email': use_email.value };
		$.ajax({
			type: "POST",
			url: '/login_ajax1',
			data: information,
			dataType: 'json',
			async: false,
			headers: { "X-CSRFToken": csrf_token },
			error: function (request) {
				alert("Connection error");
			},
			success: function (data) {
				if (data['string'] == '1') {
					send_btn.className = "send-btn3";
					info.innerText = '您的账户并未注册，请检查邮件是否填写正确！';
				}
				else {
				    databack = data['Code'];
					info.innerHTML = '<p>&nbsp</p>';
					send_btn.className = "send-btn2";
					info.innerText = '邮件已发送,请注意查收';
					var ss = setInterval(function () {
						time--;
						send_btn.value = "等待" + time + "s";
						if (time === 0) {
							time = 60;
							send_btn.value = "发送";
							send_btn.className = "send-btn3";
							clearInterval(ss);
						}
					}, 1000);
				}
			}
		});
	}
})
//登录验证
login_btn.addEventListener('click', function () {
	if (databack == password.value) {
		$.ajax({
			type: "POST",
			url: '/login_ajax2',
			data: information,
			dataType: "text",
			async: false,
			headers: { "X-CSRFToken": csrf_token },
			error: function (request) {
				alert("Connection error");
			},
			success: function (data) {
				location.replace(data);
			}
		});
	}
	else { codefail.innerText = '验证码输入错误，请重新输入'; }
});

