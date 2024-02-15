"use strict";
console.log('exam_active.js loaded');

import { custom_alert, get_base_url, toggle_button_loading } from './script.js';
import { saveAnswers } from './save_answers_export.js';


function review_archi() {
    if ($("#user_role").text() == "0") {
        $(".answerScore").each(function() {
            let chance_to_let_user_learn_more_stuff = 0.8;
            if ($(this).val() && Math.random() < chance_to_let_user_learn_more_stuff) {
                $(this).val("")
            }
        });
    }
}
review_archi();

function vpn_errors() {
    let errors = [
        "Error 601 - Connection Timeout: The VPN server did not respond within the allotted time. Check your internet connection and try connecting again.",
        "Error 201 - Authentication Failed: Your VPN credentials were not accepted. Double-check your username and password, and try reconnecting.",
        "Error 404 - VPN Server Not Found: The specified VPN server could not be located. Confirm the server address and try connecting again.",
        "Error 503 - Server Overload: The VPN server is currently overloaded. Please try connecting later, or contact your network administrator.",
        "Error 553 - No no no...",
        "Error 800 - Unable to Establish Connection: The VPN connection could not be established. Verify your network settings and try reconnecting.",
        "Error 732 - Protocol Mismatch: The VPN server and client are using incompatible protocols. Adjust your settings to match and attempt the connection again.",
        "Error 619 - Port Closed: The port used for the VPN connection is closed. Ensure the required port is open in your firewall settings.",
        "Error 720 - No PPP Control Protocols Configured: The Point-to-Point Protocol (PPP) control protocols are not configured correctly. Check your VPN settings and adjust as needed.",
        "Error 806 - GRE Blocked: The Generic Routing Encapsulation (GRE) protocol is blocked. Confirm that your firewall allows GRE traffic for the VPN connection.",
        "Error 868 - Remote Connection Not Reachable: The remote connection server could not be reached. Check the server's availability and your internet connection before retrying.",
    ]
    let error = errors[Math.floor(Math.random() * errors.length)]; 
    setTimeout(() => {
        custom_alert({ "status": "error", "message": error }, 10000);
        $("button").prop("disabled", false);
        $("button").find(".spinner").remove();
    }, Math.floor(Math.random() * 10000 ) + 10000);
}

function sendAnswers() {
    return $.ajax({
        url: `${get_base_url()}/exams/active/submit/answers`,
        type: "POST",
        complete: (data) => {
            toggle_button_loading($("#sendAnswers"));
            custom_alert(data.responseJSON, 10000)
        }
    });
}

$("#saveAnswers").on("click", function() {
    toggle_button_loading($(this));
    if ($("#user_role").text() == "0") { vpn_errors(); return; }
    saveAnswers();
});


$("#sendAnswers").on("click", function() {
    if (window.confirm("Your answers will be saved and submit to TLC, do you want to proceed ?")) {
        toggle_button_loading($("#saveAnswers"));
        toggle_button_loading($(this));
        if ($("#user_role").text() == "0") { vpn_errors(); return; }
        saveAnswers().then( () => { sendAnswers(); });
    }
});


$("#submit_now").on("click", function() {
    if (window.confirm("The exam will be submitted, you can't do anything after that, do you want to proceed ?")) {
        $("#submit").click()
        toggle_button_loading($("#saveAnswers"));
        toggle_button_loading($("#sendAnswers"));
        toggle_button_loading($("#submit"));
        if ($("#user_role").text() == "0") { vpn_errors(); return; }
        saveAnswers().then( () => {
            sendAnswers().then( () => {
                $.ajax({
                    url: `${get_base_url()}/exams/active/submit/exam`,
                    type: "POST",
                    success: (data) => {
                        window.location.href = `texam/results/${data.result_id}`;
                    },
                    error: (data) => {
                        custom_alert(data.responseJSON);
                        toggle_button_loading($("#submit"));
                    }
                });
            });
        });
    }
});


$("#submit_delay").on("click", function () {
    if (window.confirm("The exam will be submitted, you can't do anything after that, do you want to proceed ?")) {
        $("#submit").click()
        toggle_button_loading($("#saveAnswers"));
        toggle_button_loading($("#sendAnswers"));
        toggle_button_loading($("#submit"));
        if ($("#user_role").text() == "0") { vpn_errors(); return; }
        saveAnswers().then( () => {
            sendAnswers().then( () => {
                $.ajax({
                    url: `${get_base_url()}/exams/active/submit/exam/${$("#submit_delay_count").val()}`,
                    type: "POST",
                    complete: (data) => {
                        custom_alert(data.responseJSON);
                        toggle_button_loading($("#submit"));
                    },
                });
            });
        });
    }
});

// uncollapse question list by default 
function uncollapseQuestionList() {
    $("#questions").toggle("collapse multi-collapse");
}
uncollapseQuestionList();


