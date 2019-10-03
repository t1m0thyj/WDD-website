<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>WinDynamicDesktop Themes</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.3.1/css/bootstrap.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.4.1/jquery.slim.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.3.1/js/bootstrap.min.js"></script>
</head>
<body>
    <div class="container" style="max-width:1000px;">
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
                    <li class="nav-item">
                        <a class="nav-link" href="index.html#bundles">Bundles</a>
                    </li>
                </div>
                <div class="navbar-nav ml-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="https://github.com/t1m0thyj/WinDynamicDesktop/wiki/Creating-custom-themes"><i class="fa fa-plus"></i> Contribute</a>
                    </li>
                </div>
            </div>
        </nav>
        <a name="free"></a><h2 style="padding-top:20px;">Free</h2>
        <div class="row" style="padding:0 12px;">
        % for theme_name, theme_type, theme_config, theme_resolution, theme_url in themes_free:
            <div class="col-md-4" style="padding:8px;">
                <div class="img-thumbnail">
                    % if theme_type == "contrib":
                    <a href="${theme_name}.html">
                    % else:
                    <a href="${theme_url}">
                    % endif
                        <img src="thumbnails/${theme_name}_thumbnail.png" alt="${theme_name}" style="width:100%">
                        <div class="caption">
                            <%
                                display_name = theme_config.get("displayName")
                                if not display_name:
                                    display_name = theme_name.replace("_", " ")
                            %>
                            ${display_name}<small> (${theme_resolution})</small>
                        </div>
                    </a>
                    % if theme_type == "contrib":
                    <a href="https://bitbucket.org/t1m0thyj/wdd-themes/downloads/${theme_name}.ddw" style="float:right; margin-top:-22px;"><i class="fa fa-download"></i></a>
                    % else:
                    <a href="${theme_url}" target="_blank" style="float:right; margin-top:-22px;"><i class="fa fa-external-link"></i></a>
                    % endif
                </div>
            </div>
        % endfor
        </div>
        <a name="paid"></a><h2 style="padding-top:20px;">Paid</h2>
        <div class="row" style="padding:0 12px;">
        % for theme_name, _, theme_config, theme_resolution, theme_url in themes_paid:
            <div class="col-md-4" style="padding:8px;">
                <div class="img-thumbnail">
                    <a href="${theme_url}">
                        <img src="${f'thumbnails/{theme_name}_thumbnail.png'}" alt="${theme_name}" style="width:100%">
                        <div class="caption">
                            <%
                                display_name = theme_config.get("displayName")
                                if not display_name:
                                    display_name = theme_name.replace("_", " ")
                            %>
                            ${display_name}<small> (${theme_resolution})</small>
                        </div>
                    </a>
                    <a href="${theme_url}" target="_blank" style="float:right; margin-top:-22px;"><i class="fa fa-external-link"></i></a>
                </div>
            </div>
        % endfor
        </div>
        <a name="bundles"></a><h2 style="padding-top:20px;">Bundles</h2>
        <div class="row" style="padding:0 12px;">
        <span style="padding:0 8px; padding-bottom:50px;">The paid wallpapers listed above can be purchased in bundles for a 50% discount from <a href="https://www.jetsoncreative.com/24hourwindows/#paid">24 Hour Wallpaper <i class="fa fa-external-link"></i></a>.</span>
        </div>
    </div>
</body>
</html>