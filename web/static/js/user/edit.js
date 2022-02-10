;
var user_edit_ops = {
    init: function () {
        this.eventBind()
    },
    eventBind: function () {
        $(".save").click(function () {
            var nick_name_target = $("#nickname")
            var email_target = $("#email")
            var nick_name = nick_name_target.val()
            var email = email_target.val()
            if (!nick_name || nick_name.length > 20 || nick_name.length < 3) {
                common_ops.tip("姓名输入不规范", nick_name_target)
            }
            if (!email) {
                common_ops.tip("邮箱不得为空", nick_name_target)
            }
            $.ajax({
                url: common_ops.buildUrl("/user/edit"),
                type: "POST",
                data: {"nick_name": nick_name, "email": email},
                dataType: "json",
                success: function (res) {
                    common_ops.alert("用户修改成功")
                },
                error: function (res) {
                    common_ops.alert(JSON.stringify(res))
                }
            })

        })
    }

};

$(document).ready(function () {
    user_edit_ops.init();
});