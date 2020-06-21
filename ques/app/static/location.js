
var count = 0;
var map;
var point;
var geolocation;
var gc;



function getLocation(obj) {
    count = obj.parentNode.parentNode.parentNode.id.split('_')[1].split('.')[0];
    map = new BMap.Map("ques_" + count + ".map");
    point = new BMap.Point(120.0, 30);
    map.centerAndZoom("杭州" ,12);

    map.addEventListener("click",function(e){
        map.clearOverlays();
        var marker = new BMap.Marker(e.point);

        map.addOverlay(marker);
        map.panTo(e.point);
        {
            var question_div = document.getElementById("ques_"+count+".div");
            if(document.getElementById("ques_"+count+".lat")) {
                var input_lat = document.getElementById("ques_"+count+".lat");
                var input_lng = document.getElementById("ques_"+count+".lng");
                input_lat.value =  e.point.lat; 
                input_lng.value = e.point.lng;
            } else {
            }
        }
    });
    
    geolocation = new BMap.Geolocation();  
    gc = new BMap.Geocoder(); 


    geolocation.getCurrentPosition( function(r) {   //定位结果对象会传递给r变量
 
        if(this.getStatus() == BMAP_STATUS_SUCCESS) {  //通过Geolocation类的getStatus()可以判断是否成功定位。
            var pt = r.point;  
            gc.getLocation(pt, function(rs){  
                var addComp = rs.addressComponents;  
            });

            {
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
                    input_lat.value =  r.point.lat; 
                    input_lng.value = r.point.lng;
                    input_lat.step = 0.01;
                    input_lng.step = 0.01;
                    input_lat.type = "number";
                    input_lng.type = "number";
                    lab_lat.innerHTML = "纬度";
                    lab_lng.innerHTML = "经度";

                    lng_div.appendChild(lab_lng);
                    lng_div.appendChild(input_lng);
                    
                    lat_div.appendChild(lab_lat);
                    lat_div.appendChild(input_lat);
                    
                    new_div.appendChild(lat_div);
                    new_div.appendChild(lng_div);
                    question_div.appendChild(new_div);
                }
            }
        }
        else  {
            //关于状态码  
            //BMAP_STATUS_SUCCESS   检索成功。对应数值“0”。  
            //BMAP_STATUS_CITY_LIST 城市列表。对应数值“1”。  
            //BMAP_STATUS_UNKNOWN_LOCATION  位置结果未知。对应数值“2”。  
            //BMAP_STATUS_UNKNOWN_ROUTE 导航结果未知。对应数值“3”。  
            //BMAP_STATUS_INVALID_KEY   非法密钥。对应数值“4”。  
            //BMAP_STATUS_INVALID_REQUEST   非法请求。对应数值“5”。  
            //BMAP_STATUS_PERMISSION_DENIED 没有权限。对应数值“6”。(自 1.1 新增)  
            //BMAP_STATUS_SERVICE_UNAVAILABLE   服务不可用。对应数值“7”。(自 1.1 新增)  
            //BMAP_STATUS_TIMEOUT   超时。对应数值“8”。(自 1.1 新增)  
            switch( this.getStatus() )
            {
                case 2:
                    alert( '位置结果未知 获取位置失败.' );
                break;
                case 3:
                    alert( '导航结果未知 获取位置失败..' );
                break;
                case 4:
                    alert( '非法密钥 获取位置失败.' );
                break;
                case 5:
                    alert( '对不起,非法请求位置  获取位置失败.' );
                break;
                case 6:
                    alert( '对不起,当前 没有权限 获取位置失败.' );
                break;
                case 7:
                    alert( '对不起,服务不可用 获取位置失败.' );
                break;
                case 8:
                    alert( '对不起,请求超时 获取位置失败.' );
                break;
                
            }
        }        

    },
    {enableHighAccuracy: true}
    )


}


