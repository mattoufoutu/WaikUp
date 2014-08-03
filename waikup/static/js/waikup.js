/*
    WaikUp Global JavaScript
 */

$('.collapser').click(function() {
    var itemSelector = 'div#'+$(this).attr('id');
    if ($(itemSelector).hasClass('out')) {
        $(itemSelector).addClass('in');
        $(itemSelector).removeClass('out');
    } else {
        $(itemSelector).addClass('out');
        $(itemSelector).removeClass('in');
    }
});
$('.expand-all').click(function() {
    $('.collapse.out').removeClass('out').addClass('in');
});
$('.collapse-all').click(function() {
    $('.collapse.in').removeClass('in').addClass('out');
});
$('#new-link-save').click(function() {
    $('#new-link-form').submit();
    return true;
});
$('#new-link-cancel').click(function() {
    $('#new-link-url').val('');
    $('#new-link-title').val('');
    $('#new-link-description').val('');
    return true;
});
$('#chpasswd-save').click(function() {
    $('#chpasswd-form').submit();
    return true;
});
$('#chpasswd-cancel').click(function() {
    $('#chpasswd-old').val('');
    $('#chpasswd-new').val('');
    $('#chpasswd-confirm').val('');
    return true;
});
