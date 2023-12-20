console.log('exam.js loaded');

$("#saveAnswers").on("click", () => {
    let questions = [];
    $(".question").each(question => {
        answers = [];
        console.log($(question).find(".answer") );
question
        $(question).find(".answer").each(answer => {
            answers.push(Object({
                value: $(answer).find(".answerDesc")[0].text(),
                score: $(answer).find(".answerScore")[0].val()
            }));
        });
        console.log(answers);
        // questions.push(Object({
        //     description: $(question).find(".questionDesc")[0].text(),
        //     answers: answers
        // }));
    });
    let examData = Object({
        examName: $(".examName"),
        questions: questions
    }) 
    console.log(answers);
    // $.ajax({
    //     url: "/exam/answers",
    //     type: "POST",
    //     data: JSON.stringify(examData),
    //     contentType: "application/json; charset=utf-8",
    //     dataType: "json",
    //     success: (data) => {
    //         if (data.status == "success") {
    //             window.location.href = "/exam/result";
    //         } else {
    //             alert("Error: " + data.message);
    //         }
    //     },
    //     error: (error) => { console.log(error); }
    // });
});