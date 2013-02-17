#
# Conditional build:
%bcond_with	fma4	# use FMA4-only libraries (run only on AMD Bulldozer CPUs) instead of runtime detection
#
Summary:	AMD Core Math Library
Summary(pl.UTF-8):	AMD Core Math Library - biblioteka matematyczna AMD
Name:		acml
%ifarch	%{x8664}
Version:	5.3.0
%else
Version:	4.4.0
%endif
Release:	1
License:	AMD EULA
Group:		Libraries
# from http://developer.amd.com/tools/cpu-development/amd-core-math-library-acml/acml-downloads-resources/
Source0:	%{name}-5-3-0-gfortran-64bit1.tgz
# NoSource0-md5:	42707776bcfbfc7100ea30fa7b905750
# from http://developer.amd.com/tools/cpu-development/amd-core-math-library-acml/acml-archive-downloads/
Source1:	%{name}-4-4-0-gfortran-32bit.tgz
# NoSource1-md5:	1ad4e23f27849728acf305da97e337a4
NoSource:	0
NoSource:	1
URL:		http://developer.amd.com/tools/cpu-development/amd-core-math-library-acml/
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ACML - the AMD Core Math Library - is a tuned math library designed
for high performance on AMD64 machines, including Opteron(TM) and
Athlon(TM) 64, and includes both 32-bit and 64-bit library versions.
Different versions are available for Linux, Windows and Solaris
operating systems.

%description -l pl.UTF-8
ACML (AMD Core Math Library) to biblioteka matematyczna
zoptymalizowana pod kątem wydajności na maszynach AMD64, w tym
procesorach Opteron(TM) i Athlon(TM) 64. Dostępne są 32- i 64-bitowe
wersje biblioteki dla systemów Linux, Windows i Solaris.

%package devel
Summary:	Header file for ACML libraries
Summary(pl.UTF-8):	Plik nagłówkowy bibliotek ACML
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header file for ACML libraries.

%description devel -l pl.UTF-8
Plik nagłówkowy bibliotek ACML.

%package static
Summary:	Static ACML libraries
Summary(pl.UTF-8):	Statyczne biblioteki ACML
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static ACML libraries.

%description static -l pl.UTF-8
Statyczne biblioteki ACML.

%prep
%ifarch %{x8664}
%setup -q -c
tar xzf contents-acml-5-3-0-gfortran-64bit.tgz
%else
%setup -q -c -T -a1
tar xzf contents-acml-4-4-0-gfortran-32bit.tgz
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_includedir},%{_libdir}}

%ifarch %{x8664}
# all acml.h files are identical
cp -p gfortran64/include/acml.h $RPM_BUILD_ROOT%{_includedir}
install gfortran64%{?with_fma4:_fma4}/lib/lib* $RPM_BUILD_ROOT%{_libdir}
install gfortran64%{?with_fma4:_fma4}_mp/lib/lib* $RPM_BUILD_ROOT%{_libdir}
%else
# both acml.h files are identical
cp -p gfortran32/include/acml.h $RPM_BUILD_ROOT%{_includedir}
install gfortran32/lib/lib* $RPM_BUILD_ROOT%{_libdir}
install gfortran32_mp/lib/lib* $RPM_BUILD_ROOT%{_libdir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%ifarch %{x8664}
%doc ACML-EULA.txt README.64-bit ReleaseNotes
%else
%doc ACML-EULA.txt README.32-bit ReleaseNotes
%endif
%attr(755,root,root) %{_libdir}/libacml.so
%attr(755,root,root) %{_libdir}/libacml_mp.so

%files devel
%defattr(644,root,root,755)
%doc Doc/acml.pdf
%{_includedir}/acml.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libacml.a
%{_libdir}/libacml_mp.a
