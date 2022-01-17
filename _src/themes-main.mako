<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>WinDynamicDesktop Themes</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.5.3/css/bootstrap.min.css">
    <link rel="stylesheet" href="themes/main.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.slim.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.29.1/moment.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/mustache.js/3.1.0/mustache.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.5.3/js/bootstrap.min.js"></script>
</head>
<body>
    <div class="container">
        <nav class="navbar navbar-expand-sm bg-dark navbar-dark sticky-top">
            <a class="navbar-brand" href="index.html">WDD Themes</a>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#collapsibleNavbar" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="collapsibleNavbar">
                <div class="navbar-nav">
                    <li class="nav-item">
                        % if pageType == "free":
                        <a class="nav-link active" href="free.html">Free</a>
                        % else:
                        <a class="nav-link" href="free.html">Free</a>
                        % endif
                    </li>
                    <li class="nav-item">
                        % if pageType == "paid":
                        <a class="nav-link active" href="paid.html">Paid</a>
                        % else:
                        <a class="nav-link" href="paid.html">Paid</a>
                        % endif
                    </li>
                    <li class="nav-item">
                        % if pageType == "macos":
                        <a class="nav-link active" href="macos.html">macOS</a>
                        % else:
                        <a class="nav-link" href="macos.html">macOS</a>
                        % endif
                    </li>
                </div>
                <div class="navbar-nav ml-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="https://github.com/t1m0thyj/WinDynamicDesktop/wiki/Creating-custom-themes"><i class="fa fa-plus"></i> Contribute</a>
                    </li>
                </div>
            </div>
        </nav>
        % if pageType == "home":
        <div class="text-center">
            <h2>Featured Themes</h2>
        </div>
        <h3>Free</h3>
        <div class="row">
            % for theme_id in featuredFree:
            <div id="theme_${theme_id}" class="col-md-4"></div>
            % endfor
        </div>
        <div class="text-center">
            <a class="btn btn-primary mb-2 mt-2" href="free.html">Browse all ${numFree} free themes</a>
        </div>
        <h3>Paid</h3>
        <div class="row">
            % for theme_id in featuredPaid:
            <div id="theme_${theme_id}" class="col-md-4"></div>
            % endfor
        </div>
        <div class="text-center">
            <a class="btn btn-primary mb-4 mt-2" href="paid.html">Browse all ${numPaid} paid themes</a>
        </div>
        % else:
        % if pageType == "paid":
        <div class="alert alert-info" role="alert">
            <i class="fa fa-info-circle"></i> The paid wallpapers listed below can be purchased in bundles for a 50% discount from <a href="https://www.jetsoncreative.com/24hourwindows/#paid">24 Hour Wallpaper <i class="fa fa-external-link"></i></a>.
        </div>
        % elif pageType == "macos":
        <div class="alert alert-info" role="alert">
            <i class="fa fa-info-circle"></i> The wallpapers listed below are bundled with macOS and available for download in WinDynamicDesktop.
        </div>
        % endif
        <div class="form-inline">
            <input id="optionFilter" class="form-control mr-sm-3" type="search" placeholder="Search..." oninput="loadThumbnailGrid('${pageType}');">
            <label class="mr-sm-2" for="optionSort">Sort by:</label>
            <div class="form-group ml-2 ml-sm-0 mt-2 mt-sm-0">
                <select id="optionSort" class="form-control mr-sm-2" onchange="loadThumbnailGrid('${pageType}');">
                    <option>Name</option>
                    <option>Date Added</option>
                    <option>Most Popular</option>
                </select>
            </div>
            <span id="pageDescription" class="ml-auto"></span>
        </div>
        <div id="thumbnailGrid" class="row"></div>
        <ul id="pageButtons" class="pagination justify-content-center"></ul>
        % endif
    </div>
    <div id="previewModal" class="modal fade" tabindex="-1">
        <div class="modal-dialog modal-dialog-centered" role="document">
            <div class="modal-content">
                <div class="modal-body">
                    <div class="embed-responsive embed-responsive-16by9">
                        <iframe id="previewFrame" class="embed-responsive-item" width="960" height="540" frameborder="0"></iframe>
                    </div>
                </div>
                <div class="modal-footer">
                    <a id="downloadButton" class="btn btn-primary ml-auto">Download</a>
                    <button type="button" class="btn btn-secondary mr-auto" data-dismiss="modal">Close</button>
                </div>
            </div>
        </div>
    </div>
    <script src="themes/themes.db.js"></script>
    <script src="themes/main.js"></script>
    <script type="text/javascript">
    $(function() {
        % if pageType == "home":
        ${list(featuredFree + featuredPaid)}.map(loadThumbnail);
        % else:
        loadThumbnailGrid('${pageType}');
        % endif
    });
    </script>
</body>
</html>
