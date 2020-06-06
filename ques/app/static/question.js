function create_question(type){
    var base_div = document.getElementById("question_list");
  // new question div
      var new_question_div = document.createElement("div");
      
      var ques_count = 0;
      while(document.getElementById("ques_" + ques_count + ".div")) 
          ques_count++;
      new_question_div.id = "ques_" + ques_count + ".div";
      new_question_div.name = "ques_" + ques_count + ".div";
      new_question_div.setAttribute("class", "form-group row well");
      new_question_div.setAttribute("onmouseover", "show_buttons(this, 0)");
      new_question_div.setAttribute("onmouseout", "hide_buttons(this, 0)");
    
      //info div
          var info_div = document.createElement("div");
          info_div.style.fontSize = "13px";
          info_div.style.marginLeft = "5px";
          info_div.style.marginTop = "-10px";
          info_div.style.marginBottom = "10px";
              var b = document.createElement("b");
              if(type == 0) b.innerHTML = "问题" + (ques_count+1) + ": 单选题";
              else if(type == 1) b.innerHTML = "问题" + (ques_count+1) + ": 多选题";
              else if(type == 2) b.innerHTML = "问题" + (ques_count+1) + ": 文字题";
              else if(type == 3) b.innerHTML = "问题" + (ques_count+1) + ": 数字题"
              else b.innerHTML = "问题" + (ques_count+1) + ": 评分题";
          info_div.appendChild(b);
      new_question_div.appendChild(info_div);
  // must do
      var must_do_div = document.createElement("div")
          var must_do = document.createElement("input");
          must_do.id = "ques_" + ques_count + ".must_do";
          must_do.name = "ques_" + ques_count + ".must_do";
          must_do.type = "radio";
          must_do.checked = "checked";
          must_do.value = "1";
          must_do.setAttribute("class", "form-check-input")
          must_do_div.appendChild(must_do);

          var mustlabel = document.createElement("Label");
          mustlabel.setAttribute("class", "form-check-label")
          mustlabel.innerHTML = "必做";
          must_do_div.appendChild(mustlabel);

          var option_do = document.createElement("input");
          option_do.id = "ques_" + ques_count + ".option_do";
          option_do.name = "ques_" + ques_count + ".must_do";
          option_do.type = "radio";
          option_do.value = "0"
          option_do.setAttribute("class", "form-check-input")
          must_do_div.appendChild(option_do);
      
          var optionlabel = document.createElement("Label");
          optionlabel.setAttribute("class", "form-check-label")
          optionlabel.innerHTML = "选做";
          
          must_do_div.appendChild(optionlabel);

      must_do_div.setAttribute("class", "form-check form-check-inline")
      must_do_div.style.marginLeft = "5px";
      new_question_div.appendChild(must_do_div);


      var new_question_div_head = document.createElement("div");
      new_question_div_head.setAttribute("class", "row");
      new_question_div.appendChild(new_question_div_head);
    
      
          var new_question_type = document.createElement("input");
          new_question_type.id = "ques_" + ques_count + ".type";
          new_question_type.name = "ques_" + ques_count + ".type";
          new_question_type.type = "Hidden";
          new_question_type.value = type;
      new_question_div_head.appendChild(new_question_type);
      
          var new_question_description_div = document.createElement("div");
          new_question_description_div.setAttribute("class", "col-md-6");
              var new_question_description = document.createElement("input");
              new_question_description.id = "ques_" + ques_count + ".description";
              new_question_description.name = "ques_" + ques_count + ".description";
              new_question_description.type = "text";
              new_question_description.setAttribute("class", "form-control");
              new_question_description.setAttribute("required", "required");
              new_question_description.placeholder = "请输入你的问题";
          new_question_description_div.appendChild(new_question_description);
      new_question_div_head.appendChild(new_question_description_div);
    
      var new_question_div_button = document.createElement("div");
      new_question_div_button.setAttribute("class","ques_button");
      new_question_div_button.style.display = "none";
      new_question_div_head.appendChild(new_question_div_button);
    
      var new_question_delete = document.createElement("span");
      new_question_delete.setAttribute("class", "pull-right btn glyphicon glyphicon-trash");
      new_question_delete.setAttribute("onclick","delete_question(this)");
      new_question_div_button.appendChild(new_question_delete);
    
      var new_question_down = document.createElement("span");
      new_question_down.setAttribute("class", "pull-right btn glyphicon glyphicon glyphicon-arrow-down");
      new_question_down.setAttribute("onclick","move_question(this,1)");
      new_question_div_button.appendChild(new_question_down);
    
      var new_question_up = document.createElement("span");
      new_question_up.setAttribute("class", "pull-right btn glyphicon glyphicon glyphicon-arrow-up");
      new_question_up.setAttribute("onclick","move_question(this,0)");
      new_question_div_button.appendChild(new_question_up);
    
      if (type <2) {
        var new_question_add = document.createElement("span");
        new_question_add.setAttribute("class", "pull-right btn glyphicon glyphicon-plus");
        new_question_add.setAttribute("onclick","add_option(this," + type + ")");
        new_question_div_button.appendChild(new_question_add);
      }
    
      var new_option_ul = document.createElement("ul");
      new_option_ul.setAttribute("class", "form-inline");
      new_option_ul.style.listStyleType = "none";
      new_question_div.appendChild(new_option_ul);
    
      if(type<2){
        new_option_ul.innerHTML = 
        "<li class = \"row\" onmouseover = \"show_buttons(this,1)\" onmouseout = \"hide_buttons(this,1)\"><input class = \"col-md-7 form-control\" type = \"text\" id = \"ques_" + 
        ques_count + ".option_0\" name = \"ques_" + ques_count + ".option_0\" placeholder = \"new option\" required/>" + 
        "<div class = \"col-md-5 option_button\" style = \"display:none\">" + 
        "<span class = \"btn glyphicon glyphicon-arrow-up\" onclick = \"move_option(this,0)\"></span>" + 
        "<span class = \"btn glyphicon glyphicon-arrow-down\" onclick = \"move_option(this,1)\"></span>" + 
        "<span class = \"btn glyphicon glyphicon-trash\" onclick = \"delete_option(this)\"></span></div></li>" + 
        "<li class = \"row\" onmouseover = \"show_buttons(this,1)\" onmouseout = \"hide_buttons(this,1)\"><input class = \"col-md-7 form-control\" type = \"text\" id = \"ques_" + 
        ques_count + ".option_1\" name = \"ques_" + ques_count + ".option_1\" placeholder = \"new option\" required/>" + 
        "<div class = \"col-md-5 option_button\" style = \"display:none\">" + 
        "<span class = \"btn glyphicon glyphicon-arrow-up\" onclick = \"move_option(this,0)\"></span>" + 
        "<span class = \"btn glyphicon glyphicon-arrow-down\" onclick = \"move_option(this,1)\"></span>" + 
        "<span class = \"btn glyphicon glyphicon-trash\" onclick = \"delete_option(this)\"></span></div></li>";
      }

      if(type == 2) {
        new_option_ul.innerHTML = "<li class = \"row\">"+
        "<div class=\"form-check form-check-inline\" style=\"margin-left: 5px;\">"
        + "<input class = \"form-check-input\" type = \"radio\" id = \"ques_" + ques_count + ".one_row\" name= \"ques_" + ques_count + ".row\" value=\"0\" checked>"
        + "<label id=\"ques_" + ques_count + ".row_label1\" class=\"form-check-label\">单行</label>"
        + " <input class = \"form-check-input\" type = \"radio\" id = \"ques_" + ques_count + ".multi_row\" name= \"ques_" + ques_count + ".row\" value=\"1\" >"
        + "<label id=\"ques_" + ques_count + ".row_label2\" class=\"form-check-label\">多行</label></div></li>"
      }
      if(type == 3) {
        new_option_ul.innerHTML = "<li class = \"row\">"+
        "<div class=\"form-check form-check-inline\" style=\"margin-left: 5px;\">"
        + "<input class = \"form-check-input\" type = \"radio\" id = \"ques_" + ques_count + ".integer\" name= \"ques_" + ques_count + ".intordeci\" value=\"0\" checked>"
        + "<label id=\"ques_" + ques_count + ".num_label1\" class=\"form-check-label\">整数</label>"
        + "<input class = \"form-check-input\" type = \"radio\" id = \"ques_" + ques_count + ".decimal\" name= \"ques_" + ques_count + ".intordeci\" value=\"1\" >"
        + "<label id=\"ques_" + ques_count + ".num_label2\" class=\"form-check-label\">小数</label></div></li>"
        + "<li class = \"row\" >"
        + "<input class = \"col-md-7 form-control\" type = \"number\" id = \"ques_" + ques_count + ".minnumber\" name= \"ques_" + ques_count + ".minnumber\" placeholder = \"最小值或最大值\" step=0.01  required/> </li>"
        + "<li class = \"row\" >"
        + "<input class = \"col-md-7 form-control\" type = \"number\" id = \"ques_" + ques_count + ".maxnumber\" name= \"ques_" + ques_count + ".maxnumber\" placeholder = \"最大值或最小值\" step = 0.01  required/> </li>"
      }

      if(type == 4) {
        new_option_ul.innerHTML = "<li class = \"row\" >"+
        " <input class = \"col-md-7 form-control\" type = \"text\" id = \"ques_" + ques_count + ".lefttext\" name= \"ques_" + ques_count + ".lefttext\" placeholder = \"左端描述文字\" required/> </li>"
        + "<li class = \"row\" >"
        + "<input class = \"col-md-7 form-control\" type = \"text\" id = \"ques_" + ques_count + ".righttext\" name= \"ques_" + ques_count + ".righttext\" placeholder = \"右端描述文字\" required/> </li>"
        + "<li class = \"row\" >"
        + "<input style=\"width: 120px;\" class = \"col-md-7 form-control\" type = \"number\" id = \"ques_" + ques_count + ".number\" name= \"ques_" + ques_count + ".number\"  min=\"3\" max=\"10\" placeholder = \"量表级数\" required/> </li>"
      }
    
    base_div.appendChild(new_question_div);
    new_question_description.focus();
}

