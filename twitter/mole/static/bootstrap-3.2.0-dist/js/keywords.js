/**
 * Created by erica on 03/03/15.
 */

var count;

function cloneDiv(){
    count = parseInt($(".clone_div").last().attr("index")) + 1;
    var _div = $("#clone_div").clone();
    _div.attr("id","clone_div_" + count)
    _div.attr("index", count)
    $("#clone_div").parent().append("<div>").append(_div).append("</div>");

    var obj = $("#clone_div_" + count).find("input");
    setObjectAttr(obj, "keywords");

    count += 1;
}

function setObjectAttr(ojb,name) {
    ojb.setAttribute("id", name + "[" + count + "]");
    ojb.setAttribute("name", name + "[" + count + "]");
    ojb.value = "";
}

function removeButton(button){
    if($('input[type=text].keywords').length > 1){
        button.parent().parent().parent().remove();
    }
}
