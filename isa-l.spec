# doesn't seem to work on sles 12.3: #{!?make_build:#define make_build #{__make} #{?_smp_mflags}}
# so...
%if 0%{?suse_version} <= 1320
%define make_build  %{__make} %{?_smp_mflags}
%endif
%if 0%{?suse_version} >= 1315
%define isal_libname libisal2
%define isal_devname libisal-devel
%else
%define isal_libname libisa-l
%define isal_devname libisa-l-devel
%endif

%global _hardened_build 1

Name:			isa-l
Version:	2.30.0
Release:	2%{?dist}

Summary:	Intelligent Storage Acceleration Library

%if 0%{?suse_version} >= 1315
Group:		Development/Libraries/C and C++
%else
Group:		Development/Libraries
%endif
License:	BSD-3-Clause
URL:			https://github.com/01org/isa-l/wiki
Source0:	https://github.com/01org/%{name}/archive/v%{version}.tar.gz

BuildRequires: yasm

# to be able to generate configure if not present
BuildRequires: autoconf, automake, libtool

%description
This package contains the libisal.so dynamic library which contains
a collection of optimized low-level functions targeting storage
applications.

%package -n %{isal_libname}
Summary: Dynamic library for isa-l functions
License: BSD-3-Clause
Obsoletes: %{name} < %{version}

%description -n %{isal_libname}
This package contains the libisal.so dynamic library which contains
a collection of optimized low-level functions targeting storage
applications. ISA-L includes:
- Erasure codes - Fast block Reed-Solomon type erasure codes for any
encode/decode matrix in GF(2^8).
- CRC - Fast implementations of cyclic redundancy check. Six different
polynomials supported.
    - iscsi32, ieee32, t10dif, ecma64, iso64, jones64.
- Raid - calculate and operate on XOR and P+Q parity found in common
RAID implementations.
- Compression - Fast deflate-compatible data compression.
- De-compression - Fast inflate-compatible data compression.

%package -n %{isal_devname}
Summary:	ISA-L devel package
Requires:	%{isal_libname}%{?_isa} = %{version}
Provides:	%{isal_libname}-static%{?_isa} = %{version}

%description -n %{isal_devname}
Development files for the %{isal_libname} library.

%if (0%{?suse_version} > 0)
%global __debug_package 1
%global _debuginfo_subpackages 0
%debug_package
%endif

%prep
%autosetup -p1

%build
%if (0%{?suse_version} > 0)
export CFLAGS="%{optflags} -fPIC -pie"
export CXXFLAGS="%{optflags} -fPIC -pie"
# this results in compiler errors, so we are unable to produce PIEs on Leap15
#export LDFLAGS="$LDFLAGS -pie"
%else
export CFLAGS="${CFLAGS:-%optflags}"
export CXXFLAGS="${CXXFLAGS:-%optflags}"
export FFLAGS="${FFLAGS:-%optflags}"
%if "%{?build_ldflags}" != ""
export LDFLAGS="${LDFLAGS:-%{build_ldflags}}"
%endif
%endif

if [ ! -f configure ]; then
    ./autogen.sh --no-oshmem
fi
%configure --disable-static

%{make_build}

%install
%make_install
find %{?buildroot} -name *.la -print0 | xargs -r0 rm -f

%if 0%{?suse_version} >= 01315
%post -n %{isal_libname} -p /sbin/ldconfig
%postun -n %{isal_libname} -p /sbin/ldconfig
%else
%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%endif

%files
%license LICENSE
%{_bindir}/*
%{_mandir}/man1/*

%doc

%files -n %{isal_libname}
%license LICENSE
%{_libdir}/*.so.*

%files -n %{isal_devname}
%license LICENSE
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/libisal.pc

%changelog
* Fri May 19 2023 Brian J. Murrell <brian.murrell@intel> - 2.30.0-2
- Disable static library build
- Add debuginfo generation for Leap 15
- Add hardened build flags for CentOS 7 and Leap 15

* Thu Jan 28 2021 Brian J. Murrell <brian.murrell@intel> - 2.30.0-1
- Update to latest
- Add %%{_libdir}/pkgconfig/libisal.pc to -devel package

* Tue Jun 16 2020 Brian J. Murrell <brian.murrell@intel> - 2.26.0-3
- Add %%license files

* Wed Oct 02 2019 John E. Malmberg <john.e.malmberg@intel> - 2.26.0-2
- Fix some SUSE rpmlint packaging complaints

* Wed May 15 2019 Brian J. Murrell <brian.murrell@intel> - 2.26.0-1
- Update to latest
- Split into a man utilities package with igizp and a library
  package
  - Obsoletes: the older isa-l packages accordingly

* Tue May 07 2019 Brian J. Murrell <brian.murrell@intel> - 2.21.0-3
- Bump release for RPM cache coherency

* Fri May 03 2019 Brian J. Murrell <brian.murrell@intel> - 2.21.0-2
- Use the more stable "archive" URL for the source
- Define a make_build macro for SLES 12.3

* Fri Apr 05 2019 Brian J. Murrell <brian.murrell@intel> - 2.21.0-1
- initial package
