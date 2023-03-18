# Disable automatic .la file removal
%global __brp_remove_la_files %nil
%global platform linux-g++
%global qt_module qtbase
%global rpm_macros_dir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_opt_qt5_sysconfdir}/rpm; echo $d)

%global qt_version 5.15.8

Name: opt-qt5-qtbase
Summary: Qt5 - QtBase components
Version: %{qt_version}
Release: 6%{?dist}

# See LGPL_EXCEPTIONS.txt, for exception details
License: LGPL-3.0-only OR GPL-3.0-only WITH Qt-GPL-exception-1.0
Url:     http://qt-project.org/
Source0: %{name}-%{version}.tar.bz2
Source1: qtlogging.ini
# macros
Source10: macros.qt5-qtbase
Source100: qtbase-rpmlintrc

# # Do not check any files in %%{_opt_qt5_plugindir}/platformthemes/ for requires.
# # Those themes are there for platform integration. If the required libraries are
# # not there, the platform to integrate with isn't either. Then Qt will just
# # silently ignore the plugin that fails to load. Thus, there is no need to let
# # RPM drag in gtk3 as a dependency for the GTK+3 dialog support.
# %global __requires_exclude_from ^%{_opt_qt5_plugindir}/platformthemes/.*$
# # filter plugin provides
# %global __provides_exclude_from ^%{_opt_qt5_plugindir}/.*\\.so$

BuildRequires: gcc-c++
BuildRequires: make
BuildRequires: cups-devel
BuildRequires: desktop-file-utils
BuildRequires: findutils
BuildRequires: libjpeg-devel
BuildRequires: libmng-devel
BuildRequires: libtiff-devel
BuildRequires: pkgconfig(alsa)
BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(libdrm)
BuildRequires: pkgconfig(egl)
BuildRequires: pkgconfig(fontconfig)
BuildRequires: pkgconfig(freetype2)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(libsctp)
BuildRequires: pkgconfig(libpng)
BuildRequires: pkgconfig(udev)
BuildRequires: pkgconfig(mtdev)
BuildRequires: pkgconfig(libxslt)
BuildRequires: pkgconfig(openssl)
BuildRequires: pkgconfig(libpulse) pkgconfig(libpulse-mainloop-glib)
#BuildRequires: pkgconfig(libinput)
BuildRequires: pkgconfig(libsystemd)
%global vulkan 0
#BuildRequires: pkgconfig(vulkan)
BuildRequires: pkgconfig(glesv2)
BuildRequires: pkgconfig(sqlite3) >= 3.7
BuildRequires: pkgconfig(harfbuzz) >= 0.9.42
BuildRequires: pkgconfig(icu-i18n)
BuildRequires: pkgconfig(zlib)
BuildRequires: pkgconfig(libzstd)
BuildRequires: pkgconfig(gbm)
BuildRequires: pkgconfig(libproxy-1.0)
BuildRequires: pkgconfig(xkbcommon)
BuildRequires: perl
BuildRequires: python3-base
BuildRequires: opt-qt5-rpm-macros

Requires: %{name}-common = %{version}-%{release}


%description
Qt is a software toolkit for developing applications.

This package contains base tools, like string, xml, and network
handling.

%package common
Summary: Common files for Qt5
Requires: %{name} = %{version}-%{release}
BuildArch: noarch
%description common
%{summary}.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: %{name}-gui%{?_isa}
Requires: libEGL-devel
Requires: pkgconfig(glesv2)
%if 0%{?vulkan}
Requires: pkgconfig(vulkan)
%endif
Requires: opt-qt5-rpm-macros
%description devel
%{summary}.

%package private-devel
Summary: Development files for %{name} private APIs
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
# QtPrintSupport/private requires cups/ppd.h
Requires: cups-devel
%description private-devel
%{summary}.

