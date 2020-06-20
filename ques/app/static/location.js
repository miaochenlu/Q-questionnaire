
var count = 0;
function getLocation(obj) {
    count = obj.parentNode.parentNode.parentNode.id.split('_')[1].split('.')[0];
    // input_lat = document.getElementById("ques_"+count+".lat");
    // input_lng = document.getElementById("ques_"+count+".lng");
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    } else { 
        alert("Geolocation is not supported by this browser.");
    }
}

function getLocation_prime(obj) {
    count = obj.parentNode.parentNode.parentNode.parentNode.id.split('_')[1].split('.')[0];
    // input_lat = document.getElementById("ques_"+count+".lat");
    // input_lng = document.getElementById("ques_"+count+".lng");
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    } else { 
        alert("Geolocation is not supported by this browser.");
    }
}

function showPosition(position) {
    // lat = 0;
    var question_div = document.getElementById("ques_"+count+".div");
    if(document.getElementById("ques_"+count+".lat")) {

    } else {
        var new_div = document.createElement("div");

        var lat_div = document.createElement("div");
        var lng_div = document.createElement("div");

        var input_lat = document.createElement("input");
        var input_lng = document.createElement("input");
        var lab_lat = document.createElement("label");
        var lab_lng = document.createElement("label");

        input_lat.id = "ques_"+count+".lat";
        input_lat.name = "ques_"+count+".lat";
        input_lng.id = "ques_"+count+".lng";
        input_lng.name = "ques_"+count+".lng";
        input_lat.value =  position.coords.latitude.toFixed(2);; 
        input_lng.value = position.coords.longitude.toFixed(2);
        input_lat.step = 0.01;
        input_lng.step = 0.01;
        input_lat.type = "number";
        input_lng.type = "number";
        lab_lat.innerHTML = "经度";
        lab_lng.innerHTML = "纬度";

        lat_div.appendChild(lab_lat);
        lat_div.appendChild(input_lat);

        lng_div.appendChild(lab_lng);
        lng_div.appendChild(input_lng);
        // <input type="number" name="ques_{{i}}.lat" id="ques_{{i}}.lat">  
        // <input type="number" name="ques_{{i}}.lng" id="ques_{{i}}.lng">  
        
        new_div.appendChild(lat_div);
        new_div.appendChild(lng_div);
        question_div.appendChild(new_div);
    }

}