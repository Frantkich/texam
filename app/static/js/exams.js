"use strict";
console.log('exams_index.js loaded');

import { custom_alert, get_base_url } from './script.js';

$("#searchInput").val("");

$("#searchInput").on("input", function() {
    $("#itemList li").show();
    var selected = $(this).val();
    $("#itemList li").filter(function() {
        return $(this).text().toLowerCase().indexOf(selected.toLowerCase()) === -1;
    }).hide();
});

function function_activate_button(btn) {
    if (btn.prop("disabled")) {
        btn.prop("disabled", false);
        btn.find(".spinner").remove();
    } else {
        btn.prop("disabled", true);
        btn.html(`<span class="spinner spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> ${btn.text()}`);
    }
}

function fetch_exams(mode) {
    function_activate_button($(`#fetch_${mode}`));
    $.ajax({
        url: `${get_base_url()}/exams/fetch/${mode}`,
        type: "UPDATE",
        success: (data) => {
            if (data.length) {
                $("#itemList").empty();
                data.forEach((exam) => {
                    $("#itemList").append(`<a href="${document.location.pathname}/${ exam.name }"><li class="list-group-item">${ exam.name }</li></a>`);
                });
            } else {
                alert("Error: " + data.message);
            }
            custom_alert({ "status": "success", "message": `Fetched ${data.length} exams.`});
        },
        error: (data) => {
            custom_alert(data.responseJSON);
        },
        complete: (data) => {
            function_activate_button($(`#fetch_${mode}`));
        }
    });
}

$("#fetch_user").on("click", () => { 
    fetch_exams("user");
});
$("#fetch_all").on("click", () => { 
    fetch_exams("all");
});

fetch_exams("user");