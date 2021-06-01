<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>${displayName} | WinDynamicDesktop Themes</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.5.3/css/bootstrap.min.css">
    <link rel="stylesheet" href="${basePath}preview.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.slim.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.5.3/js/bootstrap.min.js"></script>
</head>
<body>
    <div id="topLeftPanel">
        <span id="themeNameText">${displayName}<small> (${imageSize})</small></span><br>
        Previewing <span id="previewText"></span>
    </div>
    <div id="topRightPanel">
        <button id="playPauseButton" type="button" class="btn btn-default btn-xs">
            <span id="playPauseIcon"><i class="fa fa-pause" aria-hidden="true"></i></span>
        </button>
    </div>
    <div id="bottomRightPanel">
        ${imageCredits}
    </div>
    <div id="myCarousel" class="carousel slide carousel-fade" data-ride="carousel">
        <ul class="carousel-indicators">
            <li data-target="#myCarousel" data-slide-to="0" class="active"></li>
        % for i in range(1, len(sunPhases)):
            <li data-target="#myCarousel" data-slide-to="${i}"></li>
        % endfor
        </ul>

        <div class="carousel-inner">
        % for i in range(len(sunPhases)):
            % if i == 0:
            <div class="carousel-item active">
            % else:
            <div class="carousel-item">
            % endif
                <img src="${basePath}previews/${themeId}_${sunPhases[i]}.jpg" alt="${sunPhases[i].capitalize()}">
            </div>
        % endfor
        </div>

        <a class="carousel-control-prev" href="#myCarousel" data-slide="prev" style="width: 80px;">
            <span class="carousel-control-prev-icon"></span>
        </a>
        <a class="carousel-control-next" href="#myCarousel" data-slide="next" style="width: 80px;">
            <span class="carousel-control-next-icon"></span>
        </a>
    </div>
    <script src="${basePath}preview.js"></script>
</body>
</html>
