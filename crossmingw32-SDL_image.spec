%define		realname	SDL_image
Summary:	Simple DirectMedia Layer - Sample Image Loading Library - Mingw32 cross version
Summary(pl):	Przyk³adowa biblioteka do ³adowania obrazków - wersja skro¶na dla Mingw32
Name:		crossmingw32-%{realname}
Version:	1.2.3
Release:	1
License:	LGPL
Group:		Libraries
Source0:	http://www.libsdl.org/projects/SDL_image/release/%{realname}-%{version}.tar.gz
# Source0-md5:	d55826ffbd2bdc48b09cc64a9ed9e59e
Patch0:		%{realname}-ac_fixes.patch
URL:		http://www.libsdl.org/projects/SDL_image/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	crossmingw32-gcc
BuildRequires:	crossmingw32-libjpeg
BuildRequires:	crossmingw32-libpng
BuildRequires:	crossmingw32-SDL
BuildRequires:	crossmingw32-w32api
BuildRequires:	crossmingw32-zlib
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target		i386-mingw32
%define		target_platform	i386-pc-mingw32
%define		arch		%{_prefix}/%{target}
%define		gccarch		%{_prefix}/lib/gcc-lib/%{target}
%define		gcclib		%{_prefix}/lib/gcc-lib/%{target}/%{version}

%define		__cc		%{target}-gcc
%define		__cxx		%{target}-g++

%description
This is a simple library to load images of various formats as SDL
surfaces. This library currently supports BMP, PPM, PCX, GIF, JPEG,
and PNG formats.

%description -l pl
jest to prosta biblioteka s³u¿±ca do ³adowania ró¿nego formatu
obrazków jako powierzchni SDL. W chwili obecnej biblioteka obs³uguje
nastepuj±ce formaty: BMP, PPM, PCX, GIF, JPEG oraz PNG.

%package dll
Summary:	%{realname} - DLL library for Windows
Summary(pl):	%{realname} - biblioteka DLL dla Windows
Group:		Applications/Emulators

%description dll
%{realname} - DLL library for Windows.

%description dll -l pl
%{realname} - biblioteka DLL dla Windows.

%prep
%setup -q -n %{realname}-%{version}
%patch0 -p1

%build
CC=%{target}-gcc ; export CC
CXX=%{target}-g++ ; export CXX
LD=%{target}-ld ; export LD
AR=%{target}-ar ; export AR
AS=%{target}-as ; export AS
CROSS_COMPILE=1 ; export CROSS_COMPILE
CPPFLAGS="-I%{arch}/include" ; export CPPFLAGS
RANLIB=%{target}-ranlib ; export RANLIB
LDSHARED="%{target}-gcc -shared" ; export LDSHARED
TARGET="%{target}" ; export TARGET

rm -f acinclude.m4
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
# no sdl test, because it requires configured wine to work
%configure \
	--host=%{_host} \
	--target=%{target} \
	--with-sdl-prefix=%{arch} \
	--disable-sdltest \
	--enable-bmp \
	--enable-gif \
	--enable-jpg \
	--enable-pcx \
	--enable-png \
	--enable-tga \
	--disable-shared

%{__make}

%{__cc} --shared IMG*.o -Wl,--enable-auto-image-base -o SDL_image.dll -Wl,--out-implib,libSDL_image.dll.a -lSDL -lpng -ljpeg

cp -f .libs/libSDL_image.a .

%if 0%{!?debug:1}
%{target}-strip -R.comment -R.note *.dll
%{target}-strip -g -R.comment -R.note *.a
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{arch}/{include/SDL,lib}
install -d $RPM_BUILD_ROOT%{_datadir}/wine/windows/system

install *.a $RPM_BUILD_ROOT%{arch}/lib
install SDL_image.h $RPM_BUILD_ROOT%{arch}/include/SDL
install *.dll $RPM_BUILD_ROOT%{_datadir}/wine/windows/system

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{arch}/include/SDL/*
%{arch}/lib/*

%files dll
%defattr(644,root,root,755)
%{_datadir}/wine/windows/system
