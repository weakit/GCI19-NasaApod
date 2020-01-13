function open_pdf(){
    pdf_url = window.location.origin + '/pdf' + window.location.pathname;
    window.open(pdf_url);
}

var today = new Date(new Date().getFullYear(), new Date().getMonth(), new Date().getDate());

$(document).ready(function() {
    if ($('.datepicker').length > 0) {
        $( ".datepicker" ).datepicker({
            uiLibrary: 'bootstrap4', 
            format: 'yyyy/mm/dd',
            minDate: '1995-06-20',
            maxDate: today
        });
    }
})


function get_image(){
    var date = $('.datepicker').val();
    if (date == '' || date.match(/^[A-Za-z]+$/))
        return alert("That date doesn't seem right.")
    date_url = window.location.origin + '/' + date;
    window.open(date_url);
}

