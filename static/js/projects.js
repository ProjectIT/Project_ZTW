// TODO add better error markers ?
// TODO add confirmation dialogs

$(document).ready(function() {
    checkIfTaskTableShouldBeHidden();
});

var tasksToRemove = [];
var peopleToRemove = [];
var filesToRemove = [];

function createProject(url) {
    var d = $('#project-form').serialize(); // get the form data
    $.ajax(url, {
        data: d,
        type: 'POST',
        success: function(response) {
            var json = $.parseJSON(response);
            window.location = json.id; // ?!
        },
        error: function(xhr, textStatus, errorThrown) {
            //console.log(textStatus + "::" + errorThrown + "->" + xhr.responseText);
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

function editProject(url, readProject_url) {
    console.log("project edit");
    var d = $('#project-form').serialize(); // get the form data
    d += "&tasksToRemove=" + JSON.stringify(tasksToRemove)
    d += "&peopleToRemove=" + JSON.stringify(peopleToRemove)
    d += "&filesToRemove=" + JSON.stringify(filesToRemove)
    $.ajax(url, {
        data: d,
        type: 'POST',
        success: function(response) {
            var json = $.parseJSON(response);
            window.location = readProject_url;
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

$(".task-remove").click(function() {
    var row = $(this).parent();
    var tid = row.data("task-id");
    console.log("removing task: " + tid);
    tasksToRemove.push(tid);
    row.remove();

    checkIfTaskTableShouldBeHidden();
});

function checkIfTaskTableShouldBeHidden() {
    var rows = $("#tasks-table tr").length;
    //console.log(rows);
    if (rows == 1) { // account for headers row
        $("#tasks-table").remove();
    }
}

$("p.person-remove").click(function() {
    var personView = $(this).parent("li");
    var id = personView.data("person-id");
    console.log("removing person: " + id);
    peopleToRemove.push(id);
    personView.remove();
});

$(".file-remove").click(function() {
    var view = $(this).parent("li");
    var id = view.data("file-id");
    console.log("removing file: " + id);
    filesToRemove.push(id);
    view.remove();
});


$('#__id_complete').slider({
    tooltip: 'hide'
});

$("#__id_complete").on('slide', function(slideEvt) {
    $("#completion-slider-val").text(slideEvt.value + "% complete");
    $("#id_abc").val(slideEvt.value);
});
//$("#__id_complete").slider('setValue', $("#__id_complete").slider('getValue') );