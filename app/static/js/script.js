"use strict";
console.log('script.js loaded');

export { custom_alert, get_base_url, toggle_button_loading };


function custom_alert(resp, timeout=2000) {
    console.log(resp);
    let resp_status, resp_message;
    if (! resp) { 
        resp_status = "danger";
        resp_message = "Something went wrong, please try again later.";
    } else {
        resp_status = resp.status;
        resp_message = resp.message;
    }
    if (resp_status == "error") {  resp_status = "danger" }
    let alertDiv = $("<div>").addClass(`alert alert-${resp_status}`).attr("role", "alert")
    alertDiv.append($("<i>").addClass("bi me-2").addClass(resp_status == "success" ? "bi-check-circle" : "bi-x-circle"));
    alertDiv.append($("<span>").text(resp_message));
    $("#liveAlert").append(alertDiv);
    setTimeout(() => {
        alertDiv.remove();
    }, timeout);
}

function get_base_url() {
    return window.location.origin + $("html base").attr("href");
}

function toggle_button_loading(btn) {
    if (btn.prop("disabled")) {
        btn.prop("disabled", false);
        btn.find(".spinner").remove();
    } else {
        btn.prop("disabled", true);
        btn.prepend($("<span>").addClass("spinner spinner-border spinner-border-sm me-2").attr("aria-hidden", "true"));
    }
}