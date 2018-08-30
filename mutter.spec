%define _disable_ld_no_undefined 1
%define _disable_rebuild_configure 1
%define Werror_cflags %nil

%define url_ver %(echo %{version}|cut -d. -f1,2)

%define api 3.0
%define major 0
%define libname %mklibname %{name} %{major}
%define girname %mklibname %{name}-gir %{api}
%define devname %mklibname -d %{name}

Summary:	Mutter window manager
Name:		mutter
Version:	3.28.3
Release:	1
License:	GPLv2+
Group:		Graphical desktop/GNOME
Url:		http://ftp.gnome.org/pub/gnome/sources/mutter/
Source0:	http://ftp.gnome.org/pub/GNOME/sources/mutter/%{url_ver}/%{name}-%{version}.tar.xz
Patch0:		mutter-disable-cast-align.patch
Patch1:		fix-string-format.patch

BuildRequires:	intltool
BuildRequires:	zenity
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(clutter-1.0)
BuildRequires:	pkgconfig(gbm)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(gnome-doc-utils)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gsettings-desktop-schemas)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(libstartup-notification-1.0)
BuildRequires:	pkgconfig(libcanberra-gtk3)
BuildRequires:	pkgconfig(pango)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(upower-glib)
BuildRequires:	pkgconfig(gnome-desktop-3.0)
BuildRequires:	pkgconfig(xcomposite)
BuildRequires:	pkgconfig(xcursor)
BuildRequires:	pkgconfig(xdamage)
BuildRequires:	pkgconfig(xfixes)
BuildRequires:	pkgconfig(xkbcommon)
BuildRequires:	pkgconfig(xkbcommon-x11)
BuildRequires:	pkgconfig(xkbfile)
BuildRequires:	pkgconfig(xkeyboard-config)
BuildRequires:	pkgconfig(xrender)
BuildRequires:  pkgconfig(libudev)
BuildRequires:	pkgconfig(xtst)
BuildRequires:	pkgconfig(libinput)

Requires:	zenity

%description
Mutter is a simple window manager that integrates nicely with
GNOME.

%package -n %{libname}
Summary:	Libraries for Mutter
Group:		System/Libraries

%description -n %{libname}
This package contains libraries used by Mutter.

%package -n %{girname}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries

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

%prep
%setup -q
%apply_patches

%build
# --enable-maintainer-flags=no is needed bc clutter and cogl pulls
# all kind -Werror flags even when you disable these.
# we also need to disable bc g_logv() and friends are *really* badly broken - crazy -
%configure \
	--disable-scrollkeeper \
	--enable-compile-warnings=no \
	--enable-maintainer-flags=no

%make

%install
%makeinstall_std
%find_lang %{name}

%files -f %{name}.lang
%doc COPYING NEWS
%{_bindir}/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/GConf/gsettings/mutter-schemas.convert
%{_datadir}/glib-2.0/schemas/org.gnome.mutter.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.mutter.wayland.gschema.xml
%{_datadir}/gnome-control-center/keybindings/*.xml
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/plugins
%{_libdir}/%{name}/plugins/default.so
%{_mandir}/man1/*
%{_libexecdir}/mutter-restart-helper
%{_datadir}/applications/mutter-wayland.desktop

%files -n %{libname}
%{_libdir}/libmutter.so.%{major}*

%files -n %{girname}
%{_libdir}/%{name}/Meta-%{api}.typelib

%files -n %{devname}
%{_libdir}/*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_libdir}/%{name}/Meta-%{api}.gir

