;
var account_set_ops = {
    init: function () {
        this.eventBind()
    },
    eventBind: function () {
        $("#savebtn").click(function () {
            var nickname_target = $("#nickname")
            var mobile_target = $("#mobile")
            var email_target = $("#email")
            var login_name_target = $("#login_name")
            var login_pwd_target = $("#login_pwd")
            var id_target = $("#id")
            var nickname = nickname_target.val();
            var mobile = mobile_target.val();
            var email = email_target.val();
            var login_name = login_name_target.val();
            var login_pwd = login_pwd_target.val();
            var id = id_target.val();

            $.ajax({
                url: common_ops.buildUrl("/account/set"),
                type: "POST",
                data: {
                    "nickname": nickname,
                    "email": email,
                    "mobile": mobile,
                    "email": email,
                    "login_name": login_name,
                    "login_pwd": login_pwd,
                    "id": id
                },
                dataType: "json",
                success: function (res) {
                    if (res.code == 200) {
                        common_ops.alert("用户信息添加成功")
                        window.location.href = common_ops.buildUrl("/account/index")
                    } else {
                        common_ops.alert(res.msg)
                    }
                },
                error: function (res) {
                    common_ops.alert(JSON.stringify(res))
                }
            })
        });
    }

};

$(document).ready(function () {
    account_set_ops.init();
});