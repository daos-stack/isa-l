# doesn't seem to work on sles 12.3: %{!?make_build:%define make_build %{__make} %{?_smp_mflags}}
# so...
%if 0%{?suse_version} <= 1320
%define make_build  %{__make} %{?_smp_mflags}
%endif

Name:		isa-l
Version:	2.26.0
Release:	1%{?dist}

Summary:	Intelligent Storage Acceleration Library

Group:		Development/Libraries
License:	BSD-3-Clause
URL:		https://github.com/01org/isa-l/wiki
Source0:        https://github.com/01org/%{name}/archive/v%{version}.tar.gz

BuildRequires: yasm

# to be able to generate configure if not present
BuildRequires: autoconf, automake, libtool

%description
The igzip utility.

%package -n libisa-l
Summary: Dynamic library for isa-l functions
License: BSD-3-Clause

%description -n libisa-l
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

%package -n libisa-l-devel
Summary:	ISA-L devel package
Requires:	lib%{name}%{?_isa} = %{version}
Provides:	lib%{name}-static%{?_isa} = %{version}

%description -n libisa-l-devel
ISA-L devel

%prep
%autosetup -p1

%build
if [ ! -f configure ]; then
    ./autogen.sh --no-oshmem
fi
%configure

%{make_build}

%install
%make_install
find %{?buildroot} -name *.la -print0 | xargs -r0 rm -f

%files
%{_bindir}/*
%{_mandir}/man1/*

%doc

%files -n libisa-l
%{_libdir}/*.so.*

%files -n libisa-l-devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a

%changelog
* Wed May 15 2019 Brian J. Murrell <brian.murrell@intel> - 2.26.0-1
- Update to latest
- Split into a man utilities package with igizp and a library
  package

* Tue May 07 2019 Brian J. Murrell <brian.murrell@intel> - 2.21.0-3
- Bump release for RPM cache coherency

* Fri May 03 2019 Brian J. Murrell <brian.murrell@intel> - 2.21.0-2
- Use the more stable "archive" URL for the source
- Define a make_build macro for SLES 12.3

* Fri Apr 05 2019 Brian J. Murrell <brian.murrell@intel> - 2.21.0-1
- initial package
