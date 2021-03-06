<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>WinDynamicDesktop Themes</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.5.3/css/bootstrap.min.css">
    <link rel="stylesheet" href="main.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.slim.min.js"></script>
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
                        <a class="nav-link" href="index.html#free">Free</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="index.html#paid">Paid</a>
                    </li>
                </div>
                <div class="navbar-nav ml-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="https://github.com/t1m0thyj/WinDynamicDesktop/wiki/Creating-custom-themes"><i class="fa fa-plus"></i> Contribute</a>
                    </li>
                </div>
            </div>
        </nav>
        <a name="free" class="h2-anchor"></a><h2>Free</h2>
        <div class="accordion">
            <div class="card">
                <div class="card-header" id="heading-free-photos">
                    <h3 class="mb-0">
                        <button class="btn btn-link" type="button" data-toggle="collapse" data-target="#collapse-free-photos" aria-expanded="true" aria-controls="collapse-free-photos">
                            <i class="fa fa-minus"></i> Photos (${len(photos_theme_data)})
                        </button>
                    </h3>
                </div>
                <div id="collapse-free-photos" class="collapse show" aria-labelledby="heading-free-photos">
                    <div class="card-body row">
                    % for theme_id, theme_data in photos_theme_data.items():
                        <div class="col-md-4">
                            <div class="img-thumbnail">
                                % if theme_data["sunPhases"]:
                                <a href="#" onclick="openPreview('${theme_id}'); return false;">
                                % else:
                                <a href="${theme_data['themeUrl']}">
                                % endif
                                    <div class="alternating-image" style="background-image: url('thumbnails/${theme_id}_day.png');">
                                        <img src="thumbnails/${theme_id}_night.png" alt="${theme_data['displayName']}">
                                    </div>
                                    <div class="caption">
                                        % if theme_data["isNew"]:
                                        <small class="label-new">NEW </small>
                                        % endif
                                        ${theme_data["displayName"]}<small> (${theme_data["imageSize"]})</small>
                                    </div>
                                </a>
                                % if theme_data["sunPhases"]:
                                <a id="download_${theme_id}" class="caption-button" href="${theme_data['themeUrl']}" title="Download (${theme_data['fileSize']} MB)"><i class="fa fa-download"></i></a>
                                % else:
                                <a href="${theme_data['themeUrl']}" class="caption-button" target="_blank" title="Open in new tab"><i class="fa fa-external-link"></i></a>
                                % endif
                            </div>
                        </div>
                    % endfor
                    </div>
                </div>
            </div>
            <div class="card">
                <div class="card-header" id="heading-free-art">
                    <h3 class="mb-0">
                        <button class="btn btn-link" type="button" data-toggle="collapse" data-target="#collapse-free-art" aria-expanded="true" aria-controls="collapse-free-art">
                            <i class="fa fa-minus"></i> Art (${len(art_theme_data)})
                        </button>
                    </h3>
                </div>
                <div id="collapse-free-art" class="collapse show" aria-labelledby="heading-free-art">
                    <div class="card-body row">
                    % for theme_id, theme_data in art_theme_data.items():
                        <div class="col-md-4">
                            <div class="img-thumbnail">
                                % if theme_data["sunPhases"]:
                                <a href="#" onclick="openPreview('${theme_id}'); return false;">
                                % else:
                                <a href="${theme_data['themeUrl']}">
                                % endif
                                    <div class="alternating-image" style="background-image: url('thumbnails/${theme_id}_day.png');">
                                        <img src="thumbnails/${theme_id}_night.png" alt="${theme_data['displayName']}">
                                    </div>
                                    <div class="caption">
                                        % if theme_data["isNew"]:
                                        <small class="label-new">NEW </small>
                                        % endif
                                        ${theme_data["displayName"]}<small> (${theme_data["imageSize"]})</small>
                                    </div>
                                </a>
                                % if theme_data["sunPhases"]:
                                <a id="download_${theme_id}" class="caption-button" href="${theme_data['themeUrl']}" title="Download (${theme_data['fileSize']} MB)"><i class="fa fa-download"></i></a>
                                % else:
                                <a href="${theme_data['themeUrl']}" class="caption-button" target="_blank" title="Open in new tab"><i class="fa fa-external-link"></i></a>
                                % endif
                            </div>
                        </div>
                    % endfor
                    </div>
                </div>
            </div>
        </div>
        <a name="paid" class="h2-anchor"></a><h2>Paid</h2>
        <div class="alert alert-info" role="alert">
            <i class="fa fa-info-circle"></i> The paid wallpapers listed below can be purchased in bundles for a 50% discount from <a href="https://www.jetsoncreative.com/24hourwindows/#paid">24 Hour Wallpaper <i class="fa fa-external-link"></i></a>.
        </div>
        <div class="accordion">
            <div class="card">
                <div class="card-header" id="heading-paid-photos">
                    <h3 class="mb-0">
                        <button class="btn btn-link" type="button" data-toggle="collapse" data-target="#collapse-paid-photos" aria-expanded="true" aria-controls="collapse-paid-photos">
                            <i class="fa fa-minus"></i> Photos (${len(paid_theme_data)})
                        </button>
                    </h3>
                </div>
                <div id="collapse-paid-photos" class="collapse show" aria-labelledby="heading-paid-photos">
                    <div class="card-body row">
                    % for theme_id, theme_data in paid_theme_data.items():
                        <div class="col-md-4">
                            <div class="img-thumbnail">
                                <a href="${theme_data['themeUrl']}">
                                    <div class="alternating-image" style="background-image: url('thumbnails/${theme_id}_day.png');">
                                        <img src="thumbnails/${theme_id}_night.png" alt="${theme_data['displayName']}">
                                    </div>
                                    <div class="caption">
                                        % if theme_data["isNew"]:
                                        <small class="label-new">NEW </small>
                                        % endif
                                        ${theme_data["displayName"]}<small> (${theme_data["imageSize"]})</small>
                                    </div>
                                </a>
                                <a href="${theme_data['themeUrl']}" class="caption-button" target="_blank" title="Open in new tab"><i class="fa fa-external-link"></i></a>
                            </div>
                        </div>
                    % endfor
                    </div>
                </div>
            </div>
        </div>
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
    <script src="main.js"></script>
</body>
</html>
