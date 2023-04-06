#
# Conditional build:
%bcond_without	doc	# Documentation

%define		orgname		qtcharts
%define		qtbase_ver		%{version}
%define		qtdeclarative_ver	%{version}
%define		qttools_ver		%{version}
Summary:	The Qt5 Charts library
Summary(pl.UTF-8):	Biblioteka Qt5 Charts
Name:		qt5-%{orgname}
Version:	5.15.9
Release:	1
License:	GPL v3 or commercial
Group:		Libraries
Source0:	https://download.qt.io/official_releases/qt/5.15/%{version}/submodules/%{orgname}-everywhere-opensource-src-%{version}.tar.xz
# Source0-md5:	bb5e5dfa9c4d8743ef3cd9a07652cfc1
URL:		https://www.qt.io/
BuildRequires:	Qt5Core-devel >= %{qtbase_ver}
BuildRequires:	Qt5Gui-devel >= %{qtbase_ver}
BuildRequires:	Qt5Qml-devel >= %{qtdeclarative_ver}
BuildRequires:	Qt5Quick-devel >= %{qtdeclarative_ver}
BuildRequires:	Qt5Widgets-devel >= %{qtbase_ver}
%if %{with doc}
BuildRequires:	qt5-assistant >= %{qttools_ver}
%endif
BuildRequires:	qt5-build >= %{qtbase_ver}
BuildRequires:	qt5-qmake >= %{qtbase_ver}
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.016
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fno-strict-aliasing
%define		qt5dir		%{_libdir}/qt5

%description
Qt is a cross-platform application and UI framework. Using Qt, you can
write web-enabled applications once and deploy them across desktop,
mobile and embedded systems without rewriting the source code.

This package contains Qt5 Charts library.

%description -l pl.UTF-8
Qt to wieloplatformowy szkielet aplikacji i interfejsów użytkownika.
Przy użyciu Qt można pisać aplikacje powiązane z WWW i wdrażać je w
systemach biurkowych, przenośnych i wbudowanych bez przepisywania kodu
źródłowego.

Ten pakiet zawiera bibliotekę Qt5 Charts.

%package -n Qt5Charts
Summary:	The Qt5 Charts library
Summary(pl.UTF-8):	Biblioteka Qt5 Charts
Group:		Libraries
Requires:	Qt5Core >= %{qtbase_ver}
Requires:	Qt5Gui >= %{qtbase_ver}
Requires:	Qt5Widgets >= %{qtbase_ver}
# for qml module
Requires:	Qt5Qml >= %{qtdeclarative_ver}
Requires:	Qt5Quick >= %{qtdeclarative_ver}

%description -n Qt5Charts
Qt Charts module provides a set of easy to use chart components. It
uses the Qt Graphics View Framework, therefore charts can be easily
integrated to modern user interfaces.

%description -n Qt5Charts -l pl.UTF-8
Biblioteka Qt5 Charts udostępnia łatwe w użyciu komponenty do
tworzenia wykresów. Wykorzystuje szkielet Qt Graphics View, dzięki
czemu wykresy mogą być łatwo integrowane z nowoczesnymi interfejsami
użytkownika.

%package -n Qt5Charts-devel
Summary:	Qt5 Charts library - development files
Summary(pl.UTF-8):	Biblioteka Qt5 Charts - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt5Charts = %{version}-%{release}
Requires:	Qt5Core-devel >= %{qtbase_ver}
Requires:	Qt5Gui-devel >= %{qtbase_ver}
Requires:	Qt5Widgets-devel >= %{qtbase_ver}

%description -n Qt5Charts-devel
Qt5 Charts library - development files.

%description -n Qt5Charts-devel -l pl.UTF-8
Biblioteka Qt5 Charts - pliki programistyczne.

%package doc
Summary:	Qt5 Charts documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt5 Charts w formacie HTML
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
BuildArch:	noarch

%description doc
Qt5 Charts documentation in HTML format.

%description doc -l pl.UTF-8
Dokumentacja do biblioteki Qt5 Charts w formacie HTML.

%package doc-qch
Summary:	Qt5 Charts documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt5 Charts w formacie QCH
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
BuildArch:	noarch

%description doc-qch
Qt5 Charts documentation in QCH format.

%description doc-qch -l pl.UTF-8
Dokumentacja do biblioteki Qt5 Charts w formacie QCH.

%package examples
Summary:	Qt5 Charts examples
Summary(pl.UTF-8):	Przykłady do biblioteki Qt5 Charts
Group:		Development/Libraries
BuildArch:	noarch

%description examples
Qt5 Charts examples.

%description examples -l pl.UTF-8
Przykłady do biblioteki Qt5 Charts.

%prep
%setup -q -n %{orgname}-everywhere-src-%{version}

%build
%{qmake_qt5}
%{__make}
%{?with_doc:%{__make} docs}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

%if %{with doc}
%{__make} install_docs \
	INSTALL_ROOT=$RPM_BUILD_ROOT
%endif

# useless symlinks
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt5*.so.5.??
# actually drop *.la, follow policy of not packaging them when *.pc exist
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt5*.la

# Prepare some files list
ifecho() {
	r="$RPM_BUILD_ROOT$2"
	if [ -d "$r" ]; then
		echo "%%dir $2" >> $1.files
	elif [ -x "$r" ] ; then
		echo "%%attr(755,root,root) $2" >> $1.files
	elif [ -f "$r" ]; then
		echo "$2" >> $1.files
	else
		echo "Error generation $1 files list!"
		echo "$r: no such file or directory!"
		return 1
	fi
}
ifecho_tree() {
	ifecho $1 $2
	for f in `find $RPM_BUILD_ROOT$2 -printf "%%P "`; do
		ifecho $1 $2/$f
	done
}

echo "%defattr(644,root,root,755)" > examples.files
ifecho_tree examples %{_examplesdir}/qt5/charts

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n Qt5Charts -p /sbin/ldconfig
%postun	-n Qt5Charts -p /sbin/ldconfig

%files -n Qt5Charts
%defattr(644,root,root,755)
%doc LICENSE.GPL3 dist/changes-*
# R: Core Gui Widgets
%attr(755,root,root) %{_libdir}/libQt5Charts.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5Charts.so.5
%dir %{qt5dir}/qml/QtCharts
%{qt5dir}/qml/QtCharts/designer
# R: Core Gui Qml Quick Widgets
%attr(755,root,root) %{qt5dir}/qml/QtCharts/libqtchartsqml2.so
%{qt5dir}/qml/QtCharts/plugins.qmltypes
%{qt5dir}/qml/QtCharts/qmldir

%files -n Qt5Charts-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5Charts.so
%{_libdir}/libQt5Charts.prl
%{_includedir}/qt5/QtCharts
%{_pkgconfigdir}/Qt5Charts.pc
%{_libdir}/cmake/Qt5Charts
%{qt5dir}/mkspecs/modules/qt_lib_charts.pri
%{qt5dir}/mkspecs/modules/qt_lib_charts_private.pri

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtcharts

%files doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtcharts.qch
%endif

%files examples -f examples.files
%defattr(644,root,root,755)
# XXX: dir shared with qt5-qtbase-examples
%dir %{_examplesdir}/qt5