%package static
Summary: Static library files for %{name}
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
Requires: pkgconfig(fontconfig)
Requires: pkgconfig(glib-2.0)
#Requires: pkgconfig(libinput)
Requires: pkgconfig(xkbcommon)
Requires: pkgconfig(zlib)

%description static
%{summary}.

# debating whether to do 1 subpkg per library or not -- rex
%package gui
Summary: Qt5 GUI-related libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description gui
Qt5 libraries used for drawing widgets and OpenGL items.


%prep
%setup -q -n %{name}-%{version}/upstream

# # use proper perl interpretter so autodeps work as expected
# sed -i -e "s|^#!/usr/bin/env perl$|#!%{__perl}|" \
#  bin/fixqt4headers.pl \
#  bin/syncqt.pl \
#  mkspecs/features/data/unix/findclasslist.pl

%build
touch .git

./configure \
  -verbose \
  -confirm-license \
  -opensource \
  -prefix %{_opt_qt5_prefix} \
  -archdatadir %{_opt_qt5_archdatadir} \
  -bindir %{_opt_qt5_bindir} \
  -libdir %{_opt_qt5_libdir} \
  -libexecdir %{_opt_qt5_libexecdir} \
  -datadir %{_opt_qt5_datadir} \
  -docdir %{_opt_qt5_docdir} \
  -examplesdir %{_opt_qt5_examplesdir} \
  -headerdir %{_opt_qt5_headerdir} \
  -importdir %{_opt_qt5_importdir} \
  -plugindir %{_opt_qt5_plugindir} \
  -sysconfdir %{_opt_qt5_sysconfdir} \
  -translationdir %{_opt_qt5_translationdir} \
  -platform %{platform} \
  -release \
  -shared \
  -no-openvg \
  -no-pch \
  -no-reduce-relocations \
  -no-separate-debug-info \
  -no-strip \
  -no-sql-ibase \
  -no-sql-mysql \
  -no-sql-odbc \
  -no-sql-psql \
  -no-sql-sqlite2 \
  -no-sql-tds \
  -no-use-gold-linker \
  -no-xcb \
  -nomake examples \
  -nomake tests \
  -dbus-linked \
  -egl -eglfs \
  -fontconfig \
  -gbm \
  -icu \
  -glib \
  -kms \
  -opengl es2 \
  -openssl-linked \
  -plugin-sql-sqlite \
  -system-harfbuzz \
  -system-freetype \
  -system-libpng \
  -system-libjpeg \
  -system-proxies \
  -system-sqlite \
  -system-zlib \
  -xkbcommon

%make_build -C qmake all binary \
  QMAKE_STRIP=

%make_build


%install
make install INSTALL_ROOT=%{buildroot}

mkdir -p %{buildroot}%{_opt_qt5_datadir}
install -m644 -p -D %{SOURCE1} %{buildroot}%{_opt_qt5_datadir}/qtlogging.ini

# Qt5.pc
mkdir -p %{buildroot}%{_opt_qt5_libdir}/pkgconfig
cat >%{buildroot}%{_opt_qt5_libdir}/pkgconfig/Qt5.pc<<EOF
prefix=%{_opt_qt5_prefix}
archdatadir=%{_opt_qt5_archdatadir}
bindir=%{_opt_qt5_bindir}
datadir=%{_opt_qt5_datadir}

docdir=%{_opt_qt5_docdir}
examplesdir=%{_opt_qt5_examplesdir}
headerdir=%{_opt_qt5_headerdir}
importdir=%{_opt_qt5_importdir}
libdir=%{_opt_qt5_libdir}
libexecdir=%{_opt_qt5_libexecdir}
moc=%{_opt_qt5_bindir}/moc
plugindir=%{_opt_qt5_plugindir}
qmake=%{_opt_qt5_bindir}/qmake
settingsdir=%{_opt_qt5_settingsdir}
sysconfdir=%{_opt_qt5_sysconfdir}
translationdir=%{_opt_qt5_translationdir}

