jQuery.noConflict();
window.addEventListener("load", function() {
    (function ($) {
        $(function () {
            var id_type_user = $('#id_type_user');
            var id_select_action_password = $('#id_select_action_password');

            var field_send_password = $('.field-send_password');
            var field_send_gen_password = $('.field-send_gen_password');
            var id_send_password = $('#id_send_password');
            var id_send_gen_password = $('#id_send_gen_password');
            // var id_open_access = $('#id_open_access')

            var field_password1 = $('.field-password1');
            var field_password2 = $('.field-password2');
            var id_password1 = $('#id_password1');
            var id_password2 = $('#id_password2');

            $(`label[for='${id_password1.attr("id")}']`).addClass('required');
            $(`label[for='${id_password2.attr("id")}']`).addClass('required');

            var field_is_getter_email = $('.field-is_getter_email');
            // var field_send_email_to_user = $('.field-send_email_to_user');
            var field_send_email_to_director = $('.field-send_email_to_director');

            var id_is_getter_email = $('#id_is_getter_email');
            // var id_send_email_to_user = $('#id_send_email_to_user');
            var id_send_email_to_director = $('#id_send_email_to_director');



            function hide_elements_form() {
                field_send_gen_password.hide()
                field_send_password.hide();
                field_send_email_to_director.hide();
                // field_send_email_to_user.hide();
                field_password1.hide();
                field_password2.hide();
                field_is_getter_email.hide();
            }
            hide_elements_form();

            function clear_field_form(){
                if (!id_password1[0] === undefined)
                    id_password1[0].value = '';
                if (!id_password2[0] === undefined)
                    id_password2[0].value = '';
                if (!id_send_password[0] === undefined)
                    id_send_password[0].checked = false;
                if (!id_send_gen_password[0] === undefined)
                    id_send_gen_password[0].checked = false;
            }

            function toggle_type_user(){
                let type_user = parseInt(id_type_user.val());

                if (type_user == 1){
                    field_is_getter_email.show();
                    field_send_email_to_director.hide();

                    if (!id_send_email_to_director[0] === undefined)
                        id_send_email_to_director[0].checked = false;

                    clear_field_form();
                } else if (type_user == 2) {
                    field_is_getter_email.hide();
                    field_send_email_to_director.show()

                    if (!id_is_getter_email[0] === undefined)
                        id_is_getter_email[0].checked = false;

                    clear_field_form();
                }
            }
            toggle_type_user();

            function toggle_action_password() {
                let id_action_pass = parseInt(id_select_action_password.val());

                switch (id_action_pass) {
                    case 1:
                        field_password1.show();
                        field_password2.show();
                        field_send_password.show();
                        field_send_gen_password.hide();

                        id_send_gen_password[0].checked = false;
                        break;
                    case 2:
                        field_password1.hide();
                        field_password2.hide();
                        field_send_password.hide();
                        field_send_gen_password.show();

                        id_password1[0].value = '';
                        id_password2[0].value = '';
                        break;
                    case 3:
                        field_password1.hide();
                        field_password2.hide();
                        field_send_password.hide();
                        field_send_gen_password.hide()

                        clear_field_form();
                        break;
                }
            }
            // if (!id_select_action_password[0] === undefined)
            toggle_action_password();



            id_type_user.change(function () {
                toggle_type_user();
            });

            id_select_action_password.change(function () {
                toggle_action_password();
            });

        });
    })(django.jQuery);
});

