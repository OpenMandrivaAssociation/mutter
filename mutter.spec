%define _disable_ld_no_undefined 1
%define _disable_rebuild_configure 1
%define Werror_cflags %nil

%define url_ver %(echo %{version}|cut -d. -f1,2)

%define api_m 17
%define api %{api_m}.0
%define major 0
%define libname %mklibname %{name}
%define oldlibname %mklibname %{name} 0
%define girname %mklibname %{name}-gir
%define oldgirname %mklibname %{name}-gir 15.0
%define devname %mklibname -d %{name}

Summary:	Mutter window manager
Name:		mutter
Version:	49.1.1
Release:	1
License:	GPLv2+
Group:		Graphical desktop/GNOME
Url:		https://ftp.gnome.org/pub/gnome/sources/mutter/
Source0:	https://ftp.gnome.org/pub/GNOME/sources/mutter/%{url_ver}/%{name}-%{version}.tar.xz
# Backported from upstream
# Fix crash when locking screen on VMs
Patch0:         0001-clutter-Skip-null-actors-in-create_event_emission_ch.patch

BuildRequires:	intltool
BuildRequires:	gettext
BuildRequires:	gtk-doc
BuildRequires:	zenity-gtk
BuildRequires:	meson
BuildRequires:	cvt
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(clutter-1.0)
BuildRequires:	pkgconfig(lcms2)
BuildRequires:	pkgconfig(colord)
BuildRequires:	pkgconfig(gbm)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(gnome-doc-utils)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gsettings-desktop-schemas)
BuildRequires:	pkgconfig(gnome-settings-daemon)
BuildRequires:	pkgconfig(gudev-1.0)
BuildRequires:	pkgconfig(graphene-gobject-1.0)
BuildRequires:	pkgconfig(harfbuzz-gobject)
BuildRequires:	pkgconfig(libdrm)
BuildRequires:	pkgconfig(libeis-1.0)
BuildRequires:	pkgconfig(libei-1.0)
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	pkgconfig(libwacom)
BuildRequires:	pkgconfig(libpipewire-0.3)
BuildRequires:	pkgconfig(libdisplay-info)
BuildRequires:	x11-server-xvfb
BuildRequires:	x11-server-xwayland
BuildRequires:	wayland-protocols-devel
BuildRequires:	pkgconfig(glycin-2)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(gtk4)
BuildRequires:	pkgconfig(libadwaita-1)
BuildRequires:	pkgconfig(libstartup-notification-1.0)
BuildRequires:	pkgconfig(libcanberra-gtk3)
BuildRequires:	pkgconfig(pango)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(upower-glib)
BuildRequires:	pkgconfig(gnome-desktop-4)
BuildRequires:	pkgconfig(xcomposite)
BuildRequires:	pkgconfig(xcursor)
BuildRequires:	pkgconfig(xdamage)
BuildRequires:	pkgconfig(xfixes)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xkbcommon)
BuildRequires:	pkgconfig(xkbcommon-x11)
BuildRequires:	pkgconfig(xkbfile)
BuildRequires:	pkgconfig(xkeyboard-config)
BuildRequires:	pkgconfig(xrender)
BuildRequires:  pkgconfig(libudev)
BuildRequires:	pkgconfig(libinput)
BuildRequires:	pkgconfig(libxcvt)
BuildRequires:	pkgconfig(wayland-server) >= 1.13.0
BuildRequires:	pkgconfig(wayland-protocols) >= 1.16
BuildRequires:  pkgconfig(wayland-eglstream-protocols)
BuildRequires:	pkgconfig(clutter-wayland-1.0)
#BuildRequires:	pkgconfig(clutter-wayland-compositor-1.0)
BuildRequires:	pkgconfig(clutter-egl-1.0)
BuildRequires:	pkgconfig(cogl-1.0) >= 1.17.1
BuildRequires:	pkgconfig(sysprof-capture-4)
BuildRequires:	sysprof
BuildRequires:	pkgconfig(umockdev-1.0)
BuildRequires:	pkgconfig(xtst)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:	pkgconfig(libglvnd)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(x11-xcb)
BuildRequires:	pkgconfig(wayland-egl)
BuildRequires:	pkgconfig(wayland-protocols)
BuildRequires:	pkgconfig(wayland-server)
BuildRequires:	pkgconfig(xwayland)
BuildRequires:	egl-devel
BuildRequires:	python3dist(python-dbusmock)
BuildRequires:  python-argcomplete
BuildRequires:  python-docutils

Requires:	zenity-gtk
Requires:	%{girname} = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

Requires: python-argcomplete

%description
Mutter is a simple window manager that integrates nicely with
GNOME.

%package -n %{libname}
Summary:	Libraries for Mutter
Group:		System/Libraries
%rename %{oldlibname}

