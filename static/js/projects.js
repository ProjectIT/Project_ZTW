// TODO add better error markers ?
// TODO add confirmation dialogs

$(document).ready(function() {
    checkIfTaskTableShouldBeHidden();
});

var tasksToRemove = [];
var peopleToRemove = [];
var peopleToAdd = [];
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
    d += "&peopleToAdd=" + JSON.stringify(peopleToAdd);
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

/*
 * add person to the project
 */
$("#person-add").click(function() {
    $("#assignment-dialog").show();
});

$("#assignment-dialog-close").click(function() {
    $("#assignment-dialog").hide();
});

$(".assignment-list-item").click(function() {
    var id = $(this).data("person-id");
    console.log("add person: " + id);
    $("#assignment-dialog").hide();
    peopleToAdd.push(id);

    // show in form
    var imgSrc = $(this).find("img").attr("src");
    var name = $(this).find(".assignement-name").html();
    // $("#assign-img").attr("src", imgSrc);
    // $("#assign-name").html(name);
    var s = '<li class="people-list-item" data-person-id="' + id + '">';
    s += '<p class="just-added">';
    s += '<span class="glyphicon glyphicon-bookmark"></span>';
    s += '<p>';
    s += '<img src="' + imgSrc + '">';
    s += name + '</li>';
    // $("#people-list").html($("#people-list").html() + s);
    $("#people-list").append(s);
});

/*
 * slider
 */
$('#__id_complete').slider({
    tooltip: 'hide'
});

$("#__id_complete").on('slide', function(slideEvt) {
    $("#completion-slider-val").text(slideEvt.value + "% complete");
    $("#id_abc").val(slideEvt.value);
});
//$("#__id_complete").slider('setValue', $("#__id_complete").slider('getValue') );