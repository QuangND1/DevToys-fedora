# Repackage bản portable chính thức của DevToys thành RPM cho Fedora.
# Version được truyền từ workflow: rpmbuild -bb --define "ver 2.0.9.0" devtoys.spec

%{!?ver: %global ver 0.0.0}

# Binary .NET self-contained: không strip, không debuginfo, không tự dò deps trên DLL/.so đi kèm
%global debug_package %{nil}
%global _build_id_links none
%global __os_install_post %{nil}
%global __arch_install_post %{nil}
%global __requires_exclude_from ^/opt/devtoys/.*$
%global __provides_exclude_from ^/opt/devtoys/.*$

Name:           devtoys
Version:        %{ver}
Release:        1%{?dist}
Summary:        A Swiss Army knife for developers
License:        MIT
URL:            https://github.com/DevToys-app/DevToys
Source0:        devtoys_linux_x64_portable.zip
Source1:        devtoys.png
ExclusiveArch:  x86_64

BuildRequires:  unzip
Requires:       gtk4
Requires:       webkitgtk6.0
Requires:       libicu
Requires:       openssl-libs
Requires:       xdg-dbus-proxy
Requires:       bubblewrap

%description
DevToys: bộ công cụ offline cho developer (JSON/YAML, Base64, JWT, Hash,
RegEx tester, Formatter...). Gói này đóng gói lại bản portable chính thức
từ upstream, kèm sẵn bộ tool mặc định (Plugins/DevToys.Tools).

%prep
%setup -q -c -T
unzip -q %{SOURCE0}

%build
# Không build gì, dùng binary chính thức

%install
install -d %{buildroot}/opt/devtoys
cp -a . %{buildroot}/opt/devtoys/
chmod 0755 %{buildroot}/opt/devtoys/DevToys.Linux

install -d %{buildroot}%{_bindir}
ln -s /opt/devtoys/DevToys.Linux %{buildroot}%{_bindir}/devtoys

install -Dm0644 %{SOURCE1} %{buildroot}%{_datadir}/pixmaps/devtoys.png

install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/devtoys.desktop <<'EOF'
[Desktop Entry]
Name=DevToys
Comment=A Swiss Army knife for developers
Exec=/opt/devtoys/DevToys.Linux
Icon=devtoys
Terminal=false
Type=Application
Categories=Development;Utility;
StartupWMClass=DevToys
EOF

%files
/opt/devtoys
%{_bindir}/devtoys
%{_datadir}/applications/devtoys.desktop
%{_datadir}/pixmaps/devtoys.png

%changelog
* Mon Oct 19 2026 QuangND1 <quang.nd1991@gmail.com> - %{ver}-1
- Repackage upstream portable build
