"use strict";
console.log('script.js loaded');

export { custom_alert };


function custom_alert(resp, timeout=2000) {
    if (resp.status == "error") {  resp.status = "danger" }
    let alertDiv = $("<div>").addClass(`alert alert-${resp.status}`).attr("role", "alert")
    alertDiv.append($("<i>").addClass("bi me-2").addClass(resp.status == "success" ? "bi-check-circle" : "bi-x-circle"));
    alertDiv.append($("<span>").text(resp.message));
    $("#liveAlert").append(alertDiv);
    setTimeout(() => {
        alertDiv.remove();
    }, timeout);
}
