var photoTaken = false;

var baseurl = "/";

// References to all the element we will need.
var video = document.querySelector('#camera-stream'),
    image = document.querySelector('#snap'),
    start_camera = document.querySelector('#start-camera'),
    controls = document.querySelector('.controls'),
    take_photo_btn = document.querySelector('#take-photo'),
    delete_photo_btn = document.querySelector('#delete-photo'),
    error_message = document.querySelector('#error-message'),
    download_image_btn = document.querySelector('#upload-photo');

let picture_data = null;

// The getUserMedia interface is used for handling camera input.
// Some browsers need a prefix so here we're covering all the options
navigator.getMedia = (navigator.getUserMedia ||
    navigator.webkitGetUserMedia ||
    navigator.mozGetUserMedia ||
    navigator.msGetUserMedia);

navigator.mediaDevices.enumerateDevices().then(function (sourceInfos) {
    var videoSource = null;
    for (var i = 0; i != sourceInfos.length; ++i) {
        var sourceInfo = sourceInfos[i];
        if (sourceInfo.kind.indexOf('video') != -1) {
            console.log(sourceInfo);

            videoSource = sourceInfo.deviceId;
        }
    }

    sourceSelected(videoSource);
});

// Mobile browsers cannot play video without user input,
// so here we're using a button to start it manually.
start_camera.addEventListener("click", function (e) {

    e.preventDefault();

    // Start video playback manually.
    video.play();
    showVideo();

});


function sourceSelected(videoSource) {
    var constraints = {
        video: {
            optional: [{
                sourceId: videoSource
            }]
        }
    };

    navigator.getMedia(constraints, function (stream) {

            // Create an object URL for the video stream and
            // set it as src of our HTLM video element.
            video.src = window.URL.createObjectURL(stream);
            // Play the video element to start the stream.
            video.play();
            video.onplay = function () {
                showVideo();
            };

        },
        // Error Callback
        function (err) {
            displayErrorMessage("There was an error with accessing the camera stream: " + err.name, err);
        });
}

/* if (!navigator.getMedia) {
    displayErrorMessage("Your browser doesn't have support for the navigator.getUserMedia interface.");
} else {

    // Request the camera.
    navigator.getMedia({
            video: true
        },
        // Success Callback
        function (stream) {

            // Create an object URL for the video stream and
            // set it as src of our HTLM video element.
            video.src = window.URL.createObjectURL(stream);

            // Play the video element to start the stream.
            video.play();
            video.onplay = function () {
                showVideo();
            };

        },
        // Error Callback
        function (err) {
            displayErrorMessage("There was an error with accessing the camera stream: " + err.name, err);
        }
    );

} */



// Mobile browsers cannot play video without user input,
// so here we're using a button to start it manually.
start_camera.addEventListener("click", function (e) {

    e.preventDefault();

    // Start video playback manually.
    video.play();
    showVideo();

});


var state = 0;

function update_view() {
    if (state == 0) {
        $("#take-photo").css("display", "block");
        $("#delete-photo").css("display", "none");
        $("#upload-photo").css("display", "none");
        $("#main_container1").css("display", "block");
        $("#main_container2").css("display", "none");
    } else if (state == 1) {
        $("#take-photo").css("display", "none");
        $("#delete-photo").css("display", "block");
        $("#upload-photo").css("display", "block");
        $("#main_container1").css("display", "block");
        $("#main_container2").css("display", "none");
    } else if (state == 2) {
        $("#main_container1").css("display", "none");
        $("#main_container2").css("display", "block");
    }
}



take_photo_btn.addEventListener("click", function (e) {

    photoTaken = true;

    e.preventDefault();

    var snap = takeSnapshot();
    picture_data = snap
    // Show image.
    image.setAttribute('src', snap);
    image.classList.add("visible");

    // Enable delete and save buttons
    delete_photo_btn.classList.remove("disabled");
    download_image_btn.classList.remove("disabled");
    take_photo_btn.classList.add("disabled");

    $('#camera-stream').hide();

    // Pause video playback of stream.
    video.pause();
    state = 1;
    update_view();

});

$("#top_overlay").on("touchmove", function (e) {
    if (photoTaken && e.touches[0].clientY > $(document).height() * 0.1 && e.touches[0].clientY < $(document).height() * 0.45) {
        $("#top_overlay").css('height', e.touches[0].clientY);
    }
});