Name: Qt5
Description: Qt5 Configuration
Version: 5.15.8
EOF

# rpm macros
install -p -m644 -D %{SOURCE10} \
  %{buildroot}%{rpm_macros_dir}/macros.qt5-qtbase
sed -i \
  -e "s|@@NAME@@|%{name}|g" \
  -e "s|@@EPOCH@@|%{?epoch}%{!?epoch:0}|g" \
  -e "s|@@VERSION@@|%{version}|g" \
  -e "s|@@EVR@@|%{?epoch:%{epoch:}}%{qt_version}-%{release}|g" \
  %{buildroot}%{rpm_macros_dir}/macros.qt5-qtbase

# create/own dirs
mkdir -p %{buildroot}{%{_opt_qt5_archdatadir}/mkspecs/modules,%{_opt_qt5_importdir},%{_opt_qt5_libexecdir},%{_opt_qt5_plugindir}/{designer,iconengines,script,styles},%{_opt_qt5_translationdir}}
mkdir -p %{buildroot}%{_opt_qt5_sysconfdir}/xdg/QtProject

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_opt_qt5_libdir}
for prl_file in libQt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd

# install privat headers for qtxcb
mkdir -p %{buildroot}%{_opt_qt5_headerdir}/QtXcb
install -m 644 src/plugins/platforms/xcb/*.h %{buildroot}%{_opt_qt5_headerdir}/QtXcb/

# drop Qt5Bootstrap from -static (#2017661)
rm -f %{buildroot}%{_opt_qt5_libdir}/libQt5Bootstrap.*a
rm -f %{buildroot}%{_opt_qt5_libdir}/libQt5Bootstrap.prl


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post gui -p /sbin/ldconfig
%postun gui -p /sbin/ldconfig

%files
%license LICENSE.FDL
%license LICENSE.GPL*
%license LICENSE.LGPL*
%dir %{_opt_qt5_sysconfdir}/xdg/QtProject/
%{_opt_qt5_libdir}/libQt5Concurrent.so.5*
%{_opt_qt5_libdir}/libQt5Core.so.5*
%{_opt_qt5_libdir}/libQt5DBus.so.5*
%{_opt_qt5_libdir}/libQt5Network.so.5*
%{_opt_qt5_libdir}/libQt5Sql.so.5*
%{_opt_qt5_libdir}/libQt5Test.so.5*
%{_opt_qt5_libdir}/libQt5Xml.so.5*
%dir %{_opt_qt5_libdir}/cmake/
%dir %{_opt_qt5_libdir}/cmake/Qt5/
%dir %{_opt_qt5_libdir}/cmake/Qt5Concurrent/
%dir %{_opt_qt5_libdir}/cmake/Qt5Core/
%dir %{_opt_qt5_libdir}/cmake/Qt5DBus/
%dir %{_opt_qt5_libdir}/cmake/Qt5Gui/
%dir %{_opt_qt5_libdir}/cmake/Qt5Network/
%dir %{_opt_qt5_libdir}/cmake/Qt5OpenGL/
%dir %{_opt_qt5_libdir}/cmake/Qt5PrintSupport/
%dir %{_opt_qt5_libdir}/cmake/Qt5Sql/
%dir %{_opt_qt5_libdir}/cmake/Qt5Test/
%dir %{_opt_qt5_libdir}/cmake/Qt5Widgets/
%dir %{_opt_qt5_libdir}/cmake/Qt5Xml/
%dir %{_opt_qt5_docdir}/
%{_opt_qt5_docdir}/global/
%{_opt_qt5_docdir}/config/
%{_opt_qt5_importdir}/
%{_opt_qt5_translationdir}/
%dir %{_opt_qt5_prefix}/
%dir %{_opt_qt5_archdatadir}/
%dir %{_opt_qt5_datadir}/
%{_opt_qt5_datadir}/qtlogging.ini
%dir %{_opt_qt5_libexecdir}/
%dir %{_opt_qt5_plugindir}/
%dir %{_opt_qt5_plugindir}/bearer/
%{_opt_qt5_plugindir}/bearer/libqconnmanbearer.so
%{_opt_qt5_plugindir}/bearer/libqgenericbearer.so
%{_opt_qt5_plugindir}/bearer/libqnmbearer.so
%{_opt_qt5_libdir}/cmake/Qt5Network/Qt5Network_QConnmanEnginePlugin.cmake
%{_opt_qt5_libdir}/cmake/Qt5Network/Qt5Network_QGenericEnginePlugin.cmake
%{_opt_qt5_libdir}/cmake/Qt5Network/Qt5Network_QNetworkManagerEnginePlugin.cmake
%dir %{_opt_qt5_plugindir}/designer/
%dir %{_opt_qt5_plugindir}/generic/
%dir %{_opt_qt5_plugindir}/iconengines/
%dir %{_opt_qt5_plugindir}/imageformats/
%dir %{_opt_qt5_plugindir}/platforminputcontexts/
%dir %{_opt_qt5_plugindir}/platforms/
%dir %{_opt_qt5_plugindir}/platformthemes/
%dir %{_opt_qt5_plugindir}/printsupport/
%dir %{_opt_qt5_plugindir}/script/
%dir %{_opt_qt5_plugindir}/sqldrivers/
%dir %{_opt_qt5_plugindir}/styles/
%{_opt_qt5_plugindir}/sqldrivers/libqsqlite.so
%{_opt_qt5_libdir}/cmake/Qt5Sql/Qt5Sql_QSQLiteDriverPlugin.cmake

%files common
# mostly empty for now, consider: filesystem/dir ownership, licenses
%{rpm_macros_dir}/macros.qt5-qtbase

%files devel
%dir %{_opt_qt5_bindir}
%{_opt_qt5_bindir}/moc*
%{_opt_qt5_bindir}/qdbuscpp2xml*
%{_opt_qt5_bindir}/qdbusxml2cpp*
%{_opt_qt5_bindir}/qmake*
%{_opt_qt5_bindir}/rcc*
%{_opt_qt5_bindir}/syncqt*
%{_opt_qt5_bindir}/uic*
%{_opt_qt5_bindir}/qlalr
%{_opt_qt5_bindir}/fixqt4headers.pl
%{_opt_qt5_bindir}/qvkgen
%dir %{_opt_qt5_headerdir}
%{_opt_qt5_headerdir}/QtConcurrent/
%{_opt_qt5_headerdir}/QtCore/
%{_opt_qt5_headerdir}/QtDBus/
%{_opt_qt5_headerdir}/QtGui/
%{_opt_qt5_headerdir}/QtNetwork/
%{_opt_qt5_headerdir}/QtOpenGL/
%{_opt_qt5_headerdir}/QtPlatformHeaders/
%{_opt_qt5_headerdir}/QtPrintSupport/
%{_opt_qt5_headerdir}/QtSql/
%{_opt_qt5_headerdir}/QtTest/
%{_opt_qt5_headerdir}/QtWidgets/
%{_opt_qt5_headerdir}/QtXcb/
%{_opt_qt5_headerdir}/QtXml/
%{_opt_qt5_headerdir}/QtEglFSDeviceIntegration
%{_opt_qt5_headerdir}/QtInputSupport
%{_opt_qt5_headerdir}/QtEdidSupport
%{_opt_qt5_headerdir}/QtXkbCommonSupport
%{_opt_qt5_archdatadir}/mkspecs/
%{_opt_qt5_libdir}/libQt5Concurrent.prl
%{_opt_qt5_libdir}/libQt5Concurrent.so
%{_opt_qt5_libdir}/libQt5Core.prl
%{_opt_qt5_libdir}/libQt5Core.so
%{_opt_qt5_libdir}/libQt5DBus.prl
%{_opt_qt5_libdir}/libQt5DBus.so
%{_opt_qt5_libdir}/libQt5Gui.prl
%{_opt_qt5_libdir}/libQt5Gui.so
%{_opt_qt5_libdir}/libQt5Network.prl
%{_opt_qt5_libdir}/libQt5Network.so
%{_opt_qt5_libdir}/libQt5OpenGL.prl
%{_opt_qt5_libdir}/libQt5OpenGL.so
%{_opt_qt5_libdir}/libQt5PrintSupport.prl
%{_opt_qt5_libdir}/libQt5PrintSupport.so
%{_opt_qt5_libdir}/libQt5Sql.prl
%{_opt_qt5_libdir}/libQt5Sql.so
%{_opt_qt5_libdir}/libQt5Test.prl
%{_opt_qt5_libdir}/libQt5Test.so
%{_opt_qt5_libdir}/libQt5Widgets.prl
%{_opt_qt5_libdir}/libQt5Widgets.so
#{_opt_qt5_libdir}/libQt5XcbQpa.prl
#{_opt_qt5_libdir}/libQt5XcbQpa.so
%{_opt_qt5_libdir}/libQt5Xml.prl
%{_opt_qt5_libdir}/libQt5Xml.so
%{_opt_qt5_libdir}/libQt5EglFSDeviceIntegration.prl
%{_opt_qt5_libdir}/libQt5EglFSDeviceIntegration.so
%{_opt_qt5_libdir}/cmake/Qt5/Qt5Config*.cmake
%{_opt_qt5_libdir}/cmake/Qt5Concurrent/Qt5ConcurrentConfig*.cmake
%{_opt_qt5_libdir}/cmake/Qt5Core/Qt5CoreConfig*.cmake
%{_opt_qt5_libdir}/cmake/Qt5Core/Qt5CoreMacros.cmake
%{_opt_qt5_libdir}/cmake/Qt5Core/Qt5CTestMacros.cmake
%{_opt_qt5_libdir}/cmake/Qt5DBus/Qt5DBusConfig*.cmake
%{_opt_qt5_libdir}/cmake/Qt5DBus/Qt5DBusMacros.cmake
%{_opt_qt5_libdir}/cmake/Qt5Gui/Qt5GuiConfig*.cmake
%{_opt_qt5_libdir}/cmake/Qt5Network/Qt5NetworkConfig*.cmake
%{_opt_qt5_libdir}/cmake/Qt5OpenGL/Qt5OpenGLConfig*.cmake
%{_opt_qt5_libdir}/cmake/Qt5PrintSupport/Qt5PrintSupportConfig*.cmake
%{_opt_qt5_libdir}/cmake/Qt5Sql/Qt5SqlConfig*.cmake
%{_opt_qt5_libdir}/cmake/Qt5Test/Qt5TestConfig*.cmake
%{_opt_qt5_libdir}/cmake/Qt5Widgets/Qt5WidgetsConfig*.cmake
%{_opt_qt5_libdir}/cmake/Qt5Widgets/Qt5WidgetsMacros.cmake
%{_opt_qt5_libdir}/cmake/Qt5Xml/Qt5XmlConfig*.cmake
%{_opt_qt5_libdir}/cmake/Qt5/Qt5ModuleLocation.cmake
%{_opt_qt5_libdir}/cmake/Qt5AccessibilitySupport/
%{_opt_qt5_libdir}/cmake/Qt5DeviceDiscoverySupport/
%{_opt_qt5_libdir}/cmake/Qt5EdidSupport/
%{_opt_qt5_libdir}/cmake/Qt5EglFSDeviceIntegration/
%{_opt_qt5_libdir}/cmake/Qt5EglFsKmsSupport/
%{_opt_qt5_libdir}/cmake/Qt5EglSupport/
%{_opt_qt5_libdir}/cmake/Qt5EventDispatcherSupport/
%{_opt_qt5_libdir}/cmake/Qt5FbSupport/
%{_opt_qt5_libdir}/cmake/Qt5FontDatabaseSupport/
#{_opt_qt5_libdir}/cmake/Qt5GlxSupport/
%{_opt_qt5_libdir}/cmake/Qt5InputSupport/
%{_opt_qt5_libdir}/cmake/Qt5KmsSupport/
#{_opt_qt5_libdir}/cmake/Qt5LinuxAccessibilitySupport/
%{_opt_qt5_libdir}/cmake/Qt5PlatformCompositorSupport/
%{_opt_qt5_libdir}/cmake/Qt5ServiceSupport/
%{_opt_qt5_libdir}/cmake/Qt5ThemeSupport/
#{_opt_qt5_libdir}/cmake/Qt5XcbQpa/
%{_opt_qt5_libdir}/cmake/Qt5XkbCommonSupport/
%{_opt_qt5_libdir}/metatypes/qt5core_metatypes.json
%{_opt_qt5_libdir}/metatypes/qt5gui_metatypes.json
%{_opt_qt5_libdir}/metatypes/qt5widgets_metatypes.json
%{_opt_qt5_libdir}/pkgconfig/Qt5.pc
%{_opt_qt5_libdir}/pkgconfig/Qt5Concurrent.pc
%{_opt_qt5_libdir}/pkgconfig/Qt5Core.pc
%{_opt_qt5_libdir}/pkgconfig/Qt5DBus.pc
%{_opt_qt5_libdir}/pkgconfig/Qt5Gui.pc
%{_opt_qt5_libdir}/pkgconfig/Qt5Network.pc
%{_opt_qt5_libdir}/pkgconfig/Qt5OpenGL.pc
%{_opt_qt5_libdir}/pkgconfig/Qt5PrintSupport.pc
%{_opt_qt5_libdir}/pkgconfig/Qt5Sql.pc
%{_opt_qt5_libdir}/pkgconfig/Qt5Test.pc
%{_opt_qt5_libdir}/pkgconfig/Qt5Widgets.pc
%{_opt_qt5_libdir}/pkgconfig/Qt5Xml.pc
%{_opt_qt5_libdir}/libQt5EglFsKmsSupport.prl
%{_opt_qt5_libdir}/libQt5EglFsKmsSupport.so
%{_opt_qt5_bindir}/tracegen
## private-devel globs
# keep mkspecs/modules stuff  in -devel for now, https://bugzilla.redhat.com/show_bug.cgi?id=1705280
%{_opt_qt5_archdatadir}/mkspecs/modules/qt_lib_*_private.pri
%exclude %{_opt_qt5_headerdir}/*/%{qt_version}/

