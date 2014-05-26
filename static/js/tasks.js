var filesToRemove = [];

function createTask(url) {
    var d = $('#task-form').serialize(); // get the form data
    $.ajax(url, {
        data: d,
        type: 'POST',
        success: function(response) {
            var json = $.parseJSON(response);
            window.location = "/task/"+json.id; // TODO hardcoded url
        },
        error: function(xhr, textStatus, errorThrown) {
            try {
                var json = $.parseJSON(xhr.responseText);
                if ('fields' in json) {
                    console.log(json.fields);
                    for (var f in json.fields) {
                        $('input[name="' + json.fields[f] + '"]').parent().addClass("has-error");
                    }
                }
            } catch (err) {
                alert("Unrecognised error " + xhr.status + " " + errorThrown);
            }
        }
    });
}

function editTask(url, readTask_url) {
    console.log("task edit");
    var d = $('#task-form').serialize(); // get the form data
    d += "&personResponsibleId=" + JSON.stringify($("#assign-img-div").data("person-id"))
    d += "&filesToRemove=" + JSON.stringify(filesToRemove)
    $.ajax(url, {
        data: d,
        type: 'POST',
        success: function(response) {
            var json = $.parseJSON(response);
            window.location = readTask_url;
        },
        error: function(xhr, textStatus, errorThrown) {
            try {
                var json = $.parseJSON(xhr.responseText);
                if ('fields' in json) {
                    for (var f in json.fields) {
                        $('input[name="' + json.fields[f] + '"]').parent().addClass("has-error");
                    }
                }
            } catch (err) {
                alert("Unrecognised error " + xhr.status + " " + errorThrown);
            }
        }
    });
}

$(".assignment-list-item").click(function() {
    var id = $(this).data("person-id");
    personResponsibleId = id;
    console.log("settings asignee: " + personResponsibleId);
    $("#assignment-dialog").hide();

    // show in form
    $("#assign-img-div").css("display", "block");
    var imgSrc = $(this).find("img").attr("src");
    var name = $(this).find(".assignement-name").html();
    $("#assign-img").attr("src", imgSrc);
    $("#assign-name").html(name);
});

$("#assign-person").click(function(){
    $("#assignment-dialog").show();
});

$("#assignment-dialog-close").click(function(){
     $("#assignment-dialog").hide();
});

$("p.person-remove").click(function() {
    console.log("removing person: " + $("#assign-img-div").data("person-id"));
    $("#assign-img-div").data("person-id", -1);
    $("#assign-img-div").hide();
});

$(".file-remove").click(function() {
    var view = $(this).parent("li");
    var id = view.data("file-id");
    console.log("removing file: " + id);
    filesToRemove.push(id);
    view.remove();
});