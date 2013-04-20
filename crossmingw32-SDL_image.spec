%define		realname	SDL_image
Summary:	Simple DirectMedia Layer - Sample Image Loading Library - MinGW32 cross version
Summary(pl.UTF-8):	Przykładowa biblioteka do ładowania obrazków - wersja skrośna dla MinGW32
Name:		crossmingw32-%{realname}
Version:	1.2.12
Release:	2
License:	Zlib-like
Group:		Libraries
Source0:	http://www.libsdl.org/projects/SDL_image/release/%{realname}-%{version}.tar.gz
# Source0-md5:	a0f9098ebe5400f0bdc9b62e60797ecb
URL:		http://www.libsdl.org/projects/SDL_image/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	crossmingw32-SDL >= 1.2.10
BuildRequires:	crossmingw32-gcc
BuildRequires:	crossmingw32-libjpeg >= 7
BuildRequires:	crossmingw32-libpng >= 1.5.0
BuildRequires:	crossmingw32-libtiff >= 4
BuildRequires:	crossmingw32-libwebp >= 0.1.3
BuildRequires:	crossmingw32-w32api
BuildRequires:	libtool >= 2:2.0
BuildRequires:	pkgconfig >= 1:0.9.0
Requires:	crossmingw32-SDL >= 1.2.10
Requires:	crossmingw32-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target			i386-mingw32
%define		target_platform		i386-pc-mingw32

%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}
%define		_libdir			%{_prefix}/lib
%define		_pkgconfigdir		%{_prefix}/lib/pkgconfig
%define		_dlldir			/usr/share/wine/windows/system
%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++
%define		__pkgconfig_provides	%{nil}

%ifnarch %{ix86}
# arch-specific flags (like alpha's -mieee) are not valid for i386 gcc
%define		optflags	-O2
%endif
# -z options are invalid for mingw linker
%define		filterout_ld	-Wl,-z,.*

%description
This is a simple library to load images of various formats as SDL
surfaces. This library currently supports BMP, GIF, JPEG, LBM, PCX,
PNG, PNM (PBM/PGM/PPM), TGA, TIFF, WebP, XCF and XPM formats.

This package contains the cross version for Win32.

%description -l pl.UTF-8
Jest to prosta biblioteka służąca do ładowania różnego formatu
obrazków jako powierzchni SDL. W chwili obecnej biblioteka obsługuje
następujące formaty: BMP, GIF, JPEG, LBM, PCX, PNG, PNM (PBM/PGM/PPM),
TGA, TIFF, WebP, XCF oraz XPM.

Ten pakiet zawiera wersję skrośną dla Win32.

%package static
Summary:	Static SDL_image library (cross MinGW32 version)
Summary(pl.UTF-8):	Statyczna biblioteka SDL_image (wersja skrośna MinGW32)
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description static
Static SDL_image library (cross MinGW32 version).

%description static -l pl.UTF-8
Statyczna biblioteka SDL_image (wersja skrośna MinGW32).

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

%build
export PKG_CONFIG_LIBDIR=%{_prefix}/lib/pkgconfig
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
# no sdl test, because it requires configured wine to work
%configure \
	--host=%{target} \
	--target=%{target} \
	--with-sdl-prefix=%{_prefix} \
	--disable-sdltest

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
%{_pkgconfigdir}/SDL_image.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libSDL_image.a

%files dll
%defattr(644,root,root,755)
%{_dlldir}/libSDL_image-*.dll
