var isPaused = false;
var previewText;

$('#playPauseButton').click(function () {
    isPaused = !isPaused;
    if (isPaused) {
        $('#myCarousel').carousel('pause');
        $('#playPauseIcon').html('<i class="fa fa-play" aria-hidden="true"></i>');
    } else {
        $('#myCarousel').carousel('cycle')
        $('#playPauseIcon').html('<i class="fa fa-pause" aria-hidden="true"></i>');
    }
});

$('#myCarousel').on('slide.bs.carousel', function (e) {
    previewText = $('#myCarousel div:nth-child(' + (e.to + 1).toString() + ')').children('img').attr('alt');
    $('#previewText').html(previewText);
});

previewText = $('#myCarousel div.active').children('img').attr('alt');
$('#previewText').html(previewText);
