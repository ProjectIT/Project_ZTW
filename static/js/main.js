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
        translate(languages["en"]);
    });
    $("#lang-pl").click(function() {
        $(this).addClass("lang-icon-active");
        $("#lang-en").removeClass("lang-icon-active");
        translate(languages["pl"]);
    });
});

function translate(lang_obj) {
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
        }else if ($el.is('input')) {
            $el.attr('placeholder', val);
        } else {
            $el.text(val);
        }
    });
}

/*
 * utils
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