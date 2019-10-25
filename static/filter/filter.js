$('document').ready(function() {
    // Click the generate button, will take all information in form and send it to the relevent API endpoint
    $('.generate').click(function() {
        // set up csrf token
        csrftoken = Cookies.get('csrftoken');
        
        var risk = $('#risk').val();
        var index = $('#index').val();
        var blacklist = $('#blacklist').val();
        $.post('/postfilter', `{"risk": "${risk}", "index": "${index}", "blacklist": "${blacklist}"}`, function(res) {
            console.log("Response: ",res)
        })
        console.log(risk,index,blacklist);
        // pseudo loading for client immersion, using settimeout
        setTimeout(function() {
            window.location = '/table';
        }, 3000);
    });
});