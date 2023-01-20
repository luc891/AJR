/*!
* Start Bootstrap - Clean Blog v6.0.8 (https://startbootstrap.com/theme/clean-blog)
* Copyright 2013-2022 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-clean-blog/blob/master/LICENSE)
*/
window.addEventListener('DOMContentLoaded', () => {
    let scrollPos = 0;
    const mainNav = document.getElementById('mainNav');
    const headerHeight = mainNav.clientHeight;
    window.addEventListener('scroll', function() {
        const currentTop = document.body.getBoundingClientRect().top * -1;
        if ( currentTop < scrollPos) {
            // Scrolling Up
            if (currentTop > 0 && mainNav.classList.contains('is-fixed')) {
                mainNav.classList.add('is-visible');
            } else {
                mainNav.classList.remove('is-visible', 'is-fixed');
            }
        } else {
            // Scrolling Down
            mainNav.classList.remove(['is-visible']);
            if (currentTop > headerHeight && !mainNav.classList.contains('is-fixed')) {
                mainNav.classList.add('is-fixed');
            }
        }
        scrollPos = currentTop;
    });
})

//CSRF Protection
function getCookie(c_name)
{
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
 }

function pass() {
    var pass1 = document.forms["chg_pass"].password1.value;
    var pass2 = document.forms["chg_pass"].password2.value;

    if (pass1 != pass2) {
        alert("Les mots de passe ne sont pas identiques");
        return false;
    }
    return true;
}

function remove_game() {
    fetch('/remove', {
        method : 'POST',
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),          
            "Content-Type": "application/json",      
          },
        body : JSON.stringify({
            title : document.querySelector('h1').innerHTML
        })
    })
    .then(response => {
        document.querySelector('#main').style.display = 'none';
        document.querySelector('#removed').style.display = 'block';
    })
}

function game_request() {
    const user = document.querySelector('#user').innerHTML;
    const game = document.querySelector('#title').innerHTML;
    fetch('/game_request', {
        method : 'POST',
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),          
            "Content-Type": "application/json",      
          },
          body : JSON.stringify({
            subject : 'Jeu demandé pour la prochaine session',
            body : {
                'user' : user,
                'game' : game
            }
          })
    })
    .then(response => {
        document.getElementsByName('game-btn')[0].style.display='none';
        document.querySelector('#message').innerHTML = 'Demande envoyée';
    })
}