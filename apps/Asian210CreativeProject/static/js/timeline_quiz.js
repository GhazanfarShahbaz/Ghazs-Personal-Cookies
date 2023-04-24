function addQuestion(question, index){
    var containerDiv = document.getElementById("container");
    containerDiv.innerHTML += "<div class=question>" + question["question"] + "</div>";

    radio_group_string = "<div class=btn-group role=group>";
    
    // var i = 0

    question["choices"].forEach(function (choice, i) {
        if(choice != question["answer"]){
            radio_group_string += "<input type=radio class=btn-check name=btnradio" + index + " id=btnradio" + 10*index + i + " autocomplete=off>"
            radio_group_string += "<label class='btn btn-outline-primary' for=btnradio" + 10*index + i + ">" + choice + "</label>"
        }
        else {

            // radio_group_string += "<label class='btn btn-primary'>" +

            // "</label>"
            radio_group_string += "<input type=radio class=btn-check name=btnradio" + index + " id=answer" + index+ " autocomplete=off>"
            radio_group_string += "<label class='btn btn-outline-primary' for=answer" + index + ">" + choice + "</label>"
        }

    });
    radio_group_string += "</div>";
    containerDiv.innerHTML  += radio_group_string

    containerDiv.innerHTML += "<hr>"

}

function checkQuiz(){
    var score = 0;
    for(i = 0; i < 10; i++){
        var answer = document.getElementById("answer" + i);

        if(answer != null && answer.checked){
            score += 1;
        }
    }
    var containerDiv = document.getElementById("container");
    containerDiv.innerHTML = "<div id = 'test'>" +
    "You got " + score + " out of 10 correct!" +
    "<br>" +
    "<button type=button class='btn btn-primary' onclick=setupQuiz()>New Quiz</button>" +
    "</div>";

}

function setupQuiz(){
    var theDiv =document.getElementById('test');    
    if(theDiv != null){
        theDiv.remove();
    }

    $.ajax({
        type: 'GET',
        url: '/getQuizQuestions',
        data: {},
        success: function(response){            
            for(i = 0 ; i < response.length; i++){
                addQuestion(response[i], i);
            }
            
            var containerDiv = document.getElementById("container");
            containerDiv.innerHTML += "<button type=button class='btn btn-primary' onclick=checkQuiz()>Submit</button>"
        }
    });
}

$(function(){
    setupQuiz();
});