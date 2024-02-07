"use strict";
console.log('admin.js loaded');

import { custom_alert, get_base_url, toggle_button_loading } from './script.js';

$("#searchInput").val("");

function filter_exams(search_string) {
    $("#itemList li").filter(function() {
        return $(this).text().toLowerCase().indexOf(search_string.toLowerCase()) === -1;
    }).hide();
}
$("#searchInput").on("input", function() {
    $("#itemList li").show();
    filter_exams($(this).val());
});

$("#fuck_archi").on("click", function() {
    toggle_button_loading($("#fuck_archi"));
    let exam_data = [];
    $("#itemList li").each((index, exam) => {
        exam_data.push(Object({
            name: $(exam).find("input").attr("id"),
            for_all: $(exam).find("input").prop('checked'),
        }));
    });
    $.ajax({
        url: `${get_base_url()}/admin/for_all`,
        type: "UPDATE",
        data: JSON.stringify(exam_data),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        complete: (data) => {        
            custom_alert(data.responseJSON)
            toggle_button_loading($("#fuck_archi"));
        }
    });
});

$("#createUser").on("click", function() {
    toggle_button_loading($("#createUser"));
    let role = 2;
    switch ($("#role").val()) {
        case "architect":
            role = 0;
            break;
        case "admin":
            role = 1;
            break;
    }
    let user = Object({
        email: $("#email").text(),
        password: $("#password").text(),
        role: role,
    });
    $.ajax({
        url: `${get_base_url()}/admin/create_user`,
        type: "POST",
        data: JSON.stringify(user),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        complete: (data) => {        
            custom_alert(data.responseJSON)
            toggle_button_loading($("#createUser"));
        }
    });
});
