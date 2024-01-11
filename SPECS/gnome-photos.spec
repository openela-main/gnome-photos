%global cairo_version 1.14.0
%global gdata_version 0.15.2
%global gdk_pixbuf_version 2.32.0
%global gegl_version 0.4.0
%global gettext_version 0.19.8
%global glib2_version 2.44.0
%global goa_version 3.8.0
%global gtk3_version 3.22.16
%global tracker_version 2.0.3
%global tracker_miners_version 2.0.4

Name:          gnome-photos
Version:       3.28.1
Release:       4%{?dist}
Summary:       Access, organize and share your photos on GNOME

# GNOME Photos itself is GPLv3+, but the egg-* files and the
# bundled libgd are LGPLv2+
License:       GPLv3+ and LGPLv2+
URL:           https://wiki.gnome.org/Apps/Photos
Source0:       http://download.gnome.org/sources/%{name}/3.28/%{name}-%{version}.tar.xz

# https://bugzilla.redhat.com/show_bug.cgi?id=1605184
Patch0:        gnome-photos-Build-against-gegl04.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1612779
Patch1:        gnome-photos-Add-a-manual.patch

BuildRequires: autoconf automake gettext-devel libtool yelp-tools
BuildRequires: pkgconfig(babl)
BuildRequires: desktop-file-utils
BuildRequires: docbook-style-xsl
BuildRequires: gettext >= %{gettext_version}
BuildRequires: pkgconfig(cairo) >= %{cairo_version}
BuildRequires: pkgconfig(cairo-gobject) >= %{cairo_version}
BuildRequires: pkgconfig(gdk-pixbuf-2.0) >= %{gdk_pixbuf_version}
BuildRequires: pkgconfig(gegl-0.4) >= %{gegl_version}
BuildRequires: pkgconfig(gio-2.0) >= %{glib2_version}
BuildRequires: pkgconfig(glib-2.0) >= %{glib2_version}
BuildRequires: pkgconfig(gobject-2.0) >= %{glib2_version}
BuildRequires: pkgconfig(goa-1.0) >= %{goa_version}
BuildRequires: pkgconfig(grilo-0.3)
BuildRequires: pkgconfig(gsettings-desktop-schemas)
BuildRequires: pkgconfig(gtk+-3.0) >= %{gtk3_version}
BuildRequires: itstool
BuildRequires: pkgconfig(libdazzle-1.0)
BuildRequires: pkgconfig(libgdata) >= %{gdata_version}
BuildRequires: pkgconfig(gexiv2)
BuildRequires: libjpeg-turbo-devel
BuildRequires: libxslt
BuildRequires: pkgconfig(tracker-control-2.0) >= %{tracker_version}
BuildRequires: pkgconfig(tracker-sparql-2.0) >= %{tracker_version}
BuildRequires: pkgconfig(libgfbgraph-0.2)
BuildRequires: pkgconfig(geocode-glib-1.0)
BuildRequires: python3-devel

Requires:      baobab
Requires:      dleyna-renderer
Requires:      gdk-pixbuf2%{?isa} >= %{gdk_pixbuf_version}
Requires:      gegl04%{?_isa} >= %{gegl_version}
Requires:      gettext-libs%{?isa} >= %{gettext_version}
Requires:      gnome-online-miners >= 3.11.3
Requires:      gnome-settings-daemon
Requires:      gtk3%{?_isa} >= %{gtk3_version}
Requires:      libgdata%{?_isa} >= %{gdata_version}
Requires:      tracker >= %{tracker_version}
Requires:      tracker-miners >= %{tracker_miners_version}

# libgd is not meant to be installed as a system-wide shared library.
# It is just a way for GNOME applications to share widgets and other common
# code on an ad-hoc basis.
Provides: bundled(libgd)


%description
A simple application to access, organize and share your photos on
GNOME. It is meant to be a simple and elegant replacement for using a
file manager to deal with photos. Seamless cloud integration is offered
through GNOME Online Accounts.


%package       tests
Summary:       Tests for %{name}

%description   tests
This package contains the installable tests for %{name}.


%prep
%setup -q
%patch0 -p1
%patch1 -p1

pathfix.py -i %{__python3} -n tests/basic.py
autoreconf -i -f


%build
%configure --enable-installed-tests --disable-silent-rules
%make_build


%install
%make_install

# Upstream doesn't install with desktop-file-install, so let's check
desktop-file-validate %{buildroot}%{_datadir}/applications/org.gnome.Photos.desktop

%find_lang %{name} --with-gnome



