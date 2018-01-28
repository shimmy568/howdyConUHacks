var photoTaken = false;

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

console.log('a');
navigator.mediaDevices.enumerateDevices().then(function (sourceInfos) {
    console.log('b');
    var audioSource = null;
    var videoSource = null;
    console.log(sourceInfos);
    for (var i = 0; i != sourceInfos.length; ++i) {
        var sourceInfo = sourceInfos[i];
        if (sourceInfo.kind === 'audio') {
            console.log(sourceInfo.id, sourceInfo.label || 'microphone');

            audioSource = sourceInfo.id;
        } else if (sourceInfo.kind === 'video') {
            console.log(sourceInfo.id, sourceInfo.label || 'camera');

            videoSource = sourceInfo.id;
        } else {
            console.log('Some other kind of source: ', sourceInfo);
        }
    }

    sourceSelected(audioSource, videoSource);
});

// Mobile browsers cannot play video without user input,
// so here we're using a button to start it manually.
start_camera.addEventListener("click", function (e) {

    e.preventDefault();

    // Start video playback manually.
    video.play();
    showVideo();

});


function sourceSelected(audioSource, videoSource) {
    var constraints = {
        audio: {
            optional: [{
                sourceId: audioSource
            }]
        },
        video: {
            optional: [{
                sourceId: videoSource
            }]
        }
    };

    navigator.getUserMedia(constraints, successCallback, errorCallback);
}

if (!navigator.getMedia) {
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

}



// Mobile browsers cannot play video without user input,
// so here we're using a button to start it manually.
start_camera.addEventListener("click", function (e) {

    e.preventDefault();

    // Start video playback manually.
    video.play();
    showVideo();

});


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
    console.log('nani');
});

$("#upload-photo").click(function () {
    url = 'http://127.0.0.1:5000/';
    im = snap.src;

    let data = {
        'x': Math.round(($("#snap").width() - $(document).width()) / 2),
        'y': Math.round($("#top_overlay").height()),
        'width': Math.round($(document).width()),
        'height': Math.round($(document).height() - $('#bottom_overlay').height() - $('#top_overlay').height()),
        'img': im.substring(im.indexOf(',') + 1, im.length),
    }
    console.log(data)
    $.ajax({
        type: "POST",
        url: url,
        data: data,
        dataType: "json",
        success: function (resultData) {
            console.log('Success')
            console.log(resultData)
        },
    });
});

console.log(delete_photo_btn);

delete_photo_btn.addEventListener("click", function (e) {
    console.log("hey");
    e.preventDefault();

    photoTaken = false;

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