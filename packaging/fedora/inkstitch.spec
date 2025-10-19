Name:           inkstitch
Version:        3.2.2
Release:        %{autorelease}
Summary:        Machine embroidery inkscape extension

License:        GPL-3.0-or-later
URL:            https://inkstitch.org
Source:         https://github.com/inkstitch/inkstitch/archive/%{version}/inkstitch-%{version}.tar.gz


BuildRequires:  geos-devel
BuildRequires:  gettext
BuildRequires:  inkscape
BuildRequires:  make
BuildRequires:  python3-devel
BuildRequires:  python3dist(colormath2)
BuildRequires:  python3dist(diskcache)
BuildRequires:  python3dist(flask)
BuildRequires:  python3dist(flask-cors)
BuildRequires:  python3dist(fonttools)
BuildRequires:  python3dist(inkex)
BuildRequires:  python3dist(jinja2)
BuildRequires:  python3dist(lxml)
BuildRequires:  python3dist(networkx)
BuildRequires:  python3dist(numpy)
BuildRequires:  python3dist(platformdirs)
BuildRequires:  python3dist(pystitch)
BuildRequires:  python3dist(requests)
BuildRequires:  python3dist(shapely)
BuildRequires:  python3dist(trimesh)
BuildRequires:  python3dist(wxpython)
BuildRequires:  python3dist(pytest)
Requires:  inkscape
Requires:  python3dist(colormath2)
Requires:  python3dist(diskcache)
Requires:  python3dist(flask)
Requires:  python3dist(flask-cors)
Requires:  python3dist(fonttools)
Requires:  python3dist(inkex)
Requires:  python3dist(jinja2)
Requires:  python3dist(lxml)
Requires:  python3dist(networkx)
Requires:  python3dist(numpy)
Requires:  python3dist(platformdirs)
Requires:  python3dist(pystitch)
Requires:  python3dist(requests)
Requires:  python3dist(shapely)
Requires:  python3dist(trimesh)
Requires:  python3dist(wxpython)

BuildArch:      noarch

%description
Ink/Stitch aims to be a full-fledged embroidery digitizing platform based
entirely on free, open source software. Our goal is to be approachable for
hobbyists while also providing the power needed by professional digitizers.
We also aim to provide a welcoming open source environment where contributing
is fun and easy.

%prep
%autosetup -n inkstitch-%{version}
sed -i 's/python bin/python3 bin/g' Makefile
# remove GitHub specific build files
rm -r .github

%build
make manual
cp LOGGING_template.toml LOGGING.toml
# Disable logging
sed -i 's/warnings_capture = true/warnings_capture = false/g' LOGGING.toml
sed -i 's/level = "DEBUG"/level = "CRITICAL"/g' LOGGING.toml
cp DEBUG_template.toml DEBUG.toml
sed -i 's/# disable_logging = true/disable_logging = true/g' DEBUG.toml
sed -i 's/# log_config_file = "LOGGING.toml"/log_config_file = "LOGGING.toml"/g' DEBUG.toml

%install

mkdir -p %{buildroot}%{_datadir}/inkscape/extensions/inkstitch
cp -a -p -r . \
   %{buildroot}%{_datadir}/inkscape/extensions/inkstitch/
%py3_shebang_fix \
   %{buildroot}%{_datadir}/inkscape/extensions/inkstitch/bin/generate-inx-files
%py3_shebang_fix \
   %{buildroot}%{_datadir}/inkscape/extensions/inkstitch/bin/generate-version-file
%py3_shebang_fix \
   %{buildroot}%{_datadir}/inkscape/extensions/inkstitch/bin/git-pre-commit-hook
%py3_shebang_fix \
   %{buildroot}%{_datadir}/inkscape/extensions/inkstitch/bin/inkstitch-fonts-gettext
%py3_shebang_fix \
   %{buildroot}%{_datadir}/inkscape/extensions/inkstitch/bin/inkstitch-tiles-gettext
%py3_shebang_fix \
   %{buildroot}%{_datadir}/inkscape/extensions/inkstitch/bin/pystitch-convert
%py3_shebang_fix \
   %{buildroot}%{_datadir}/inkscape/extensions/inkstitch/bin/pystitch-gettext

%check
%pytest

%files
%license %{_datadir}/inkscape/extensions/inkstitch/LICENSE
%doc README.md
%{_datadir}/inkscape/extensions/inkstitch/


%changelog
%autochangelog
