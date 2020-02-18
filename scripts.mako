<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>WinDynamicDesktop Scripts</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.4.1/css/bootstrap.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.4.1/jquery.slim.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.1/umd/popper.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.4.1/js/bootstrap.min.js"></script>
</head>
<body>
    <div class="container" style="max-width:1000px;">
        <nav class="navbar navbar-expand-sm bg-dark navbar-dark sticky-top">
            <a class="navbar-brand" href="index.html">WDD Scripts</a>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#collapsibleNavbar" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="collapsibleNavbar">
                <div class="navbar-nav">
                    <li class="nav-item">
                        <a class="nav-link" href="index.html#stable">Stable</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="index.html#experimental">Experimental</a>
                    </li>
                </div>
                <div class="navbar-nav ml-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="https://github.com/t1m0thyj/WDD-scripts#creating-new-scripts"><i class="fa fa-plus"></i> Contribute</a>
                    </li>
                </div>
            </div>
        </nav>
        <div class="alert alert-info" role="alert">
            <i class="fa fa-info-circle"></i> Scripts are a new feature in WinDynamicDesktop 4.0. Click <a href="https://github.com/t1m0thyj/WinDynamicDesktop/wiki/Installing-scripts">here</a> for instructions on how to install them.
        </div>
        <a name="free" style="margin-top:-38px; padding-top:38px;"></a><h2 style="padding-top:20px;">Stable</h2>
        <div class="row" style="padding:0 12px;">
            <table class="table table-striped">
            <tbody>
            % for script_data in scripts_stable:
                <%
                    script_id = script_data["filename"][:-4]
                    script_name = script_data["name"]
                    author = script_data["author"]
                    requires = script_data["requires"]
                    description = script_data["description"]
                    url = "https://github.com/t1m0thyj/WDD-scripts/raw/master/stable/" + script_data["filename"]
                    warning = script_data.get("warning")
                    info = script_data.get("info")
                %>
                <tr><td style="width: 50%">
                <a name="${script_id}"><h4>${script_name}</h4></a>
                ${description}
                </td><td style="width: 50%">
                % if "win10" in requires:
                <a href="#" data-toggle="popover" data-placement="top" title="Requires Windows 10" data-content="This script will not work on older versions of Windows."><span class="badge badge-secondary" style="font-size: small;">Windows 10</span></a>
                % endif
                % if "desktop" in requires:
                <a href="#" data-toggle="popover" data-placement="top" title="Requires desktop app" data-content="This script will not work in the Microsoft Store app."><span class="badge badge-secondary" style="font-size: small;">Desktop Only</span></a>
                % endif
                <a href="https://github.com/${author}" target="_blank"><span class="badge badge-secondary" style="font-size: small;">@${author}</span></a>
                <a href="${url}" style="float: right;">Download</a>
                % if info:
                <div class="alert alert-info" role="alert" style="bottom: -15px;">
                    <i class="fa fa-info-circle"></i> ${info}
                </div>
                % endif
                </td></tr>
            % endfor
            </tbody>
            </table>
        </div>
        <a name="paid" style="margin-top:-38px; padding-top:38px;"></a><h2 style="padding-top:20px;">Experimental</h2>
        <div class="row" style="padding:0 12px;">
            <table class="table table-striped">
            <tbody>
            % for script_data in scripts_experimental:
                <%
                    script_id = script_data["filename"][:-4]
                    script_name = script_data["name"]
                    author = script_data["author"]
                    requires = script_data["requires"]
                    description = script_data["description"]
                    url = "https://github.com/t1m0thyj/WDD-scripts/raw/master/experimental/" + script_data["filename"]
                    warning = script_data.get("warning")
                    info = script_data.get("info")
                %>
                <tr><td style="width: 50%">
                <a name="${script_id}"><h4>${script_name}</h4></a>
                ${description}
                </td><td style="width: 50%">
                % if "win10" in requires:
                <a href="#" data-toggle="popover" data-placement="top" title="Requires Windows 10" data-content="This script will not work on older versions of Windows."><span class="badge badge-secondary" style="font-size: small;">Windows 10</span></a>
                % endif
                % if "desktop" in requires:
                <a href="#" data-toggle="popover" data-placement="top" title="Requires desktop app" data-content="This script will not work in the Microsoft Store app."><span class="badge badge-secondary" style="font-size: small;">Desktop Only</span></a>
                % endif
                <a href="https://github.com/${author}" target="_blank"><span class="badge badge-secondary" style="font-size: small;">@${author}</span></a>
                <a href="${url}" style="float: right;">Download</a>
                % if warning:
                <div class="alert alert-warning" role="alert" style="bottom: -15px;">
                    <i class="fa fa-warning"></i> ${warning}
                </div>
                % endif
                % if info:
                <div class="alert alert-info" role="alert" style="bottom: -15px;">
                    <i class="fa fa-info-circle"></i> ${info}
                </div>
                % endif
                </td></tr>
            % endfor
            </tbody>
            </table>
        </div>
    </div>
    <script>
    $(document).ready(() => {
        $('[data-toggle="popover"]').popover();
    });
    </script>
</body>
</html>
