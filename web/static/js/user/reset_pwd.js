;
var reset_pwd_ops = {
    init: function () {
        this.eventBind()
    },
    eventBind: function () {
        $("#save").click(function () {
            var old_password_target = $("#old_password");
            var new_password_target = $("#new_password");
            var old_password = old_password_target.val();
            var new_password = new_password_target.val();
            $.ajax({
                url: common_ops.buildUrl("/user/reset_pwd"),
                type: "POST",
                data: {"old_password": old_password, "new_password": new_password},
                dataType: "json",
                success: function (res) {
                    common_ops.alert("用户密码修改成功")
                },
                error: function (res) {
                    common_ops.alert(JSON.stringify(res))
                }
            })
        });
    }

};

$(document).ready(function () {
    reset_pwd_ops.init();
});