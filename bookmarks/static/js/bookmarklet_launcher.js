(function(){
    if (window.myBookmarklet !== undefined){
        myBookmarklet();
    }
    else {
        document.body.appendChild(document.createElement('script')).src='http://d715cb9a33e1.ngrok.io/static/js/bookmarklet.js?r='+Math.floor(Math.random()*99999999999999999999);
    }
})();


// https://3f6ad53c.ngrok.io/static/js/bookmarklet.js
// http://c475567f675c.ngrok.io/static/js/bookmarklet_launcher.js