%files private-devel
%{_opt_qt5_headerdir}/*/%{qt_version}/
#{_opt_qt5_archdatadir}/mkspecs/modules/qt_lib_*_private.pri

%files static
%{_opt_qt5_headerdir}/QtOpenGLExtensions/
%{_opt_qt5_libdir}/libQt5OpenGLExtensions.*a
%{_opt_qt5_libdir}/libQt5OpenGLExtensions.prl
%{_opt_qt5_libdir}/cmake/Qt5OpenGLExtensions/
%{_opt_qt5_libdir}/pkgconfig/Qt5OpenGLExtensions.pc
%{_opt_qt5_libdir}/libQt5AccessibilitySupport.*a
%{_opt_qt5_libdir}/libQt5AccessibilitySupport.prl
%{_opt_qt5_headerdir}/QtAccessibilitySupport
%{_opt_qt5_libdir}/libQt5DeviceDiscoverySupport.*a
%{_opt_qt5_libdir}/libQt5DeviceDiscoverySupport.prl
%{_opt_qt5_headerdir}/QtDeviceDiscoverySupport
%{_opt_qt5_libdir}/libQt5EglSupport.*a
%{_opt_qt5_libdir}/libQt5EglSupport.prl
%{_opt_qt5_headerdir}/QtEglSupport
%{_opt_qt5_libdir}/libQt5EventDispatcherSupport.*a
%{_opt_qt5_libdir}/libQt5EventDispatcherSupport.prl
%{_opt_qt5_headerdir}/QtEventDispatcherSupport
%{_opt_qt5_libdir}/libQt5FbSupport.*a
%{_opt_qt5_libdir}/libQt5FbSupport.prl
%{_opt_qt5_headerdir}/QtFbSupport
%{_opt_qt5_libdir}/libQt5FontDatabaseSupport.*a
%{_opt_qt5_libdir}/libQt5FontDatabaseSupport.prl
%{_opt_qt5_headerdir}/QtFontDatabaseSupport
#{_opt_qt5_libdir}/libQt5GlxSupport.*a
#{_opt_qt5_libdir}/libQt5GlxSupport.prl
#{_opt_qt5_headerdir}/QtGlxSupport
%{_opt_qt5_libdir}/libQt5InputSupport.*a
%{_opt_qt5_libdir}/libQt5InputSupport.prl
#{_opt_qt5_libdir}/libQt5LinuxAccessibilitySupport.*a
#{_opt_qt5_libdir}/libQt5LinuxAccessibilitySupport.prl
#{_opt_qt5_headerdir}/QtLinuxAccessibilitySupport
%{_opt_qt5_libdir}/libQt5PlatformCompositorSupport.*a
%{_opt_qt5_libdir}/libQt5PlatformCompositorSupport.prl
%{_opt_qt5_headerdir}/QtPlatformCompositorSupport
%{_opt_qt5_libdir}/libQt5ServiceSupport.*a
%{_opt_qt5_libdir}/libQt5ServiceSupport.prl
%{_opt_qt5_headerdir}/QtServiceSupport
%{_opt_qt5_libdir}/libQt5ThemeSupport.*a
%{_opt_qt5_libdir}/libQt5ThemeSupport.prl
%{_opt_qt5_headerdir}/QtThemeSupport
%{_opt_qt5_libdir}/libQt5KmsSupport.*a
%{_opt_qt5_libdir}/libQt5KmsSupport.prl
%{_opt_qt5_headerdir}/QtKmsSupport
%{_opt_qt5_libdir}/libQt5EdidSupport.*a
%{_opt_qt5_libdir}/libQt5EdidSupport.prl
%{_opt_qt5_libdir}/libQt5XkbCommonSupport.*a
%{_opt_qt5_libdir}/libQt5XkbCommonSupport.prl
%if 0%{?vulkan}
%{_opt_qt5_headerdir}/QtVulkanSupport/
%{_opt_qt5_libdir}/cmake/Qt5VulkanSupport/
%{_opt_qt5_libdir}/libQt5VulkanSupport.*a
%{_opt_qt5_libdir}/libQt5VulkanSupport.prl
%endif

%files gui
%{_opt_qt5_libdir}/libQt5Gui.so.5*
%{_opt_qt5_libdir}/libQt5OpenGL.so.5*
%{_opt_qt5_libdir}/libQt5PrintSupport.so.5*
%{_opt_qt5_libdir}/libQt5Widgets.so.5*
#{_opt_qt5_libdir}/libQt5XcbQpa.so.5*
%{_opt_qt5_plugindir}/generic/libqevdevkeyboardplugin.so
%{_opt_qt5_plugindir}/generic/libqevdevmouseplugin.so
%{_opt_qt5_plugindir}/generic/libqevdevtabletplugin.so
%{_opt_qt5_plugindir}/generic/libqevdevtouchplugin.so
#{_opt_qt5_plugindir}/generic/libqlibinputplugin.so
#{_opt_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QLibInputPlugin.cmake
%{_opt_qt5_plugindir}/generic/libqtuiotouchplugin.so
%{_opt_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QEvdevKeyboardPlugin.cmake
%{_opt_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QEvdevMousePlugin.cmake
%{_opt_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QEvdevTabletPlugin.cmake
%{_opt_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QEvdevTouchScreenPlugin.cmake
%{_opt_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QTuioTouchPlugin.cmake
%{_opt_qt5_plugindir}/imageformats/libqgif.so
%{_opt_qt5_plugindir}/imageformats/libqico.so
%{_opt_qt5_plugindir}/imageformats/libqjpeg.so
%{_opt_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QGifPlugin.cmake
%{_opt_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QICOPlugin.cmake
%{_opt_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QJpegPlugin.cmake
%{_opt_qt5_plugindir}/platforminputcontexts/libcomposeplatforminputcontextplugin.so
%{_opt_qt5_plugindir}/platforminputcontexts/libibusplatforminputcontextplugin.so
%{_opt_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QComposePlatformInputContextPlugin.cmake
%{_opt_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QIbusPlatformInputContextPlugin.cmake
%{_opt_qt5_libdir}/libQt5EglFSDeviceIntegration.so.5*
%{_opt_qt5_libdir}/libQt5EglFsKmsSupport.so.5*
%{_opt_qt5_plugindir}/platforms/libqeglfs.so
%{_opt_qt5_plugindir}/platforms/libqminimalegl.so
%dir %{_opt_qt5_plugindir}/egldeviceintegrations/
%{_opt_qt5_plugindir}/egldeviceintegrations/libqeglfs-kms-integration.so
#{_opt_qt5_plugindir}/egldeviceintegrations/libqeglfs-x11-integration.so
#{_opt_qt5_plugindir}/xcbglintegrations/libqxcb-egl-integration.so
%{_opt_qt5_plugindir}/egldeviceintegrations/libqeglfs-kms-egldevice-integration.so
%{_opt_qt5_plugindir}/egldeviceintegrations/libqeglfs-emu-integration.so
%{_opt_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QMinimalEglIntegrationPlugin.cmake
%{_opt_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QEglFSIntegrationPlugin.cmake
%{_opt_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QEglFSKmsGbmIntegrationPlugin.cmake
#{_opt_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QXcbEglIntegrationPlugin.cmake
%{_opt_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QEglFSKmsEglDeviceIntegrationPlugin.cmake
%{_opt_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QEglFSEmulatorIntegrationPlugin.cmake
%{_opt_qt5_plugindir}/platforms/libqlinuxfb.so
%{_opt_qt5_plugindir}/platforms/libqminimal.so
%{_opt_qt5_plugindir}/platforms/libqoffscreen.so
#{_opt_qt5_plugindir}/platforms/libqxcb.so
%{_opt_qt5_plugindir}/platforms/libqvnc.so
%{_opt_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QLinuxFbIntegrationPlugin.cmake
%{_opt_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QMinimalIntegrationPlugin.cmake
%{_opt_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QOffscreenIntegrationPlugin.cmake
%{_opt_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QVncIntegrationPlugin.cmake
#{_opt_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QXcbIntegrationPlugin.cmake
#{_opt_qt5_plugindir}/xcbglintegrations/libqxcb-glx-integration.so
#{_opt_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QXcbGlxIntegrationPlugin.cmake
%{_opt_qt5_plugindir}/platformthemes/libqxdgdesktopportal.so
#{_opt_qt5_plugindir}/platformthemes/libqgtk3.so
%{_opt_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QXdgDesktopPortalThemePlugin.cmake
#{_opt_qt5_libdir}/cmake/Qt5Gui/Qt5Gui_QGtk3ThemePlugin.cmake
%{_opt_qt5_plugindir}/printsupport/libcupsprintersupport.so
%{_opt_qt5_libdir}/cmake/Qt5PrintSupport/Qt5PrintSupport_QCupsPrinterSupportPlugin.cmake
