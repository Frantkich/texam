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
