<!DOCTYPE html>
<html lang="en">
<%
    theme_name, theme_type, theme_config, theme_resolution, image_paths = theme_data
    display_name = theme_config.get("displayName")
    if not display_name:
        display_name = theme_name.replace("_", " ")
%>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>${theme_name} - WinDynamicDesktop Themes</title>
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
        <a href="https://bitbucket.org/t1m0thyj/wdd-themes/downloads/${theme_name}.ddw">
            <button type="button" class="btn btn-success" style="float:right; margin-right:20px; margin-top:4px;"><i class="fa fa-download"></i> Download (${theme_config["fileSize"]} MB)</button>
        </a>
        <h2 style="margin-left:20px;">${display_name}<small> (${theme_resolution})</small></h2>
        <div class="container mb-auto">
            <div id="demo" class="carousel slide carousel-fade" data-ride="carousel">
                <ul class="carousel-indicators">
                    <li data-target="#demo" data-slide-to="0" class="active"></li>
                % for i in range(1, len(image_paths)):
                    <li data-target="#demo" data-slide-to="${i}"></li>
                % endfor
                </ul>

                <div class="carousel-inner">
                % for i in range(len(image_paths)):
                    % if i == 0:
                    <div class="carousel-item active">
                    % else:
                    <div class="carousel-item">
                    % endif
                        <img src="${image_paths[i]}" alt="Wallpaper ${i + 1}">
                    </div>
                % endfor
                </div>

                <a class="carousel-control-prev" href="#demo" data-slide="prev">
                    <span class="carousel-control-prev-icon"></span>
                </a>
                <a class="carousel-control-next" href="#demo" data-slide="next">
                    <span class="carousel-control-next-icon"></span>
                </a>
            </div>
        </div>
        <p class="text-secondary" style="margin-left:20px;">Credits: ${theme_config["imageCredits"]}</p>
    </div>
</body>
</html>