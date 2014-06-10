// TODO add better error markers ?
// TODO add confirmation dialogs

var searchQueryId = 0;

$(document).ready(function() {
    checkIfTaskTableShouldBeHidden();

    var searchDelay = 500;

    var searchTimer = null;
    $(".search-person-ctr").keyup(function() {
        $("#assignment-list").hide();
        $("#search-loading").show();
        clearTimeout(searchTimer);
        searchTimer = setTimeout(function() {
            searchPerson();
        }, searchDelay);
    });
});

var submitName;

function setSubmit(button) {
    submitName = button.value;
}

/*
 * person assignment search
 */
function searchPerson() {
    var d = $('#assignment-form').serialize(); // get the form data
    ++searchQueryId;
    d += "&search-token=" + searchQueryId;
    console.log(d);

    // var url = "project/user/search/2";
    var url = "user/search";
    $.ajax(url, {
        data: d,
        type: 'POST',
        success: function(response) {
            $("#search-loading").hide();
            var json = $.parseJSON(response);
            // $("#search-person-result").html(response);
            if (json["search-token"] != searchQueryId) {
                console.log("Got old search results");
                return;
            }

            if (json.status && json.data.length > 0) {
                $('#assignment-list').empty();
                // create person views
                var tmplMarkup = $('#search-result-template').html();
                for (i = 0; i < json.data.length; ++i) {
                    var p = json.data[i];
                    var compiledTmpl = _.template(tmplMarkup, p);
                    $('#assignment-list').append(compiledTmpl);
                }

                $('#assignment-list').show();

                for (i = 0; i < json.data.length; ++i) {
                    var p = json.data[i];
                    $("[data-person-id='" + p.id + "']").click(assignmentListItemClick);
                }


            } else if (json.status && json.data.length === 0) {
                var s = "Could not find user that matches the criteria";
                $("#search-person-result").html(s);
                // $("#search-person-result").html($("#search-person-result").html() + s);
            } else {
                var s = "Found " + json["found-count"] + " users that match the criteria, please limit the search";
                $("#search-person-result").html(s);
                // $("#search-person-result").html($("#search-person-result").html() + s);
            }
        },
        error: function(xhr, textStatus, errorThrown) {
            $("#search-loading").hide();
            //console.log(textStatus + "::" + errorThrown + "->" + xhr.responseText);
            var json = $.parseJSON(xhr.responseText);
            $("#search-person-result").html("Some error happened: '" + xhr.responseText + "'");
        }
    });
}

function deleteProject( successUrl) {
     var d = $('#project-form').serialize(); // get the form data
    $.ajax("", {
        data: d,
        type: 'DELETE',
        beforeSend: function(xhr) {
            // xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
            xhr.setRequestHeader("X-CSRFToken", Get_Cookie("csrftoken"));
        },
        success: function(response) {
            // console.log(response);
            var json = $.parseJSON(response);
            if(json.success){
                // window.location = "/task/" + json.id;
                window.location = successUrl;
            }else{
                alert("Unspecified error");
            }
        },
        error: function(xhr, textStatus, errorThrown) {
            alert("Error " + xhr.status + " " + errorThrown);
        }
    });
}


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

function assignmentListItemClick() {
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
};

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
