%define		realname	SDL_image
Summary:	Simple DirectMedia Layer - Sample Image Loading Library - Mingw32 cross version
Summary(pl.UTF-8):	Przykładowa biblioteka do ładowania obrazków - wersja skrośna dla Mingw32
Name:		crossmingw32-%{realname}
Version:	1.2.6
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://www.libsdl.org/projects/SDL_image/release/%{realname}-%{version}.tar.gz
# Source0-md5:	b866dc4f647517bdaf57f6ffdefd013e
URL:		http://www.libsdl.org/projects/SDL_image/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	crossmingw32-SDL >= 1.2.10
BuildRequires:	crossmingw32-gcc
BuildRequires:	crossmingw32-libjpeg >= 6b
BuildRequires:	crossmingw32-libpng >= 1.2.0
BuildRequires:	crossmingw32-w32api
BuildRequires:	crossmingw32-zlib
BuildRequires:	libtool
Requires:	crossmingw32-SDL >= 1.2.10
Requires:	crossmingw32-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target			i386-mingw32
%define		target_platform		i386-pc-mingw32

%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}
%define		_libdir			%{_prefix}/lib
%define		_dlldir			/usr/share/wine/windows/system
%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++

%ifarch alpha sparc sparc64 sparcv9
# alpha's -mieee and sparc's -mtune=* are not valid for target's gcc
%define		optflags	-O2
%endif

%description
This is a simple library to load images of various formats as SDL
surfaces. This library currently supports BMP, PPM, PCX, GIF, JPEG,
and PNG formats.

This package contains the cross version for Win32.

%description -l pl.UTF-8
Jest to prosta biblioteka służąca do ładowania różnego formatu
obrazków jako powierzchni SDL. W chwili obecnej biblioteka obsługuje
następujące formaty: BMP, PPM, PCX, GIF, JPEG oraz PNG.

Ten pakiet zawiera wersję skrośną dla Win32.

%package static
Summary:	Static SDL_image library (cross mingw32 version)
Summary(pl.UTF-8):	Statyczna biblioteka SDL_image (wersja skrośna mingw32)
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description static
Static SDL_image library (cross mingw32 version).

%description static -l pl.UTF-8
Statyczna biblioteka SDL_image (wersja skrośna mingw32).

%package dll
Summary:	SDL_image - DLL library for Windows
Summary(pl.UTF-8):	SDL_image - biblioteka DLL dla Windows
Group:		Applications/Emulators
Requires:	crossmingw32-SDL-dll >= 1.2.10
Requires:	wine

%description dll
SDL_image - DLL library for Windows.

%description dll -l pl.UTF-8
SDL_image - biblioteka DLL dla Windows.

%prep
%setup -q -n %{realname}-%{version}

rm -f acinclude.m4

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
# no sdl test, because it requires configured wine to work
%configure \
	png_lib=libpng12-0.dll \
	--host=%{target} \
	--target=%{target} \
	--with-sdl-prefix=%{_prefix} \
	--disable-sdltest \
	--enable-bmp \
	--enable-gif \
	--enable-jpg \
	--enable-pcx \
	--enable-png \
	--enable-tga

# LIBS hack for libtool not detecting libraries without .la files
%{__make} \
	LIBS="$(%{_bindir}/sdl-config --libs | sed -e 's/\(-lmingw32\|-lSDLmain\)/-Wl,\1/g')"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_dlldir}
mv -f $RPM_BUILD_ROOT%{_prefix}/bin/*.dll $RPM_BUILD_ROOT%{_dlldir}

%if 0%{!?debug:1}
%{target}-strip --strip-unneeded -R.comment -R.note $RPM_BUILD_ROOT%{_dlldir}/*.dll
%{target}-strip -g -R.comment -R.note $RPM_BUILD_ROOT%{_libdir}/*.a
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES README
%{_libdir}/libSDL_image.dll.a
%{_libdir}/libSDL_image.la
%{_includedir}/SDL/SDL_image.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libSDL_image.a

%files dll
%defattr(644,root,root,755)
%{_dlldir}/libSDL_image-*.dll