function getLocation_prime(obj) {
    count = obj.parentNode.parentNode.parentNode.parentNode.id.split('_')[1].split('.')[0];
    map = new BMap.Map("ques_" + count + ".map");
    point = new BMap.Point(120.0, 30);
    map.centerAndZoom("杭州" ,12);

    map.addEventListener("click",function(e){
        map.clearOverlays();
        var marker = new BMap.Marker(e.point);

        map.addOverlay(marker);
        map.panTo(e.point);
        {
            var question_div = document.getElementById("ques_"+count+".div");
            if(document.getElementById("ques_"+count+".lat")) {
                var input_lat = document.getElementById("ques_"+count+".lat");
                var input_lng = document.getElementById("ques_"+count+".lng");
                input_lat.value =  e.point.lat; 
                input_lng.value = e.point.lng;
            } else {
            }
        }
    });
    
    geolocation = new BMap.Geolocation();  
    gc = new BMap.Geocoder(); 


    geolocation.getCurrentPosition( function(r) {   //定位结果对象会传递给r变量
 
        if(this.getStatus() == BMAP_STATUS_SUCCESS) {  //通过Geolocation类的getStatus()可以判断是否成功定位。
            var pt = r.point;  
            gc.getLocation(pt, function(rs){  
                var addComp = rs.addressComponents;  
            });

            {
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
                    input_lat.value =  r.point.lat; 
                    input_lng.value = r.point.lng;
                    input_lat.step = 0.01;
                    input_lng.step = 0.01;
                    input_lat.type = "number";
                    input_lng.type = "number";
                    lab_lat.innerHTML = "纬度";
                    lab_lng.innerHTML = "经度";

                    lng_div.appendChild(lab_lng);
                    lng_div.appendChild(input_lng);
                    
                    lat_div.appendChild(lab_lat);
                    lat_div.appendChild(input_lat);
                    
                    new_div.appendChild(lat_div);
                    new_div.appendChild(lng_div);
                    question_div.appendChild(new_div);
                }
            }
        }
        else  {
            //关于状态码  
            //BMAP_STATUS_SUCCESS   检索成功。对应数值“0”。  
            //BMAP_STATUS_CITY_LIST 城市列表。对应数值“1”。  
            //BMAP_STATUS_UNKNOWN_LOCATION  位置结果未知。对应数值“2”。  
            //BMAP_STATUS_UNKNOWN_ROUTE 导航结果未知。对应数值“3”。  
            //BMAP_STATUS_INVALID_KEY   非法密钥。对应数值“4”。  
            //BMAP_STATUS_INVALID_REQUEST   非法请求。对应数值“5”。  
            //BMAP_STATUS_PERMISSION_DENIED 没有权限。对应数值“6”。(自 1.1 新增)  
            //BMAP_STATUS_SERVICE_UNAVAILABLE   服务不可用。对应数值“7”。(自 1.1 新增)  
            //BMAP_STATUS_TIMEOUT   超时。对应数值“8”。(自 1.1 新增)  
            switch( this.getStatus() )
            {
                case 2:
                    alert( '位置结果未知 获取位置失败.' );
                break;
                case 3:
                    alert( '导航结果未知 获取位置失败..' );
                break;
                case 4:
                    alert( '非法密钥 获取位置失败.' );
                break;
                case 5:
                    alert( '对不起,非法请求位置  获取位置失败.' );
                break;
                case 6:
                    alert( '对不起,当前 没有权限 获取位置失败.' );
                break;
                case 7:
                    alert( '对不起,服务不可用 获取位置失败.' );
                break;
                case 8:
                    alert( '对不起,请求超时 获取位置失败.' );
                break;
                
            }
        }        

    },
    {enableHighAccuracy: true}
    )


}


// function showPosition(position) {
//     // lat = 0;
//     var question_div = document.getElementById("ques_"+count+".div");
//     if(document.getElementById("ques_"+count+".lat")) {

//     } else {
//         var new_div = document.createElement("div");

//         var lat_div = document.createElement("div");
//         var lng_div = document.createElement("div");

//         var input_lat = document.createElement("input");
//         var input_lng = document.createElement("input");
//         var lab_lat = document.createElement("label");
//         var lab_lng = document.createElement("label");

//         input_lat.id = "ques_"+count+".lat";
//         input_lat.name = "ques_"+count+".lat";
//         input_lng.id = "ques_"+count+".lng";
//         input_lng.name = "ques_"+count+".lng";
//         input_lat.value =  position.coords.latitude.toFixed(2);; 
//         input_lng.value = position.coords.longitude.toFixed(2);
//         input_lat.step = 0.01;
//         input_lng.step = 0.01;
//         input_lat.type = "number";
//         input_lng.type = "number";
//         lab_lat.innerHTML = "纬度";
//         lab_lng.innerHTML = "经度";

//         lng_div.appendChild(lab_lng);
//         lng_div.appendChild(input_lng);
        
//         lat_div.appendChild(lab_lat);
//         lat_div.appendChild(input_lat);

//         // <input type="number" name="ques_{{i}}.lat" id="ques_{{i}}.lat">  
//         // <input type="number" name="ques_{{i}}.lng" id="ques_{{i}}.lng">  
        
//         new_div.appendChild(lat_div);
//         new_div.appendChild(lng_div);
//         question_div.appendChild(new_div);
//     }

// }
