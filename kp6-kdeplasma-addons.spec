#
# Conditional build:
%bcond_without	qtwebengine	# build with Qt6Webengine support
%bcond_with	tests		# build with tests

%ifarch x32 i686
%undefine	with_qtwebengine
%endif

%define		kdeplasmaver	6.5.3
%define		kfver		6.5.0
%define		qtver		6.7.0
%define		kpname		kdeplasma-addons

Summary:	All kind of addons to improve your Plasma experience
Name:		kp6-%{kpname}
Version:	6.5.3
Release:	2
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/plasma/%{kdeplasmaver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	5ff4b367d841c276691f7131c7789174
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6DBus-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel >= %{qtver}
BuildRequires:	Qt6Network-devel >= %{qtver}
BuildRequires:	Qt6Qml-devel >= %{qtver}
BuildRequires:	Qt6Qt5Compat-devel >= %{qtver}
BuildRequires:	Qt6Quick-devel >= %{qtver}
BuildRequires:	Qt6Test-devel >= %{qtver}
%{?with_qtwebengine:BuildRequires:	Qt6WebEngine-devel}
BuildRequires:	Qt6Widgets-devel >= %{qtver}
BuildRequires:	cmake >= 3.16.0
BuildRequires:	kf6-extra-cmake-modules >= %{kfver}
BuildRequires:	kf6-kauth-devel >= %{kfver}
BuildRequires:	kf6-kcmutils-devel >= %{kfver}
BuildRequires:	kf6-kconfig-devel >= %{kfver}
BuildRequires:	kf6-kconfigwidgets-devel >= %{kfver}
BuildRequires:	kf6-kcoreaddons-devel >= %{kfver}
BuildRequires:	kf6-kdbusaddons-devel >= %{kfver}
BuildRequires:	kf6-kdeclarative-devel >= %{kfver}
BuildRequires:	kf6-kglobalaccel-devel >= %{kfver}
BuildRequires:	kf6-kholidays-devel >= %{kfver}
BuildRequires:	kf6-ki18n-devel >= %{kfver}
BuildRequires:	kf6-kio-devel >= %{kfver}
BuildRequires:	kf6-kjobwidgets-devel >= %{kfver}
BuildRequires:	kf6-knewstuff-devel >= %{kfver}
BuildRequires:	kf6-knotifications-devel >= %{kfver}
BuildRequires:	kf6-kpackage-devel >= %{kfver}
BuildRequires:	kf6-krunner-devel >= %{kfver}
BuildRequires:	kf6-kservice-devel >= %{kfver}
BuildRequires:	kf6-kunitconversion-devel >= %{kfver}
BuildRequires:	kf6-kwidgetsaddons-devel >= %{kfver}
BuildRequires:	kf6-kxmlgui-devel >= %{kfver}
BuildRequires:	kf6-sonnet-devel >= %{kfver}
BuildRequires:	kp6-libplasma-devel >= %{kdeplasmaver}
BuildRequires:	kp6-plasma5support-devel >= %{kdeplasmaver}
BuildRequires:	libicu-devel >= 66.1
BuildRequires:	libstdc++-devel >= 6:8
BuildRequires:	ninja
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(post,postun):	gtk-update-icon-cache
Requires:	Qt6DBus >= %{qtver}
Requires:	Qt6Gui >= %{qtver}
Requires:	Qt6Network >= %{qtver}
Requires:	Qt6Qml >= %{qtver}
Requires:	Qt6Qt5Compat >= %{qtver}
Requires:	Qt6Quick >= %{qtver}
Requires:	Qt6Widgets >= %{qtver}
Requires:	hicolor-icon-theme
%requires_eq_to Qt6Core Qt6Core-devel
Suggests:	Qt6Quick3D
Suggests:	kf6-kirigami-addons
Suggests:	kf6-kitemmodels
Suggests:	kf6-purpose
Obsoletes:	kp5-%{kpname} < 6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6

%description
All kind of addons to improve your Plasma experience.

%package devel
Summary:	Header files for %{kpname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kpname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	kp5-%{kpname}-devel < %{version}

%description devel
Header files for %{kpname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kpname}.

%prep
%setup -q -n %{kpname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir}
%ninja_build -C build

%if %{with tests}
ctest
%endif

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kpname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%update_icon_cache hicolor

%postun
/sbin/ldconfig
%update_icon_cache hicolor

%files -f %{kpname}.lang
%defattr(644,root,root,755)
%{_datadir}/knsrcfiles/comic.knsrc
%ghost %{_libdir}/libplasmaweatherdata.so.6
%{_libdir}/libplasmaweatherdata.so.*.*
%ghost %{_libdir}/libplasmaweatherion.so.6
%{_libdir}/libplasmaweatherion.so.*.*
%dir %{_libdir}/qt6/qml/org/kde/plasma/private/colorpicker
%{_libdir}/qt6/qml/org/kde/plasma/private/colorpicker/libcolorpickerplugin.so
%{_libdir}/qt6/qml/org/kde/plasma/private/colorpicker/qmldir
%dir %{_libdir}/qt6/qml/org/kde/plasma/private/diskquota
%{_libdir}/qt6/qml/org/kde/plasma/private/diskquota/libdiskquotaplugin.so
%{_libdir}/qt6/qml/org/kde/plasma/private/diskquota/qmldir

%dir %{_libdir}/qt6/qml/org/kde/plasma/private/fifteenpuzzle
%{_libdir}/qt6/qml/org/kde/plasma/private/fifteenpuzzle/libfifteenpuzzleplugin.so
%{_libdir}/qt6/qml/org/kde/plasma/private/fifteenpuzzle/qmldir
%dir %{_libdir}/qt6/qml/org/kde/plasma/private/notes
%{_libdir}/qt6/qml/org/kde/plasma/private/notes/libnotesplugin.so
%{_libdir}/qt6/qml/org/kde/plasma/private/notes/qmldir
%{_iconsdir}/hicolor/scalable/apps/fifteenpuzzle.svgz
%dir %{_datadir}/kwin
%{_datadir}/kwin/tabbox
%dir %{_datadir}/plasma/desktoptheme/default
%dir %{_datadir}/plasma/desktoptheme/default/widgets
%{_datadir}/plasma/desktoptheme/default/widgets/timer.svgz
%{_datadir}/plasma/plasmoids/org.kde.plasma.calculator
%{_datadir}/plasma/plasmoids/org.kde.plasma.fifteenpuzzle
%{_datadir}/plasma/plasmoids/org.kde.plasma.fuzzyclock
%{_datadir}/plasma/plasmoids/org.kde.plasma.kickerdash
%{_datadir}/plasma/plasmoids/org.kde.plasma.konsoleprofiles
%{_datadir}/plasma/plasmoids/org.kde.plasma.notes
%{_datadir}/plasma/plasmoids/org.kde.plasma.diskquota
%{_datadir}/plasma/plasmoids/org.kde.plasma.userswitcher
%{_datadir}/plasma/wallpapers/org.kde.haenau
%{_datadir}/plasma/wallpapers/org.kde.hunyango

%{_libdir}/libplasmapotdprovidercore.so
%{_libdir}/qt6/plugins/plasma/applets/org.kde.plasma.grouping.so
%{_libdir}/qt6/plugins/plasma/applets/org.kde.plasma.binaryclock.so
%{_libdir}/qt6/plugins/plasma/applets/org.kde.plasma.keyboardindicator.so
%{_libdir}/qt6/plugins/plasma/applets/org.kde.plasma.quicklaunch.so
%{_libdir}/qt6/plugins/plasma/applets/org.kde.plasma.timer.so
%{_libdir}/qt6/plugins/plasma/applets/org.kde.plasma.weather.so
%dir %{_libdir}/qt6/plugins/plasma/weather_ions
%{_libdir}/qt6/plugins/plasma/weather_ions/bbcukmet.so
%{_libdir}/qt6/plugins/plasma/weather_ions/dwd.so
%{_libdir}/qt6/plugins/plasma/weather_ions/envcan.so
%{_libdir}/qt6/plugins/plasma/weather_ions/noaa.so
%{_libdir}/qt6/plugins/plasma/weather_ions/wettercom.so
%dir %{_libdir}/qt6/plugins/potd
%{_libdir}/qt6/plugins/potd/plasma_potd_apodprovider.so
%{_libdir}/qt6/plugins/potd/plasma_potd_bingprovider.so
%{_libdir}/qt6/plugins/potd/plasma_potd_epodprovider.so
%{_libdir}/qt6/plugins/potd/plasma_potd_flickrprovider.so
%{_libdir}/qt6/plugins/potd/plasma_potd_wcpotdprovider.so
%dir %{_libdir}/qt6/qml/org/kde/plasma/private/mediaframe
%{_libdir}/qt6/qml/org/kde/plasma/private/mediaframe/libmediaframeplugin.so
%{_libdir}/qt6/qml/org/kde/plasma/private/mediaframe/qmldir
%{_datadir}/metainfo/org.kde.haenau.appdata.xml
%{_datadir}/metainfo/org.kde.hunyango.appdata.xml
%{_datadir}/metainfo/org.kde.plasma.calculator.appdata.xml
%{_datadir}/metainfo/org.kde.plasma.colorpicker.appdata.xml
%{_datadir}/metainfo/org.kde.plasma.diskquota.appdata.xml
%{_datadir}/metainfo/org.kde.plasma.fifteenpuzzle.appdata.xml
%{_datadir}/metainfo/org.kde.plasma.fuzzyclock.appdata.xml
%{_datadir}/metainfo/org.kde.plasma.grouping.appdata.xml
%{_datadir}/metainfo/org.kde.plasma.kickerdash.appdata.xml
%{_datadir}/metainfo/org.kde.plasma.konsoleprofiles.appdata.xml
%{_datadir}/metainfo/org.kde.plasma.mediaframe.appdata.xml
%{_datadir}/metainfo/org.kde.plasma.notes.appdata.xml
%{_datadir}/metainfo/org.kde.plasma.userswitcher.appdata.xml
%{_datadir}/metainfo/org.kde.potd.appdata.xml
%dir %{_datadir}/plasma/desktoptheme/default/weather
%{_datadir}/plasma/desktoptheme/default/weather/wind-arrows.svgz
%{_datadir}/plasma/plasmoids/org.kde.plasma.grouping
%{_datadir}/plasma/plasmoids/org.kde.plasma.mediaframe
%{_datadir}/plasma/wallpapers/org.kde.potd
%{_libdir}/qt6/plugins/plasmacalendarplugins/astronomicalevents.so
%dir %{_libdir}/qt6/plugins/plasmacalendarplugins/astronomicalevents
%{_libdir}/qt6/plugins/plasmacalendarplugins/astronomicalevents/AstronomicalEventsConfig.qml
%dir %{_libdir}/qt6/qml/org/kde/plasmacalendar
%dir %{_libdir}/qt6/qml/org/kde/plasmacalendar/astronomicaleventsconfig
%{_libdir}/qt6/qml/org/kde/plasmacalendar/astronomicaleventsconfig/libplasmacalendarastronomicaleventsconfig.so
%{_libdir}/qt6/qml/org/kde/plasmacalendar/astronomicaleventsconfig/qmldir
%{_datadir}/plasma/plasmoids/org.kde.plasma.colorpicker
%dir %{_libdir}/qt6/plugins/kf6/krunner
%{_libdir}/qt6/plugins/kf6/krunner/krunner_charrunner.so
%{_libdir}/qt6/plugins/kf6/krunner/krunner_dictionary.so
%{_libdir}/qt6/plugins/kf6/krunner/krunner_katesessions.so
%{_libdir}/qt6/plugins/kf6/krunner/krunner_konsoleprofiles.so
%{_libdir}/qt6/plugins/kf6/krunner/krunner_spellcheck.so
%{_libdir}/qt6/plugins/kf6/krunner/org.kde.datetime.so

%{_libdir}/qt6/plugins/kf6/krunner/unitconverter.so

%{_libdir}/qt6/plugins/kf6/krunner/kcms/kcm_krunner_charrunner.so
%{_libdir}/qt6/plugins/kf6/krunner/kcms/kcm_krunner_dictionary.so
%{_libdir}/qt6/plugins/kf6/krunner/kcms/kcm_krunner_spellcheck.so
%{_libdir}/qt6/plugins/potd/plasma_potd_simonstalenhagprovider.so

%dir %{_libdir}/qt6/qml/org/kde/plasma/wallpapers/potd
%{_libdir}/qt6/qml/org/kde/plasma/wallpapers/potd/libplasma_wallpaper_potdplugin.so
%attr(755,root,root) %{_libdir}/qt6/qml/org/kde/plasma/wallpapers/potd/qmldir

%{_libdir}/qt6/plugins/plasmacalendarplugins/alternatecalendar.so
%dir %{_libdir}/qt6/plugins/plasmacalendarplugins/alternatecalendar
%{_libdir}/qt6/plugins/plasmacalendarplugins/alternatecalendar/AlternateCalendarConfig.qml
%{_libdir}/qt6/qml/org/kde/plasma/private/profiles/libprofiles_qml_plugin.so
%dir %{_libdir}/qt6/qml/org/kde/plasma/private/profiles
%{_libdir}/qt6/qml/org/kde/plasma/private/profiles/qmldir
%{_datadir}/kdevappwizard/templates/plasmapotdprovider.tar.bz2
%{_datadir}/metainfo/org.kde.plasma.addons.katesessions.appdata.xml
%dir %{_datadir}/plasma/plasmoids/org.kde.plasma.addons.katesessions
%dir %{_datadir}/plasma/plasmoids/org.kde.plasma.addons.katesessions/contents
%dir %{_datadir}/plasma/plasmoids/org.kde.plasma.addons.katesessions/contents/ui
%{_datadir}/plasma/plasmoids/org.kde.plasma.addons.katesessions/contents/ui/KateSessionsItemDelegate.qml
%{_datadir}/plasma/plasmoids/org.kde.plasma.addons.katesessions/contents/ui/Menu.qml
%{_datadir}/plasma/plasmoids/org.kde.plasma.addons.katesessions/contents/ui/main.qml
%{_datadir}/plasma/plasmoids/org.kde.plasma.addons.katesessions/metadata.json

%ghost %{_libdir}/libplasmapotdprovidercore.so.2
%{_libdir}/libplasmapotdprovidercore.so.*.*
%{_libdir}/qt6/plugins/kf6/packagestructure/plasma_comic.so
%{_libdir}/qt6/plugins/kwin/effects/configs/kwin_cube_config.so
%{_libdir}/qt6/plugins/plasma/applets/org.kde.plasma.comic.so
%{_libdir}/qt6/qml/org/kde/plasma/private/colorpicker/colorpickerplugin.qmltypes
%{_libdir}/qt6/qml/org/kde/plasma/private/colorpicker/kde-qmlmodule.version
%{_libdir}/qt6/qml/org/kde/plasma/private/diskquota/diskquotaplugin.qmltypes
%{_libdir}/qt6/qml/org/kde/plasma/private/diskquota/kde-qmlmodule.version
%{_libdir}/qt6/qml/org/kde/plasma/private/fifteenpuzzle/fifteenpuzzleplugin.qmltypes
%{_libdir}/qt6/qml/org/kde/plasma/private/fifteenpuzzle/kde-qmlmodule.version
%{_libdir}/qt6/qml/org/kde/plasma/private/mediaframe/kde-qmlmodule.version
%{_libdir}/qt6/qml/org/kde/plasma/private/mediaframe/mediaframeplugin.qmltypes
%{_libdir}/qt6/qml/org/kde/plasma/private/notes/kde-qmlmodule.version
%{_libdir}/qt6/qml/org/kde/plasma/private/notes/notesplugin.qmltypes
%{_libdir}/qt6/qml/org/kde/plasma/private/profiles/kde-qmlmodule.version
%{_libdir}/qt6/qml/org/kde/plasma/private/profiles/profiles_qml_plugin.qmltypes
%{_libdir}/qt6/qml/org/kde/plasma/wallpapers/potd/kde-qmlmodule.version
%{_libdir}/qt6/qml/org/kde/plasma/wallpapers/potd/plasma_wallpaper_potdplugin.qmltypes
%{_libdir}/qt6/qml/org/kde/plasmacalendar/astronomicaleventsconfig/kde-qmlmodule.version
%{_libdir}/qt6/qml/org/kde/plasmacalendar/astronomicaleventsconfig/plasmacalendarastronomicaleventsconfig.qmltypes
%{_datadir}/knotifications6/plasma_applet_timer.notifyrc
%dir %{_datadir}/kwin/effects/cube
%dir %{_datadir}/kwin/effects/cube/contents
%dir %{_datadir}/kwin/effects/cube/contents/config
%{_datadir}/kwin/effects/cube/contents/config/main.xml
%dir %{_datadir}/kwin/effects/cube/contents/ui
%{_datadir}/kwin/effects/cube/contents/ui/Cube.qml
%{_datadir}/kwin/effects/cube/contents/ui/CubeCameraController.qml
%{_datadir}/kwin/effects/cube/contents/ui/CubeFace.qml
%{_datadir}/kwin/effects/cube/contents/ui/DesktopView.qml
%{_datadir}/kwin/effects/cube/contents/ui/ScreenView.qml
%{_datadir}/kwin/effects/cube/contents/ui/constants.js
%{_datadir}/kwin/effects/cube/contents/ui/main.qml
%{_datadir}/kwin/effects/cube/metadata.json
%{_datadir}/qlogging-categories6/kdeplasma-addons.categories
%{_datadir}/polkit-1/actions/org.kde.kameleonhelper.policy

%{_libdir}/qt6/plugins/kf6/kded/kameleon.so
%dir %{_libdir}/qt6/qml/org/kde/plasma/private/alternatecalendarconfig
%{_libdir}/qt6/qml/org/kde/plasma/private/alternatecalendarconfig/kde-qmlmodule.version
%{_libdir}/qt6/qml/org/kde/plasma/private/alternatecalendarconfig/libplasmacalendaralternatecalendarconfig.so
%{_libdir}/qt6/qml/org/kde/plasma/private/alternatecalendarconfig/plasmacalendaralternatecalendarconfig.qmltypes
%{_libdir}/qt6/qml/org/kde/plasma/private/alternatecalendarconfig/qmldir
%attr(755,root,root) %{_prefix}/libexec/kf6/kauth/kameleonhelper
%{_datadir}/dbus-1/system-services/org.kde.kameleonhelper.service
%{_datadir}/dbus-1/system.d/org.kde.kameleonhelper.conf
%{_datadir}/kwin/effects/cube/contents/ui/PlaceholderView.qml
%{_libdir}/qt6/plugins/kf6/krunner/krunner_colors.so
%{_datadir}/qlogging-categories6/kdeplasma-addons.renamecategories
%{_datadir}/plasma/weather

%if %{with qtwebengine}
%{_datadir}/plasma/plasmoids/org.kde.plasma.webbrowser
%dir %{_libdir}/qt6/qml/org/kde/plasma/private/dict
%{_libdir}/qt6/qml/org/kde/plasma/private/dict/libdictplugin.so
%{_libdir}/qt6/qml/org/kde/plasma/private/dict/dictplugin.qmltypes
%{_libdir}/qt6/qml/org/kde/plasma/private/dict/kde-qmlmodule.version
%{_libdir}/qt6/qml/org/kde/plasma/private/dict/qmldir
%{_iconsdir}/hicolor/scalable/apps/accessories-dictionary.svg*
%{_datadir}/metainfo/org.kde.plasma.webbrowser.appdata.xml
%{_datadir}/metainfo/org.kde.plasma_applet_dict.appdata.xml
%{_datadir}/plasma/plasmoids/org.kde.plasma_applet_dict
%endif

%files devel
%defattr(644,root,root,755)
%{_includedir}/plasma/potdprovider
%{_libdir}/cmake/PlasmaPotdProvider
%{_libdir}/libplasmaweatherdata.so
%{_libdir}/libplasmaweatherion.so