function delete_question(obj){
    count=obj.parentNode.parentNode.parentNode.id.split('_')[1].split('.')[0];
    var current_question=document.getElementById("ques_"+count+".div");
    current_question.parentNode.removeChild(current_question);
    count++;
    current_question=document.getElementById("ques_"+count+".div");
    while(current_question!=null){
      var question_div=document.getElementById("ques_"+count+".div");
      question_div.id="ques_"+(count-1)+".div";
      question_div.name="ques_"+(count-1)+".div";
      
      var must_do = document.getElementById("ques_"+count+".must_do");
      var option_do = document.getElementById("ques_"+count+".option_do");
      must_do.id = "ques_" + (count - 1) + ".must_do";
      must_do.name = "ques_" + (count - 1) + ".must_do";
      option_do.id = "ques_" + (count - 1) + ".option_do";
      option_do.name = "ques_" + (count - 1) + ".must_do";


      var question_type=document.getElementById("ques_"+count+".type");
      question_type.id="ques_"+(count-1)+".type";
      question_type.name="ques_"+(count-1)+".type";
      var type=question_type.value;
  
      var question_description=document.getElementById("ques_"+count+".description");
      question_description.id="ques_"+(count-1)+".description";
      question_description.name="ques_"+(count-1)+".description";
  
  
      if(type < 2){
        var option_count = 0;
        var current_option=document.getElementById("ques_" + count + ".option_" + option_count);
        while(current_option != null){
          current_option.id = "ques_" + (count-1) + ".option_" + option_count;
          current_option.name = "ques_"+ (count-1) + ".option_" + option_count;
          option_count++;
          current_option = document.getElementById("ques_" + count + ".option_" + option_count);
        }
      }
      if(type == 2) {
        var row_label1 = document.getElementById("ques_" + count + ".row_label1");
        var row_label2 = document.getElementById("ques_" + count + ".row_label2");
        var one_row = document.getElementById("ques_" + count + ".one_row");
        var multi_row = document.getElementById("ques_" + count + ".multi_row");

        row_label1.id = "ques_" + (count - 1) + ".row_label1";
        row_label2.id = "ques_" + (count - 1) + ".row_label2";
        one_row.id = "ques_" + (count - 1) + ".one_row";
        one_row.name = "ques_" + (count - 1) + ".row";
        multi_row.id = "ques_" + (count - 1) + ".multi_row";
        multi_row.name = "ques_" + (count - 1) + ".row";
      }
      if(type == 3) {
        var num_label1 = document.getElementById("ques_" + count + ".num_label1");
        var num_label2 = document.getElementById("ques_" + count + ".num_label2");
        var integer = document.getElementById("ques_" + count + ".integer");
        var decimal = document.getElementById("ques_" + count + ".decimal");
        var min = document.getElementById("ques_" + count + ".minnumber");
        var max = document.getElementById("ques_" + count + ".maxnumber");

        num_label1.id = "ques_" + (count - 1) + ".num_label1";
        num_label2.id = "ques_" + (count - 1) + ".num_label2";
        integer.id = "ques_" + (count - 1) + ".integer";
        integer.name = "ques_" + (count - 1) + ".intordeci";
        decimal.id = "ques_" + (count - 1) + ".decimal";
        decimal.name = "ques_" + (count - 1) + ".decimal";
        min.id = "ques_" + (count - 1) + ".minnumber";
        min.name = "ques_" + (count - 1) + ".minnumber";
        max.id = "ques_" + (count - 1) + ".maxnumber";
        max.name = "ques_" + (count - 1) + ".maxnumber";
        
      }
      if(type == 4) {
        var lefttext = document.getElementById("ques_" + count + ".lefttext");
        var righttext = document.getElementById("ques_" + count + ".righttext");
        var number = document.getElementById("ques_" + count + ".number");
        lefttext.id = "ques_" + (count - 1) + ".lefttext";
        lefttext.name = "ques_" + (count - 1) + ".lefttext";
        righttext.id = "ques_" + (count - 1) + ".righttext";
        righttext.name = "ques_" + (count - 1) + ".righttext";
        number.id = "ques_" + (count - 1) + ".number";
        number.name = "ques_" + (count - 1) + ".number";
      }
      count++;
      current_question = document.getElementById("ques_" + count + ".div");
    }
  }
  
  function move_question(obj,direction){
    var count=obj.parentNode.parentNode.parentNode.id.split('_')[1].split('.')[0];
    var next_count = count;
    if(direction == 1) next_count++;
    else next_count--;
  
    var current_question_div = document.getElementById("ques_" + count + ".div");
    var next_question_div = document.getElementById("ques_" + next_count + ".div");
  
    if(current_question_div == null || next_question_div == null)return;
  
    current_question_div.id = "ques_" + next_count + ".div";
    current_question_div.name="ques_" + next_count + ".div";
    next_question_div.id = "ques_" + count + ".div";
    next_question_div.name="ques_" + count + ".div";
  
    var current_question_type = document.getElementById("ques_" + count + ".type");
    var next_question_type = document.getElementById("ques_" + next_count + ".type");
    current_question_type.id = "ques_" + next_count + ".type";
    current_question_type.name = "ques_" + next_count + ".type";
    next_question_type.id = "ques_" + count + ".type";
    next_question_type.name = "ques_" + count + ".type";
  
    var current_type = current_question_type.value;
    var next_type = next_question_type.value;

        var current_must_do = document.getElementById("ques_"+count+".must_do");
        var current_option_do = document.getElementById("ques_"+count+".option_do");
        var next_must_do = document.getElementById("ques_"+next_count+".must_do");
        var next_option_do = document.getElementById("ques_"+next_count+".option_do");
        
        var current_must_do_check = current_must_do.checked;
        var current_option_do_check = current_option_do.checked;
        var next_must_do_check = next_must_do.checked;
        var next_option_do_check = next_option_do.checked;

        current_must_do.id = "ques_" + next_count + ".must_do";
        current_must_do.name = "ques_" + next_count + ".must_do";
        if( current_must_do_check) {
          current_must_do.checked =  current_must_do_check;
        }
        current_option_do.id = "ques_" + next_count + ".option_do";
        current_option_do.name = "ques_" + next_count + ".must_do";

        if(current_option_do_check) {
          current_option_do.checked = current_option_do_check
        }

        next_must_do.id = "ques_" + count + ".must_do";
        next_must_do.name = "ques_" + count + ".must_do";
        if(next_must_do_check){
          next_must_do.checked = next_must_do_check;
        }
        next_option_do.id = "ques_" + count + ".option_do";
        next_option_do.name = "ques_" + count + ".must_do";
        if(next_option_do_check) {
          next_option_do.checked = next_option_do_check;
        }



    var current_question_description = document.getElementById("ques_" + count + ".description");
    var next_question_description = document.getElementById("ques_" + next_count + ".description");
    current_question_description.id = "ques_" + next_count + ".description";
    current_question_description.name = "ques_" + next_count + ".description";
    next_question_description.id = "ques_" + count + ".description";
    next_question_description.name = "ques_" + count + ".description";
  
  /*************为选择题设置*************/
    var option_count = 0;
    var current_option = document.getElementById("ques_" + count + ".option_" + option_count);
    var next_option = document.getElementById("ques_" + next_count + ".option_" + option_count);
  /*----------------------------*/

  /*************为评分题设置*************/
    var current_score_lefttext = document.getElementById("ques_" + count + ".lefttext");
    var current_score_righttext = document.getElementById("ques_" + count + ".righttext");
    var current_score_number = document.getElementById("ques_" + count + ".number");

    var next_score_lefttext = document.getElementById("ques_" + next_count + ".lefttext");
    var next_score_righttext = document.getElementById("ques_" + next_count + ".righttext");
    var next_score_number = document.getElementById("ques_" + next_count + ".number");
  /*----------------------------*/

    var current_row_label1 = document.getElementById("ques_" + count + ".row_label1");
    var current_row_label2 = document.getElementById("ques_" + count + ".row_label2");
    var current_one_row = document.getElementById("ques_" + count + ".one_row");
    var current_multi_row = document.getElementById("ques_" + count + ".multi_row");

    var next_row_label1 = document.getElementById("ques_" + next_count + ".row_label1");
    var next_row_label2 = document.getElementById("ques_" + next_count + ".row_label2");
    var next_one_row = document.getElementById("ques_" + next_count + ".one_row");
    var next_multi_row = document.getElementById("ques_" + next_count + ".multi_row");
    
    var current_one_row_check;
    var current_multi_row_check;
    var next_one_row_check;
    var next_multi_row_check;
  
    if(current_one_row) {
      current_one_row_check = current_one_row.checked;
      current_multi_row_check = current_multi_row.checked;
    }
    if(next_one_row) {
      next_one_row_check = next_one_row.checked;
      next_multi_row_check = next_multi_row.checked;
    }


    var current_num_label1 = document.getElementById("ques_" + count + ".num_label1");
    var current_num_label2 = document.getElementById("ques_" + count + ".num_label2");
    var current_integer = document.getElementById("ques_" + count + ".integer");
    var current_decimal = document.getElementById("ques_" + count + ".decimal");
    var current_min = document.getElementById("ques_" + count + ".minnumber");
    var current_max = document.getElementById("ques_" + count + ".maxnumber");

    var next_num_label1 = document.getElementById("ques_" + next_count + ".num_label1");
    var next_num_label2 = document.getElementById("ques_" + next_count + ".num_label2");
    var next_integer  = document.getElementById("ques_" + next_count + ".integer");
    var next_decimal= document.getElementById("ques_" + next_count + ".decimal");
    var next_min = document.getElementById("ques_" + next_count + ".minnumber");
    var next_max = document.getElementById("ques_" + next_count + ".maxnumber");

    var current_integer_check;
    var current_decimal_check;
    var next_integer_check;
    var next_decimal_check;
  
    if(current_integer) {
      current_integer_check = current_integer.checked;
      current_decimal_check = current_decimal.checked;
    }
    if(next_integer) {
      next_integer_check = next_integer.checked;
      next_decimal_check = next_decimal.checked;
    }

    if(current_type == 2) {
        current_row_label1.id = "ques_" + next_count + ".row_label1";
        current_row_label2.id = "ques_" + next_count + ".row_label2";
        current_one_row.id = "ques_" + next_count + ".one_row";
        current_one_row.name = "ques_" + next_count + ".row";
        current_multi_row.id = "ques_" + next_count + ".multi_row";
        current_multi_row.name = "ques_" + next_count + ".row";
        
        if(current_one_row_check) {
          current_one_row.checked = current_one_row_check;
        }
        if(current_multi_row_check) {
          current_multi_row.checked = current_multi_row_check;
        }
    }
    if(current_type == 3) {
      current_num_label1.id = "ques_" + next_count + ".num_label1";
      current_num_label2.id = "ques_" + next_count + ".num_label2";
      current_integer.id = "ques_" + next_count + ".integer";
      current_integer.name = "ques_" + next_count + ".intordeci";
      current_decimal.id = "ques_" + next_count + ".decimal";
      current_decimal.name = "ques_" + next_count + ".intordeci";
      current_min.id = "ques_" + next_count + ".minnumber";
      current_min.name = "ques_" + next_count + ".minnumber";
      current_max.id = "ques_" + next_count + ".maxnumber";
      current_max.name = "ques_" + next_count + ".maxnumber";

      if(current_integer_check) {
        current_integer.checked = current_integer_check;
      }
      if(current_decimal_check) {
        current_decimal.checked = current_decimal_check;
      }
    }
    if(current_type == 4) {
        current_score_lefttext.id = "ques_" + next_count + ".lefttext";
        current_score_lefttext.name = "ques_" + next_count + ".lefttext";

        current_score_righttext.id = "ques_" + next_count + ".righttext";
        current_score_righttext.name = "ques_" + next_count + ".righttext";

        current_score_number.id = "ques_" + next_count + ".number";
        current_score_number.name = "ques_" + next_count + ".number";
    }
    if(current_type < 2){
        if(next_type < 2){
            while(current_option != null && next_option != null){
              current_option.id="ques_"+next_count+".option_"+option_count;
              current_option.name="ques_"+next_count+".option_"+option_count;
              next_option.id="ques_"+count+".option_"+option_count;
              next_option.name="ques_"+count+".option_"+option_count;
              option_count++;
              current_option=document.getElementById("ques_"+count+".option_"+option_count);
              next_option=document.getElementById("ques_"+next_count+".option_"+option_count);
            }
            while(current_option!=null){
              current_option.id="ques_"+next_count+".option_"+option_count;
              current_option.name="ques_"+next_count+".option_"+option_count;
              option_count++;
              current_option=document.getElementById("ques_"+count+".option_"+option_count);
            }
            while(next_option!=null){
              next_option.id="ques_"+count+".option_"+option_count;
              next_option.name="ques_"+count+".option_"+option_count;
              option_count++;
              next_option=document.getElementById("ques_"+next_count+".option_"+option_count);
            }
        }
        else {
          while(current_option!=null){
            current_option.id="ques_"+next_count+".option_"+option_count;
            current_option.name="ques_"+next_count+".option_"+option_count;
            option_count++;
            current_option=document.getElementById("ques_"+count+".option_"+option_count);
        }   
      }
    }
    if(next_type < 2 && current_type > 2){
        while(next_option!=null){
            next_option.id="ques_"+count+".option_"+option_count;
            next_option.name="ques_"+count+".option_"+option_count;
            option_count++;
            next_option=document.getElementById("ques_"+next_count+".option_"+option_count);
        }
    } 
    if(next_type == 4) {
        next_score_lefttext.id = "ques_" + count + ".lefttext";
        next_score_lefttext.name = "ques_" + count + ".lefttext";
        next_score_righttext.id = "ques_" + count + ".righttext";
        next_score_righttext.name = "ques_" + count + ".righttext";
        next_score_number.id = "ques_" + count + ".number";
        next_score_number.name = "ques_" + count + ".number";
    }
    if(next_type == 2) {
        next_row_label1.id = "ques_" + count + ".row_label1";
        next_row_label2.id = "ques_" + count + ".row_label2";
        next_one_row.id = "ques_" + count + ".one_row";
        next_one_row.name = "ques_" + count + ".row";
        next_multi_row.id = "ques_" + count + ".multi_row";
        next_multi_row.name = "ques_" + count + ".row";

        // if(next_one_row_check) {
        //   next_one_row.checked = next_one_row_check;
        // }
        // if(next_multi_row_check) {
        //   next_multi_row.checked = next_multi_row_check;
        // }

    }
    if(next_type == 3) {
      next_num_label1.id = "ques_" + count + ".num_label1";
      next_num_label2.id = "ques_" + count + ".num_label2";
      next_integer.id = "ques_" + count + ".integer";
      next_integer.name = "ques_" + count + ".intordeci";
      next_decimal.id = "ques_" + count + ".decimal";
      next_decimal.name = "ques_" + count + ".intordeci";
      next_min.id = "ques_" + count + ".minnumber";
      next_min.name = "ques_" + count + ".minnumber";
      next_max.id = "ques_" + count + ".maxnumber";
      next_max.name = "ques_" + count + ".maxnumber";

      // if(next_integer_check) {
      //   next_integer.checked = next_integer_check;
      // }
      // if(next_decimal_check) {
      //   next_decimal.checked = next_decimal_check;
      // }
    }
    if(direction==0)$(current_question_div).insertBefore($(next_question_div));
    else $(next_question_div).insertBefore($(current_question_div));
}
  
