function getKey(){
    let key = "";
    
    $.ajax({
        type: 'GET',
        url: '/movieKey',
        async: false, 
        cache: false,
        success: function(response){
            key =  response;
        }
    });

    return(key)
}

function movieSearch(){
    var search = document.getElementById('search').value
    document.getElementById('results').innerHTML = ""
    var elementCount = 0

    $.ajax({
        url: "https://api.themoviedb.org/3/search/movie?api_key="+ getKey() + "&query=" + search,
        dataType: "json",
        
        success: function(data){
            for(i = 0 ; i < data.results.length ; i++){
                results.innerHTML  += "<div class= card style=width: 18rem;>" +
                                            "<img style= width: 200px; height: 200px;class=card-img-top src=https://image.tmdb.org/t/p/w185" + data.results[i].poster_path +">"+
                                            "<div class = card-body>"+
                                                "<h5 id=title"+elementCount+" class=card-title>" + data.results[i].original_title  + "</h5>"+
                                                    "<button style=margin-bottom:10px;width:175px: class=btn btn-primary onclick = displayModel(this.id) id=myBtn_" + elementCount + ">Movie Description</button>" +
                                                    "<div id=myModal"+elementCount + " class=modal>"+
                                                        "<div class=modal-content>" +
                                                            "<span id =close"+elementCount+ " class=close>&times;</span>"+
                                                            "<h4> Title: "+data.results[i].original_title+"</h1>"+
                                                            "<h4> Movie Overview: </h4>"+ 
                                                            "<p>"+data.results[i].overview+"</p>"+
                                                        "</div>"+
                                                    "</div>"+
                                                "<button id=" +elementCount+ " onclick = movieReccomendation(this.id) type = button class=btn btn-primary>Get Reccomendation</button>" +
                                            "</div>"+
                                        "</div>"
                elementCount++
            }
        },
        type: "GET"
    });
}
function displayModel(this_id){
    id = this_id.substr(this_id.indexOf('_')+1)
    var modal = document.getElementById("myModal"+id);

    // Get the button that opens the modal
    var btn = document.getElementById("myBtn_"+id);

    // Get the <span> element that closes the modal
    var span = document.getElementsByClassName("close")[id];

    // When the user clicks the button, open the modal 
    btn.onclick = function() {
    modal.style.display = "block";
    }

    // When the user clicks on <span> (x), close the modal
    span.onclick = function() {
    modal.style.display = "none";
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
}



function movieReccomendation(id){
    jQuery.support.cors = true;
    
    $.ajax({
        type: 'GET',
        url: '/movieRecc',
        data: {movie_name: document.getElementById("title"+id).textContent},
        success: function(response){
            document.getElementById("someId").style.display = "block";
            for(i = 0 ; i < 3 ; i++){
                returnReccomendation(response.movie_name[i], i)
            }
        }
    });
}

function returnReccomendation(movieData, modalId){
    if(modalId == 0){
        yourList.innerHTML = "" //Resetting the old reccomended list
    }
    movieData = movieData.substr(2, movieData.length - 4)
    $.ajax({
        url: "https://api.themoviedb.org/3/search/movie?api_key="+ getKey() +"&query=" + movieData,
        dataType: "json",
        
        success: function(data){
            foundIndex = -1

            for(i = 0; i < data.results.length; i++){
                if(data.results[i].title == movieData){
                    foundIndex = i;
                    break;
                }
            }

            if(foundIndex != -1){
                let newId = modalId + 100
                yourList.innerHTML  += "<div class= card style=width: 18rem;>" +
                                            "<img style= width: 200px; height: 200px;class=card-img-top src=https://image.tmdb.org/t/p/w185" + data.results[foundIndex].poster_path +">"+
                                            "<div class = card-body>"+
                                                "<h5 id=title"+newId+" class=card-title>" + data.results[foundIndex].title  + "</h5>"+
                                                    "<button style=margin-bottom:10px;width:175px: class=btn btn-primary onclick = displayModel(this.id) id=myBtn_" + newId+ ">Movie Description</button>" +
                                                    "<div id=myModal"+newId + " class=modal>"+
                                                        "<div class=modal-content>" +
                                                            "<span id =close"+newId+ " class=close>&times;</span>"+
                                                            "<h4> Title: "+data.results[foundIndex].title+"</h1>"+
                                                            "<h4> Movie Overview: </h4>"+ 
                                                            "<p>"+data.results[foundIndex].overview+"</p>"+
                                                        "</div>"+
                                                    "</div>"+
                                            "</div>"+
                                        "</div>"
            }
        },
        type: "GET"
    });
}