%files -f %{name}.lang
%{_bindir}/%{name}
%{_datadir}/metainfo/org.gnome.Photos.appdata.xml
%{_datadir}/applications/org.gnome.Photos.desktop
%{_datadir}/dbus-1/services/org.gnome.Photos.service
%{_datadir}/glib-2.0/schemas/org.gnome.photos.gschema.xml
%{_datadir}/gnome-shell/
%{_datadir}/icons/hicolor/*/apps/org.gnome.Photos.png
%{_datadir}/icons/hicolor/scalable/apps/org.gnome.Photos-symbolic.svg
%{_datadir}/man/man1/%{name}.1*
%{_docdir}/%{name}
%{_libexecdir}/%{name}-thumbnailer

%files tests
%{_libexecdir}/installed-tests/Photos
%{_datadir}/installed-tests


%changelog
* Wed Nov 11 2020 Debarshi Ray <rishi@fedoraproject.org> - 3.28.1-4
- Add a manual
Resolves: #1612779

* Tue Feb 11 2020 Debarshi Ray <rishi@fedoraproject.org> - 3.28.1-3
- Disable Python 2 during the build - itstool doesn't need it anymore
Resolves: #1597806

* Mon Dec 17 2018 Ray Strode <rstrode@redhat.com> - 3.28.1-2
- rebuild

* Wed Sep 05 2018 Debarshi Ray <rishi@fedoraproject.org> - 3.28.1-1
- Update to 3.28.1

* Thu Jul 26 2018 Debarshi Ray <rishi@fedoraproject.org> - 3.28.0-4
- Build against gegl04
Resolves: #1605184

* Tue Jul 03 2018 Debarshi Ray <rishi@fedoraproject.org> - 3.28.0-3
- Drop the run-time requirement on ImageMagick
- Enable Python 2 during the build for itstool
Resolves: #1564997

* Thu Jun 14 2018 Petr Viktorin <pviktori@redhat.com> - 3.28.0-2
- Change shebang for a test script to Python 3

* Thu Mar 15 2018 Kalev Lember <klember@redhat.com> - 3.28.0-1
- Update to 3.28.0

* Wed Mar 07 2018 Debarshi Ray <rishi@fedoraproject.org> - 3.27.92-1
- Update to 3.27.92

* Mon Feb 19 2018 Debarshi Ray <rishi@fedoraproject.org> - 3.27.90-1
- Update to 3.27.90

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.27.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 12 2018 Debarshi Ray <rishi@fedoraproject.org> - 3.27.4-1
- Update to 3.27.4

* Thu Jan 11 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.27.3-2
- Remove obsolete scriptlets

* Wed Dec 13 2017 Debarshi Ray <rishi@fedoraproject.org> - 3.27.3-1
- Update to 3.27.3

* Tue Oct 24 2017 Debarshi Ray <rishi@fedoraproject.org> - 3.27.1-1
- Update to 3.27.1

* Sun Oct 08 2017 Kalev Lember <klember@redhat.com> - 3.26.1-1
- Update to 3.26.1

* Tue Sep 19 2017 Debarshi Ray <rishi@fedoraproject.org> - 3.26.0-2
- Add run-time dependency on tracker-miners

* Wed Sep 13 2017 Kalev Lember <klember@redhat.com> - 3.26.0-1
- Update to 3.26.0

* Tue Sep 05 2017 Debarshi Ray <rishi@fedoraproject.org> - 3.25.92-1
- Update to 3.25.92

* Wed Aug 23 2017 Debarshi Ray <rishi@fedoraproject.org> - 3.25.91-1
- Update to 3.25.91

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.25.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.25.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 19 2017 Debarshi Ray <rishi@fedoraproject.org> - 3.25.4-1
- Update to 3.25.4

* Wed Jun 21 2017 Debarshi Ray <rishi@fedoraproject.org> - 3.25.3-1
- Update to 3.25.3

* Wed May 10 2017 Debarshi Ray <rishi@fedoraproject.org> - 3.25.1-1
- Update to 3.25.1

* Tue Apr 11 2017 Kalev Lember <klember@redhat.com> - 3.24.1-1
- Update to 3.24.1

* Tue Mar 21 2017 Kalev Lember <klember@redhat.com> - 3.24.0-1
- Update to 3.24.0

* Tue Mar 14 2017 Debarshi Ray <rishi@fedoraproject.org> - 3.23.92-1
- Update to 3.23.92

* Fri Mar 03 2017 Debarshi Ray <rishi@fedoraproject.org> - 3.23.91-1
- Update to 3.23.91

* Mon Feb 20 2017 Debarshi Ray <rishi@fedoraproject.org> - 3.23.90-1
- Update to 3.23.90

* Mon Feb 13 2017 Richard Hughes <rhughes@redhat.com> - 3.23.4-1
- Update to 3.23.4

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.23.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 01 2016 Kalev Lember <klember@redhat.com> - 3.23.2-1
- Update to 3.23.2

* Wed Nov 23 2016 Kalev Lember <klember@redhat.com> - 3.22.2-1
- Update to 3.22.2

* Thu Oct 06 2016 Debarshi Ray <rishi@fedoraproject.org> - 3.22.1-1
- Update to 3.22.1
- Use --disable-silent-rules

* Mon Sep 19 2016 Kalev Lember <klember@redhat.com> - 3.22.0-1
- Update to 3.22.0

* Mon Sep 12 2016 Debarshi Ray <rishi@fedoraproject.org> - 3.21.92-1
- Update to 3.21.92
- Use make_build macro
- Update minimum required versions; use pkgconfig(...) for BRs

* Sat Sep 03 2016 Kalev Lember <klember@redhat.com> - 3.21.91-1
- Update to 3.21.91

* Mon Aug 22 2016 Kalev Lember <klember@redhat.com> - 3.21.90-1
- Update to 3.21.90

* Wed Jul 20 2016 Richard Hughes <rhughes@redhat.com> - 3.21.4-1
- Update to 3.21.4

* Wed Jun 22 2016 Richard Hughes <rhughes@redhat.com> - 3.21.3-1
- Update to 3.21.3

* Tue May 03 2016 Kalev Lember <klember@redhat.com> - 3.21.1-1
- Update to 3.21.1

* Wed Apr 13 2016 Kalev Lember <klember@redhat.com> - 3.20.1-1
- Update to 3.20.1

* Tue Mar 22 2016 Kalev Lember <klember@redhat.com> - 3.20.0-1
- Update to 3.20.0

* Wed Mar 16 2016 Kalev Lember <klember@redhat.com> - 3.19.92-1
- Update to 3.19.92

* Fri Mar 04 2016 Richard Hughes <rhughes@redhat.com> - 3.19.91-1
- Update to 3.19.91

* Thu Feb 18 2016 Richard Hughes <rhughes@redhat.com> - 3.19.90-1
- Update to 3.19.90

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.19.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 29 2016 Debarshi Ray <rishi@fedoraproject.org> - 3.19.4-2
- Use upstreamed screenshots

* Wed Jan 20 2016 Kalev Lember <klember@redhat.com> - 3.19.4-1
- Update to 3.19.4

* Fri Dec 18 2015 Kalev Lember <klember@redhat.com> - 3.19.3-2
- Build with grilo 0.3

* Wed Dec 16 2015 Kalev Lember <klember@redhat.com> - 3.19.3-1
- Update to 3.19.3
- Build with grilo 0.2
- Define minimum gegl version
- Use make_install macro

* Tue Dec 08 2015 Debarshi Ray <rishi@fedoraproject.org> - 3.19.2-1
- Update to 3.19.2

* Tue Nov 10 2015 Kalev Lember <klember@redhat.com> - 3.18.2-1
- Update to 3.18.2

* Mon Oct 12 2015 Kalev Lember <klember@redhat.com> - 3.18.1-1
- Update to 3.18.1

* Tue Sep 22 2015 Kalev Lember <klember@redhat.com> - 3.18.0-1
- Update to 3.18.0

* Wed Jul 22 2015 David King <amigadave@amigadave.com> - 3.17.2-3
- Bump for new gnome-desktop3

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.17.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 29 2015 Debarshi Ray <rishi@fedoraproject.org> - 3.17.2-1
- Update to 3.17.2

* Wed May 13 2015 Debarshi Ray <rishi@fedoraproject.org> - 3.16.2-1
- Update to 3.16.2

* Mon Apr 27 2015 David King <amigadave@amigadave.com> - 3.16.0-3
- Rebuild for libgdata soname bump

* Mon Mar 30 2015 Richard Hughes <rhughes@redhat.com> - 3.16.0-2
- Use better AppData screenshots

* Mon Mar 23 2015 Kalev Lember <kalevlember@gmail.com> - 3.16.0-1
- Update to 3.16.0

* Fri Mar 13 2015 Kalev Lember <kalevlember@gmail.com> - 3.15.91-1
- Update to 3.15.91

* Wed Feb 25 2015 Richard Hughes <rhughes@redhat.com> - 3.15.90-1
- Update to 3.15.90

* Thu Jan 22 2015 Richard Hughes <rhughes@redhat.com> - 3.15.4-1
- Update to 3.15.4

* Fri Dec 19 2014 Richard Hughes <rhughes@redhat.com> - 3.15.3-1
- Update to 3.15.3

* Sat Nov 29 2014 Kalev Lember <kalevlember@gmail.com> - 3.15.2-1
- Update to 3.15.2

* Wed Nov 12 2014 Vadim Rutkovsky <vrutkovs@redhat.com> - 3.14.2-2
- Build installed tests

* Mon Nov 10 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.2-1
- Update to 3.14.2

* Wed Sep 24 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.0-1
- Update to 3.14.0
- Set minimum required versions for libgdata and gtk3

* Wed Sep 17 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.92-1
- Update to 3.13.92

* Fri Sep 05 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.91-1
- Update to 3.13.91
- Include HighContrast icons

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.13.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 24 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.4-1
- Update to 3.13.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 16 2014 Kalev Lember <kalevlember@gmail.com> - 3.12.1-1
- Update to 3.12.1
- Include help files

* Mon Mar 24 2014 Richard Hughes <rhughes@redhat.com> - 3.12.0-1
- Update to 3.12.0

* Tue Mar 18 2014 Richard Hughes <rhughes@redhat.com> - 3.11.92-1
- Update to 3.11.92

* Sat Mar 08 2014 Richard Hughes <rhughes@redhat.com> - 3.11.91-1
- Update to 3.11.91

* Thu Feb 20 2014 Kalev Lember <kalevlember@gmail.com> - 3.11.90-1
- Update to 3.11.90

* Wed Feb 19 2014 Richard Hughes <rhughes@redhat.com> - 3.11.5-2
- Rebuilt for gnome-desktop soname bump

* Thu Feb 06 2014 Kalev Lember <kalevlember@gmail.com> - 3.11.5-1
- Update to 3.11.5

* Wed Jan 15 2014 Richard Hughes <rhughes@redhat.com> - 3.11.4-1
- Update to 3.11.4

* Tue Dec 17 2013 Richard Hughes <rhughes@redhat.com> - 3.11.3-1
- Update to 3.11.3

* Mon Nov 25 2013 Richard Hughes <rhughes@redhat.com> - 3.11.2-1
- Update to 3.11.2

* Thu Nov 14 2013 Richard Hughes <rhughes@redhat.com> - 3.10.2-1
- Update to 3.10.2

* Tue Oct 29 2013 Richard Hughes <rhughes@redhat.com> - 3.10.1-1
- Update to 3.10.1

* Wed Sep 25 2013 Richard Hughes <rhughes@redhat.com> - 3.10.0-1
- Update to 3.10.0

* Wed Sep 18 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.92-1
- Update to 3.9.92
- Include the appdata file

* Wed Sep 04 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.91-1
- Update to 3.9.91

* Thu Aug 22 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.90-1
- Update to 3.9.90

* Sun Aug 04 2013 Debarshi Ray <rishi@fedoraproject.org> - 3.9.5.1-1
- Update to 3.9.5.1

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 16 2013 Debarshi Ray <rishi@fedoraproject.org> - 3.9.4-1
- Update to 3.9.4

* Tue May 14 2013 Richard Hughes <rhughes@redhat.com> - 3.8.2-1
- Update to 3.8.2

* Mon Apr 15 2013 Richard Hughes <rhughes@redhat.com> - 3.8.0-1
- Update to 3.8.0
- Drop upstreamed packages
- Fix BRs

* Thu Feb 21 2013 Kalev Lember <kalevlember@gmail.com> - 3.7.3-6
- Rebuilt for cogl soname bump

* Wed Feb 20 2013 Kalev Lember <kalevlember@gmail.com> - 3.7.3-5
- Rebuilt for libgnome-desktop soname bump

* Mon Jan 28 2013 Matthias Clasen <mclasen@redhat.com> - 3.7.3-4
- Rebuild for new tracker

* Fri Jan 25 2013 Peter Robinson <pbrobinson@fedoraproject.org> 3.7.3-3
- Rebuild for new cogl

* Fri Dec 21 2012 Kalev Lember <kalevlember@gmail.com> - 3.7.3-2
- Rebuilt for libgnome-desktop-3 3.7.3 soname bump

* Wed Dec 19 2012 Debarshi Ray <rishi@fedoraproject.org> - 3.7.3-1
- Update to 3.7.3

* Sat Dec 01 2012 Mathieu Bridon <bochecha@fedoraproject.org> - 3.7.2-4
* Fix based on Ivan's review feedback:
  - Add a comment on the multi-licensing situation

* Thu Nov 29 2012 Mathieu Bridon <bochecha@fedoraproject.org> - 3.7.2-3
* Fixes based on Ivan's review feedback:
  - Fix the upstream URL
  - Fix the License tag
  - Preserve timestamps when installing

* Sun Nov 25 2012 Mathieu Bridon <bochecha@fedoraproject.org> - 3.7.2-2
* Fixes based on Debarshi's review feedback:
  - Fix build requirement on gdk-pixbuf2-devel
  - Add missing Provides on the bundled libgd

* Sun Nov 18 2012 Mathieu Bridon <bochecha@fedoraproject.org> - 3.7.2-1
- Initial package for Fedora.