%description -n %{libname}
This package contains libraries used by Mutter.

%package -n %{girname}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries
%rename %{oldgirname}

%description -n %{girname}
GObject Introspection interface description for %{name}.

%package -n %{devname}
Summary:	Libraries and include files with Mutter
Group:		Development/GNOME and GTK+
Requires:	%{libname} = %{version}-%{release}
Requires:	%{girname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This package provides the necessary development libraries and include
files to allow you to develop with Mutter.

%package  tests
Summary:  Tests for the %{name} package
Requires: %{name}%{?_isa} = %{version}-%{release}
 
%description tests
The %{name}-tests package contains tests that can be used to verify
the functionality of the installed %{name} package.

%prep
%autosetup -p1

%build

sed -i "/'-Werror=redundant-decls',/d" meson.build 
%meson  \
	-Dopengl=true \
	-Degl=true \
	-Dglx=true \
	-Dintrospection=true \
	-Dwayland=true \
	-Degl_device=true \
	-Dwayland_eglstream=true \
	-Dxwayland_initfd=enabled \
	-Dremote_desktop=true \
	-Dnative_backend=true \
	-Dinstalled_tests=false \
    -Dcogl_tests=false \
	-Dclutter_tests=false \
 	-Dx11=true

%meson_build

%install
%meson_install
%find_lang %{name}

%files -f %{name}.lang
%doc COPYING NEWS
%{_bindir}/*
#{_datadir}/applications/%{name}.desktop
%{_datadir}/applications/org.gnome.Mutter.Mdk.desktop
%{_datadir}/GConf/gsettings/mutter-schemas.convert
%{_datadir}/glib-2.0/schemas/org.gnome.mutter.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.mutter.wayland.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.mutter.devkit.gschema.xml
%{_datadir}/gnome-control-center/keybindings/*.xml
%{_datadir}/polkit-1/actions/org.gnome.mutter.backlight-helper.policy
%dir %{_libdir}/%{name}-%{api_m}
%dir %{_libdir}/%{name}-%{api_m}/plugins
%{_libdir}/%{name}-%{api_m}/plugins/libdefault.so
%{_mandir}/man1/*
%{_libexecdir}/mutter-restart-helper
%{_libexecdir}/mutter-x11-frames
%{_libexecdir}/mutter-backlight-helper
%{_libexecdir}/mutter-devkit
%{_prefix}/lib/udev/rules.d/61-mutter.rules
#{_datadir}/applications/mutter-wayland.desktop
%{_sysconfdir}/bash_completion.d/gdctl
%{_iconsdir}/hicolor/scalable/apps/org.gnome.Mutter.Mdk.Devel.svg
%{_iconsdir}/hicolor/scalable/apps/org.gnome.Mutter.Mdk.svg
%{_iconsdir}/hicolor/symbolic/apps/org.gnome.Mutter.Mdk-symbolic.svg

%files -n %{libname}
%{_libdir}/libmutter-%{api_m}.so.%{major}*
%{_libdir}/mutter-%{api_m}/libmutter-clutter-%{api_m}.so.%{major}*
%{_libdir}/mutter-%{api_m}/libmutter-cogl-%{api_m}.so.%{major}*
%{_libdir}/mutter-%{api_m}/libmutter-mtk-%{api_m}.so.%{major}*

%files -n %{girname}
%{_libdir}/mutter-%{api_m}/Clutter-%{api_m}.typelib
%{_libdir}/mutter-%{api_m}/Cogl-%{api_m}.typelib
%{_libdir}/mutter-%{api_m}/Meta-%{api_m}.typelib
#{_libdir}/mutter-16/MetaTest-%{api_m}.typelib
%{_libdir}/mutter-%{api_m}/Mtk-%{api_m}.typelib

%files -n %{devname}
%{_libdir}/*.so
%{_libdir}/mutter-%{api_m}/libmutter-clutter-%{api_m}.so
%{_libdir}/mutter-%{api_m}/libmutter-cogl-%{api_m}.so
%{_libdir}/mutter-%{api_m}/libmutter-mtk-%{api_m}.so
%{_libdir}/mutter-%{api_m}/Clutter-%{api_m}.gir
%{_libdir}/mutter-%{api_m}/Cogl-%{api_m}.gir
%{_libdir}/mutter-%{api_m}/Meta-%{api_m}.gir
#{_libdir}/mutter-16/MetaTest-%{api_m}.gir
%{_libdir}/mutter-%{api_m}/Mtk-%{api_m}.gir
%{_includedir}/*
%{_libdir}/pkgconfig/*

%files tests
%{_datadir}/mutter-%{api_m}/tests/
%{_libdir}/mutter-%{api_m}/MetaTest-%{api_m}.gir
%{_libdir}/mutter-%{api_m}/MetaTest-%{api_m}.typelib
