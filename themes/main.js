function openPreview(themeId) {
    $('#previewFrame').attr('src', 'preview_' + themeId + '.html');
    $('#downloadButton').html('<i class="fa fa-download"></i> ' + $('#download_' + themeId).attr('title'));
    $('#downloadButton').attr('href', $('#download_' + themeId).attr('href'));
    $('#previewModal').modal();
}