$("#bottom_overlay").on("touchmove", function (e) {
    if (photoTaken && $(document).height() - e.touches[0].clientY > $(document).height() * 0.2 && $(document).height() - e.touches[0].clientY < $(document).height() * 0.45) {
        $("#bottom_overlay").css('height', $(document).height() - e.touches[0].clientY);
    }
});

$("#upload-photo").click(function () {
    url = baseurl;

    im = snap.src;
    let data = {
        'x': Math.round(($("#snap").width() - $(document).width()) / 2),
        'y': Math.round($("#top_overlay").height()),
        'width': Math.round($(document).width()),
        'height': Math.round($(document).height() - $('#bottom_overlay').height() - $('#top_overlay').height()),
        'img': im.substring(im.indexOf(',') + 1, im.length),
    }
    state = 2;
    update_view();
    console.log(data)
    $.ajax({
        type: "POST",
        url: url,
        data: data,
        async: true,
        dataType: "json",
        success: function (resultData) {
            console.log('Success');
            console.log('result', resultData);
            update_description(resultData);
        },
    });
});


console.log(delete_photo_btn);

delete_photo_btn.addEventListener("click", function (e) {
    e.preventDefault();
    return_to_pic();
});



function showVideo() {
    // Display the video stream and the controls.

    hideUI();
    video.classList.add("visible");
    controls.classList.add("visible");
}


function takeSnapshot() {
    // Here we're using a trick that involves a hidden canvas element.

    var hidden_canvas = document.querySelector('canvas'),
        context = hidden_canvas.getContext('2d');

    var width = video.clientWidth,
        height = video.clientHeight;

    console.log(width);
    console.log(height);

    if (width && height) {

        // Setup a canvas with the same dimensions as the video.
        hidden_canvas.width = width;
        hidden_canvas.height = height;

        // Make a copy of the current frame in the video on the canvas.
        context.drawImage(video, 0, 0, width, height);

        // Turn the canvas image into a dataURL that can be used as a src for our photo.
        return hidden_canvas.toDataURL('image/png');
    }
}


function displayErrorMessage(error_msg, error) {
    error = error || "";
    if (error) {
        console.log(error);
    }

    error_message.innerText = error_msg;

    hideUI();
    error_message.classList.add("visible");
}


function hideUI() {
    // Helper function for clearing the app UI.
    controls.classList.remove("visible");
    start_camera.classList.remove("visible");
    video.classList.remove("visible");
    snap.classList.remove("visible");
    error_message.classList.remove("visible");
}

var data = [];
var images = [];

function update_description( json ){
    console.log("JSON DATA", json);
    var descrip = '';
    for (let i = 0; i < json.length; i++){
        if (typeof json[i] == "string"){
            descrip += " ".concat(json[i]);
        } else {
            var ch = json[i].desc;
            descrip += ` <u onclick='display_modal("${ch}")'>`.concat(json[i].word).concat("</u>");
        }
    }

    if (json.length <= 1){
        descrip = 'No results found, please retake photo.'
    }

    $("#description").html(descrip);
    data=json;

}

var model_is_displayed = false;
function display_modal(term){
    $("#modal").css("display", "block");
    $("#modal_text").text(term);
    setTimeout(function(){
        model_is_displayed = true;
    }, 500);
}

function close_modal(){
    if (model_is_displayed == true){
        $("#modal").css("display", "none");
        model_is_displayed = false;
    }
}


function return_to_pic(){
    photoTaken = false;

    state = 0;
    update_view();
    // Hide image.
    image.setAttribute('src', "");
    image.classList.remove("visible");

    // Disable delete and save buttons
    delete_photo_btn.classList.add("disabled");
    download_image_btn.classList.add("disabled");
    take_photo_btn.classList.remove("disabled");

    $("#top_overlay").removeAttr('style');
    $("#bottom_overlay").removeAttr('style');

    $('#camera-stream').show();

    // Resume playback of stream.
    video.play();
}

const items = document.querySelectorAll(".accordion a");

function toggleAccordion(){
  this.classList.toggle('active');
  this.nextElementSibling.classList.toggle('active');
}

items.forEach(item => item.addEventListener('click', toggleAccordion));
