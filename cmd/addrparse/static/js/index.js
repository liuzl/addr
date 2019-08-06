$(document).ready(function() {
    var text = GetQueryString("text");
    if (text != null) {
        $('#text').val(text);
        Parse(text);
    }
    $('#submit').click(function() {
        var text = $('#text').val().trim();
        if (text != "") {
            Parse(text);
        }
    });
    $("#text").on('keypress', function(e) {
        if (e.keyCode != 13) return;
        var text = $('#text').val().trim();
        if (text != "") {
            Parse(text);
        }
    });
});

function Parse(text) {
    $('#editor_holder').html("<h4>loading...</h4>");
    $("#visual").html("<h4>loading...</h4>");
    $.ajax({
        url: "./api?text="+encodeURIComponent(text), cache: false,
        success: function(result) {
            $('#editor_holder').jsonview(result);
            visual(result);
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            alert(XMLHttpRequest.responseText);
        }
    });
}

function one(k, v) {
    return "<fieldset><legend class=\"label label-info left\">"+
        k+"</legend>"+v+"</fieldset>";
}

function visual(doc) {
    if (doc["status"] != "ok") {
        return "<h4>ERROR</h4>";
    }
    doc = doc["message"];
    var html = "";
    for (var i = 0; i < doc.length; i++) {
        var k = "result " + (i+1);
        var v = "";
        for (k2 in doc[i]) {
            vv = doc[i][k2];
            if (k2 == "address") {
                var x = "";
                for (var j = 0; j < vv.length; j++) {
                    var kj = "item " + (j+1);
                    var vj = "";
                    for (k3 in vv[j]) {
                        vj += one(k3, vv[j][k3]);
                    }
                    x += one(kj, vj);
                }
                vv = x;
            }
            v += one(k2, vv);
        }
        html += one(k, v);
    }
    $("#visual").html(html);
}