function add_option(obj,type){
    var count=obj.parentNode.parentNode.parentNode.id.split('_')[1].split('.')[0];
    var ul=obj.parentNode.parentNode.nextSibling;
    var ocount = 0;
    var radio;
    if(type == 0)radio="radio";
    else radio="checkbox";
    while(document.getElementById("ques_"+count+".option_"+ocount)!=null)ocount++;

    console.log(count)

    var li=document.createElement("li");
    li.setAttribute("onmouseover","show_buttons(this,1)");
    li.setAttribute("onmouseout","hide_buttons(this,1)");
  
    li.setAttribute("class","row");
    li.innerHTML="<input class=\"col-md-7 form-control\" type=\"text\" id=\"ques_"+
      count+".option_"+ocount+"\" name=\"ques_"+count+".option_"+ocount+"\" placeholder=\"new option\" required/>"+
      "<div style=\"display:none\" class=\"col-md-5 option_button\">"+
  
      "<span class=\"btn glyphicon glyphicon-arrow-up\" onclick=\"move_option(this,0)\"></span>"+
    "<span class=\"btn glyphicon glyphicon-arrow-down\" onclick=\"move_option(this,1)\"></span>"+
      "<span class=\"btn glyphicon glyphicon-trash\" onclick=\"delete_option(this)\"></span></div>";
    ul.appendChild(li);
    document.getElementById("ques_"+count+".option_"+ocount).focus();
}
  
