function editProfile(url, readProfile_url) {
    console.log("profile edit");
    var d = $('#profile-form').serialize(); // get the form data
    $.ajax(url, {
        data: d,
        type: 'POST',
        success: function(response) {
            var json = $.parseJSON(response);
            window.location = readProfile_url;
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

function editSettings(url, readProfile_url) {
    console.log("settings edit");
    var d = $('#settings-form').serialize(); // get the form data
    $.ajax(url, {
        data: d,
        type: 'POST',
        success: function(response) {
            var json = $.parseJSON(response);
            window.location = readProfile_url;
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