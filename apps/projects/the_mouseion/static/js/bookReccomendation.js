function bookSearch(){
    if(typeof bookSearch.counter == 'undefined'){
        bookSearch.counter = 0;
    }
    var search = document.getElementById('search').value
    document.getElementById('results').innerHTML = ""
    var elementCount = 0;

    $.ajax({
        url: "https://www.googleapis.com/books/v1/volumes?q=" + search,
        dataType: "json",
        
        success: function(data){
            for(i = 0 ; i < data.items.length ; i++){
                if(bookSearch.counter == 0){
                    searchbar.innerHTML +="<h2 style = left:50%>Search Results</h2>"  
                }
                var found = false; 
                if("authors" in data.items[i].volumeInfo &&  "smallThumbnail" in data.items[i].volumeInfo.imageLinks && "averageRating" in data.items[i].volumeInfo && "ratingsCount" in data.items[i].volumeInfo && 'categories' in data.items[i].volumeInfo && 'publishedDate' in data.items[i].volumeInfo){
                    if(i > 0){
                        for(j = 0 ; j < elementCount ; j++){
                            //checks for duplicates
                            if(document.getElementById("title"+j).textContent == data.items[i].volumeInfo.title && document.getElementById("author"+j).textContent == data.items[i].volumeInfo.authors[0]){
                                found = true;
                                break;
                            }
                        }
                    }
                    if(found == false){
                        results.innerHTML += "<div class= card style=width: 18rem;>" +
                                                "<img class=card-img-top src=" + data.items[i].volumeInfo.imageLinks.smallThumbnail +">"+
                                                "<div class = card-body>"+
                                                    "<h5 id=title"+elementCount+" class=card-title>" + data.items[i].volumeInfo.title + "</h5>"+
                                                        "<p id=author" + elementCount + ">" + data.items[i].volumeInfo.authors[0] +"</p>" +
                                                        "<button style=margin-bottom:10px;width:175px: class=btn btn-primary onclick = displayModel(this.id) id=myBtn_" + elementCount + ">Book Description</button>" +
                                                        "<div id=myModal"+elementCount + " class=modal>"+
                                                            "<div class=modal-content>" +
                                                                "<span id =close"+elementCount+ " class=close>&times;</span>"+
                                                                "<h4> Title: "+data.items[i].volumeInfo.title+"</h1>"+
                                                                "<h4> Author: "+data.items[i].volumeInfo.authors[0]+"</h3>"+
                                                                "<h4> Book Description: </h4>"+ 
                                                                "<p>"+data.items[i].volumeInfo.description+"</p>"+
                                                                "</div>"+
                                                        "</div>"+
                                                    "<button id=" + elementCount + " type = button onclick = addBookToYourList(this.id) class=btn btn-primary>Get Reccomendation</button>" +
                                                "</div>"+
                                            "</div>"
                        elementCount++;
                        addToCsv(data.items[i].volumeInfo.title, data.items[i].volumeInfo.authors[0], data.items[i].volumeInfo.imageLinks.smallThumbnail, 
                            data.items[i].volumeInfo.averageRating, data.items[i].volumeInfo.ratingsCount, data.items[i].volumeInfo.categories[0], data.items[i].volumeInfo.publishedDate)
                    }
                }
            }
        },
        type: "GET"
    });
    bookSearch.counter++
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

function addToCsv(bookName, author, url, ratings, ratingsCount, categories, publishedDate){
    $.ajax({
        type: 'GET',
        url: '/addToData',
        data: {book_name: bookName, author: author, url: url, rating: ratings, ratings_count: ratingsCount, categories: categories, year_published: publishedDate}
    });
}



function addBookToYourList(id){
    jQuery.support.cors = true;
    $.ajax({
        type: 'GET',
        url: '/recc',
        data: {book_name: document.getElementById("title"+id).textContent},
        success: function(response){
            document.getElementById("someId").style.display = "block";
            
            for(i = 0 ; i < 3 ; i++){
                yourList.innerHTML +=   "<div class= card style=width: 18rem;>" +
                                            "<img class=card-img-top src=" + response.Url[i] + ">"+
                                            "<div class = card-body>"+
                                                "<h5 id=title"+i+" class=card-title>" +  response.Book_Name[i] + "</h5>"+
                                                "<p>" + response.Book_Author[i] + "</p>"
                                            "</div>"+
                                        "</div>"
            }
        }
    });
}