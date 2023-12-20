// main.js
console.log('exams_index.js loaded');

$("#searchInput").val("");

$("#searchInput").on("input", function() {
    var selected = $(this).val();
    $("ul li").show();
    $("ul li").filter(function() {
        return $(this).text().toLowerCase().indexOf(selected.toLowerCase()) === -1;
    }).hide();
});

$("#fetchNewExam").on("click", function() { 
    if (confirm("Are you sure?")) {
        $.ajax({
            url: "/exam/fetchNewExam",
            type: "UPDATE",
            success: (data) => {
                console.log(data);
                if (data.length) {
                    data.forEach((exam) => {
                        $("#itemList").append(`<a href="${ exam.code }"><li class="list-group-item">${ exam.name }</li></a>`);
                    });
                } else {
                    alert("Error: " + data.message);
                }
            },
            error: (error) => { console.log(error); }
        });
    }
});
