function updateTimeline(){

    var eventName = document.getElementById("nameOfEventInput").value;
    var eventDescription = document.getElementById("descriptionOfEventInput").value;
    var eventDate = document.getElementById("dateOfEventInput").value;

    $.ajax({
        type: 'POST',
        url: '/updateTimelineJson',
        data: {eventName: eventName, eventDescription: eventDescription, eventDate: eventDate}
    });
}