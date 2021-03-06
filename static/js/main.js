/*
 * i18n
 */
// i18n.configure({
// defaultLocale: 'en',
// locales: ['en', 'de', 'es', 'fr', 'ja', 'nl', 'pt-br', 'pt', 'ro', 'sv', 'tr', 'it'],
// directory: './language'
// });
// i18n.setLocale(pureLanguage);

languages = {};

$(document).ready(function() {
    // <img src="{{ STATIC_URL }}imgs/lang/gb.png" id="lang-en" class="navigation-bar-icon lang-icon">
    // <img src="{{ STATIC_URL }}imgs/lang/pl.png" id="lang-pl" class="navigation-bar-icon lang-icon">

    $("#lang-en").click(function() {
        $(this).addClass("lang-icon-active");
        $("#lang-pl").removeClass("lang-icon-active");
        translate("en");
    });
    $("#lang-pl").click(function() {
        $(this).addClass("lang-icon-active");
        $("#lang-en").removeClass("lang-icon-active");
        translate("pl");
    });

    if (Get_Cookie('i18n')) {
        // alert(Get_Cookie('i18n'));
        var lang_id = Get_Cookie('i18n');
        translate(lang_id);
        $("#lang-" + lang_id).addClass("lang-icon-active");
    }
});

function translate(lang_id) {
    lang_obj = languages[lang_id];
    $('[data-translate]').each(function() {
        var $el = $(this);
        var key = $el.data('translate');
        var val = "###";
        if (key in lang_obj)
            val = lang_obj[key];

        if ($el.is('input[type="submit"]')) {
            // console.log($el);
            // console.log(val+":"+key);
            $el.attr('value', val);
            // $el.attr('value', "a");
        } else if ($el.is('input')) {
            $el.attr('placeholder', val);
        } else {
            $el.text(val);
        }
    });
    Set_Cookie('i18n', lang_id, '', '/', '', '');
}

/*
 * utils
 * http://techpatterns.com/downloads/javascript_cookies.php
 */
function Get_Cookie(check_name) {
    // first we'll split this cookie up into name/value pairs
    // note: document.cookie only returns name=value, not the other components
    var a_all_cookies = document.cookie.split(';');
    var a_temp_cookie = '';
    var cookie_name = '';
    var cookie_value = '';
    var b_cookie_found = false; // set boolean t/f default f

    for (i = 0; i < a_all_cookies.length; i++) {
        // now we'll split apart each name=value pair
        a_temp_cookie = a_all_cookies[i].split('=');


        // and trim left/right whitespace while we're at it
        cookie_name = a_temp_cookie[0].replace(/^\s+|\s+$/g, '');

        // if the extracted name matches passed check_name
        if (cookie_name == check_name) {
            b_cookie_found = true;
            // we need to handle case where cookie has no value but exists (no = sign, that is):
            if (a_temp_cookie.length > 1) {
                cookie_value = unescape(a_temp_cookie[1].replace(/^\s+|\s+$/g, ''));
            }
            // note that in cases where cookie is initialized but no value, null is returned
            return cookie_value;
            break;
        }
        a_temp_cookie = null;
        cookie_name = '';
    }
    if (!b_cookie_found) {
        return null;
    }
}

function Set_Cookie(name, value, expires, path, domain, secure) {
    // set time, it's in milliseconds
    var today = new Date();
    today.setTime(today.getTime());

    /*
if the expires variable is set, make the correct
expires time, the current script below will set
it for x number of days, to make it for hours,
delete * 24, for minutes, delete * 60 * 24
*/
    if (expires) {
        expires = expires * 1000 * 60 * 60 * 24;
    }
    var expires_date = new Date(today.getTime() + (expires));

    document.cookie = name + "=" + escape(value) +
        ((expires) ? ";expires=" + expires_date.toGMTString() : "") +
        ((path) ? ";path=" + path : "") +
        ((domain) ? ";domain=" + domain : "") +
        ((secure) ? ";secure" : "");
}