function delete_option(obj){
    var option=obj.parentNode.previousSibling;
    var li=option.parentNode;
    var ul=li.parentNode;
    var ques_count=option.id.split('_')[1].split('.')[0];
    var option_count=option.id.split('_')[2];
    ul.removeChild(li);
  
    option_count++;
    var current_option=document.getElementById("ques_"+ques_count+".option_"+option_count);
    while(current_option!=null){
      current_option.id="ques_"+ques_count+".option_"+(option_count-1);
      current_option.name="ques_"+ques_count+".option_"+(option_count-1);
      option_count++;
      current_option=document.getElementById("ques_"+ques_count+".option_"+option_count);
    }
}
  
function move_option(obj,direction){
    var option=obj.parentNode.previousSibling;
    var ques_count=option.id.split('_')[1].split('.')[0];
    var option_count=option.id.split('_')[2];
    var next_count=option_count;
    if(direction==1){
      next_count++;
    }
    else{
      next_count--;
    } 
    var current_option=document.getElementById("ques_"+ques_count+".option_"+option_count);
    var next_option=document.getElementById("ques_"+ques_count+".option_"+next_count);
    if(current_option==null||next_option==null)return;
    current_option.id="ques_"+ques_count+".option_"+next_count;
    current_option.name="ques_"+ques_count+".option_"+next_count;
    next_option.id="ques_"+ques_count+".option_"+option_count;
    next_option.name="ques_"+ques_count+".option_"+option_count;
    var current_li=$(current_option.parentNode);
    var next_li=$(next_option.parentNode);
    if(direction==0)current_li.insertBefore(next_li);
    else next_li.insertBefore(current_li);
}
  
