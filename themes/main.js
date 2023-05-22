var basePath = document.currentScript.getAttribute('src').slice(0, -14);
var isLoading = false;
var themesPerPage = 30;

var thumbnailTemplate = `<div class="img-thumbnail">
    {{#sunPhases.length}}
    <a href="#" onclick="openPreview('{{themeId}}'); return false;">
    {{/sunPhases.length}}
    {{^sunPhases.length}}
    <a href="{{themeUrl}}" onclick="clickCounter('{{themeId}}');">
    {{/sunPhases.length}}
        <div class="alternating-image" style="background-image: url('${basePath}images/thumbnails/{{themeId}}_day.png');">
            <img src="${basePath}images/thumbnails/{{themeId}}_night.png" alt="{{displayName}}">
        </div>
        <div class="caption">
            {{#isNew}}
            <small class="label-new">NEW </small>
            {{/isNew}}
            {{displayName}}<small> ({{imageSize}})</small>
        </div>
    </a>
    {{#sunPhases.length}}
    <a id="download_{{themeId}}" class="caption-button" href="{{themeUrl}}" onclick="clickCounter('{{themeId}}');" title="Download ({{fileSize}} MB)"><i class="fa fa-download"></i></a>
    {{/sunPhases.length}}
    {{^sunPhases.length}}
    <a href="{{themeUrl}}" class="caption-button" onclick="clickCounter('{{themeId}}');" target="_blank" title="Open in new tab"><i class="fa fa-external-link"></i></a>
    {{/sunPhases.length}}
</div>`;

function clickCounter(themeId) {
    if (window.location.protocol === 'file:') return;
    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'https://script.google.com/macros/s/AKfycbzUm3ztw4b0rDQrXdLtZoONcqc8n8NYqOf2eK85G9pWgyyugnz3vf1wSjm72kDQptFU/exec');
    xhr.send(themeId);
}

function loadThumbnail(themeId) {
    var themeData = themesDb[themeId];
    themeData.isNew = moment().diff(themeData.dateAdded, 'months', true) < 1;
    themeData.themeId = themeId;
    $('#theme_' + themeId).html(Mustache.render(thumbnailTemplate, themeData));
}

function loadThumbnailGrid(themeType, pageNumber) {
    if (isLoading) return;
    isLoading = true;
    var themeIds = Object.keys(themesDb).filter(themeId => themesDb[themeId].themeType === themeType);
    var filterString = $('#optionFilter').val().toLowerCase();
    if (filterString.length > 0) {
        themeIds = themeIds.filter(themeId => themesDb[themeId].displayName.toLowerCase().includes(filterString));
    }
    var sortIndex = $('#optionSort').prop('selectedIndex');
    if (sortIndex === 1) {
        themeIds = themeIds.concat().sort((a, b) => moment(themesDb[b].dateAdded).diff(themesDb[a].dateAdded));
    } else if (sortIndex === 2) {
        themeIds = themeIds.concat().sort((a, b) => themesDb[b].clickCount - themesDb[a].clickCount);
    }
    var themeCount = themeIds.length;
    renderPageButtons(pageNumber, Math.ceil(themeCount / themesPerPage), themeType);
    if (themeCount > 0) {
        var themeMin = themesPerPage * ((pageNumber || 1) - 1) + 1;
        var themeMax = Math.min(themeMin + themesPerPage - 1, themeCount);
        themeIds = themeIds.slice(themeMin - 1, themeMax);
        $('#pageDescription').html('Showing ' + themeMin.toString() + '-' + themeMax.toString() + ' of ' + themeCount.toString() + ' themes');
    } else {
        $('#pageDescription').html('No themes found');
    }
    $('#thumbnailGrid').empty();
    themeIds.forEach((themeId) => {
        $('#thumbnailGrid').append('<div id="theme_' + themeId + '" class="col-md-4"></div>');
        loadThumbnail(themeId);
    });
    isLoading = false;
}

function openPreview(themeId) {
    $('#previewFrame').attr('src', 'preview/' + themeId + '.html');
    $('#downloadButton').html('<i class="fa fa-download"></i> ' + $('#download_' + themeId).attr('title'));
    $('#downloadButton').attr('href', $('#download_' + themeId).attr('href'));
    $('#downloadButton').click(function() { clickCounter(themeId); });
    $('#previewModal').modal();
}

function pageChanger(themeType, pageNumber) {
    return function() {
        loadThumbnailGrid(themeType, pageNumber);
        document.body.scrollTop = 0; // For Safari
        document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
        return false;
    };
}

function renderPageButtons(pageNumber, pageCount, themeType) {
    if (pageNumber == null) {
        if (pageCount > 1) {
            $('#pageButtons').html('<li id="page-prev" class="page-item"><a class="page-link" href="#">Previous</a></li>');
            for (var i = 1; i <= pageCount; i++) {
                $('#pageButtons').append('<li id="page-' + i.toString() + '" class="page-item"><a class="page-link" href="#">' + i.toString() + '</a></li>');
                $('#page-' + i.toString() + ' a').click(pageChanger(themeType, i));
            }
            $('#pageButtons').append('<li id="page-next" class="page-item"><a class="page-link" href="#">Next</a></li>');
            $('#pageButtons').show();
        } else {
            $('#pageButtons').hide();
        }
    }
    pageNumber = pageNumber || 1;
    if (pageCount > 1) {
        $('#pageButtons li').removeClass('active disabled');
        $('#page-' + pageNumber.toString()).addClass('active');
        if (pageNumber === 1) {
            $('#page-prev').addClass('disabled');
        } else {
            $('#page-prev a').click(pageChanger(themeType, pageNumber - 1));
        }
        if (pageNumber === pageCount) {
            $('#page-next').addClass('disabled');
        } else {
            $('#page-next a').click(pageChanger(themeType, pageNumber + 1));
        }
    }
}
