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
    // "csrfmiddlewaretoken=7agqY8aEZdUVrKmCwXLRjZdVwWPmQVIK&name=Project+A&__complete=&complete=40&description=Lorem+ipsum+dolor+sit+amet%2C+consectetur+adipiscing+elit.+Sed+condimentum+vel+neque+eget+iaculis.+Mauris+placerat+consectetur+leo+eget+tempus.+Nullam+porta+lacinia+metus%2C+in+laoreet+lectus+cursus+a.+Praesent+condimentum+ligula+vitae+tellus+vehicula%2C+non+sodales+lectus+ultricies.+Sed+nunc+nisi%2C+pulvinar+eget+pulvinar+nec%2C+posuere+sed+arcu.+Vivamus+et+lacus+ut+est+facilisis+faucibus+at+quis+ligula.+Aliquam+scelerisque+dolor+lorem%2C+ut+blandit+libero+dapibus+id.+Duis+risus+felis%2C+mattis+nec+consequat+non%2C+pellentesque+a+sem.+Maecenas+at+neque+ut+enim+fermentum+vulputate.+Vivamus+non+auctor+enim.+Fusce+sollicitudin+ullamcorper+massa%2C+at+posuere+libero+commodo+sed.+Nullam+pharetra%2C+diam+et+ultrices+fermentum%2C+tortor+felis+tincidunt+risus%2C+id+condimentum+nibh+leo+eu+nisl.+Cras+leo+ante%2C+blandit+ac+bibendum+eu%2C+volutpat+id+nulla."
    d += "&tasksToRemove=" + JSON.stringify(tasksToRemove)
    d += "&peopleToRemove=" + JSON.stringify(peopleToRemove)
    d += "&filesToRemove=" + JSON.stringify(filesToRemove)
    $.ajax(url, {
        data: d,
        type: 'POST',
        beforeSend: function(xhr) {
            xhr.setRequestHeader('TASKS_TO_REMOVE', "[1,2,3,4]");
        },
        success: function(response) {
            var json = $.parseJSON(response);
            window.location = readProject_url; //json.id; // project read
        },
        error: function(xhr, textStatus, errorThrown) {
            //console.log(textStatus + "::" + errorThrown + "->" + xhr.responseText);
            try {
                // var json = $.parseJSON(xhr.responseText);
                // if ('fields' in json) {
                // for (var f in json.fields) {
                // $('input[name="' + json.fields[f] + '"]').parent().addClass("has-error");
                // }
                // }
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