function show_buttons(obj,type){
    var str;
    if(type==0)str=".ques_button";
    else str=".option_button";
    $(str,obj).each(function(){
      $(this).show()
    });
}

function hide_buttons(obj,type){
    var str;
    if(type==0)str=".ques_button";
    else str=".option_button";
    $(str,obj).each(function(){
      $(this).hide()
    });
}


function move_option_prime(obj,direction){
  var option=obj.parentNode.previousSibling.previousSibling;
  var ques_count=option.id.split('_')[1].split('.')[0];
  var option_count=option.id.split('_')[2];
  var next_count=option_count;
  if(direction==1){
    next_count++;
  }
  else{
    next_count--;
  } 
  var current_option=document.getElementById("ques_"+ques_count+".option_"+option_count);
  var next_option=document.getElementById("ques_"+ques_count+".option_"+next_count);
  if(current_option==null||next_option==null)return;
  current_option.id="ques_"+ques_count+".option_"+next_count;
  current_option.name="ques_"+ques_count+".option_"+next_count;
  next_option.id="ques_"+ques_count+".option_"+option_count;
  next_option.name="ques_"+ques_count+".option_"+option_count;
  var current_li=$(current_option.parentNode);
  var next_li=$(next_option.parentNode);
  if(direction==0)current_li.insertBefore(next_li);
  else next_li.insertBefore(current_li);
}

