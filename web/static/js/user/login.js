;
var user_login_ops = {
    init: function () {
        this.eventBind()
    },
    eventBind: function () {
        $(".do_login").click(function () {
            var login_name = $(".login_wrap input[name=login_name]").val();
            var login_pwd = $(".login_wrap input[name=login_pwd]").val();
            if (login_name == undefined || login_name.length < 1) {
                common_ops.alert("请输入用户名")
            }
            if (login_pwd == undefined || login_pwd.length < 1) {
                common_ops.alert("请输入用户密码")
            }
            $.ajax({
                url: common_ops.buildUrl("/user/login"),
                type: "POST",
                data: {"login_name": login_name, "login_pwd": login_pwd},
                dataType: "json",
                success: function (res) {
                    // 登录成功进入首页
                    if (res.code == 200) {
                        window.location.href = common_ops.buildUrl("/")
                    } else {
                        common_ops.alert(res.msg)
                    }
                },
                error: function (res) {
                    common_ops.alert("执行出错")
                    common_ops.alert(JSON.stringify(res))
                }
            })
        });
    }


};

$(document).ready(function () {
    user_login_ops.init();
});