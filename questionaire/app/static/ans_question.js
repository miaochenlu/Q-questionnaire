function judge_display(obj){
    // ques_{{i}}.ans-{{j}}
    var ques_loc = obj.id.split('_')[1].split('.')[0];
    var option_loc = obj.id.split('-')[1];

    var i = 0; i = ques_loc;
    i++;
    var ques_div = document.getElementById("ques_" + i + ".div");

    while(ques_div != null) {
        var ques_select_div = document.getElementById("ques_" + i + ".ques_select.div");
        if(ques_select_div != null) {
            var select_ques = document.getElementById("ques_" + i + ".ques_select");
            var select_option = document.getElementById("ques_" + i + ".option_select");
            var ques_value = select_ques.value;
            var option_value = select_option.value;
            if(ques_loc == ques_value) {
                if(option_loc == option_value) {
                    ques_div.style.display = 'block';
                }
                else {
                    ques_div.style.display = 'none';
                }
            }
        } 
        i++;
        ques_div = document.getElementById("ques_" + i + ".div");
    }
}