function delete_option_prime(obj){
  var option=obj.parentNode.previousSibling.previousSibling;
  var li=option.parentNode;
  var ul=li.parentNode;
  var ques_count=option.id.split('_')[1].split('.')[0];
  var option_count=option.id.split('_')[2];
  ul.removeChild(li);

  option_count++;
  var current_option=document.getElementById("ques_"+ques_count+".option_"+option_count);
  while(current_option!=null){
    current_option.id="ques_"+ques_count+".option_"+(option_count-1);
    current_option.name="ques_"+ques_count+".option_"+(option_count-1);
    option_count++;
    current_option=document.getElementById("ques_"+ques_count+".option_"+option_count);
  }
}

function add_option_prime(obj,type){
  var count=obj.parentNode.parentNode.parentNode.id.split('_')[1].split('.')[0];
  var ul=obj.parentNode.parentNode.nextSibling.nextSibling;
  var ocount = 0;
  var radio;
  if(type == 0)radio="radio";
  else radio="checkbox";
  while(document.getElementById("ques_"+count+".option_"+ocount)!=null)ocount++;

  console.log(count)

  var li=document.createElement("li");
  li.setAttribute("onmouseover","show_buttons(this,1)");
  li.setAttribute("onmouseout","hide_buttons(this,1)");

  li.setAttribute("class","row");
  li.innerHTML="<input class=\"col-md-7 form-control\" type=\"text\" id=\"ques_"+
    count+".option_"+ocount+"\" name=\"ques_"+count+".option_"+ocount+"\" placeholder=\"new option\" required/>"+
    "<div style=\"display:none\" class=\"col-md-5 option_button\">"+

    "<span class=\"btn glyphicon glyphicon-arrow-up\" onclick=\"move_option(this,0)\"></span>"+
    "<span class=\"btn glyphicon glyphicon-arrow-down\" onclick=\"move_option(this,1)\"></span>"+
    "<span class=\"btn glyphicon glyphicon-trash\" onclick=\"delete_option(this)\"></span></div>";
  ul.appendChild(li);
  document.getElementById("ques_"+count+".option_"+ocount).focus();
}