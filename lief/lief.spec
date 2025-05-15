# Python API needs some
%bcond python 0

Name:           lief
Version:        0.16.5
Release:        %autorelease
Summary:        Library to Instrument Executable Formats

# Fails to build on s390x
# https://github.com/lief-project/LIEF/issues/1210
ExcludeArch:    s390x

# Main project is Apache-2.0
# Some bundled CMake files come from Kitware
# - cmake/ios.toolchain.cmake
# Bundled span is BSL-1.0
SourceLicense:  Apache-2.0 AND BSL-1.0 AND BSD-3-Clause
License:        Apache-2.0 AND BSL-1.0

%global         forgeurl0 https://github.com/lief-project/LIEF
# Picking up a few changes that fix packaging issues
%global         tag0      dc66460141c7b14a8ac36e9d9478d73badbbc621
%forgemeta

URL:            https://lief.re
Source:         %{forgesource0}

# Should be using c++20 span, but it causes lots of issues
Provides:       bundled(span)

BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  json-devel
BuildRequires:  spdlog-devel
BuildRequires:  expected-devel
BuildRequires:  utf8cpp-devel
BuildRequires:  mbedtls-devel
BuildRequires:  frozen-devel
BuildRequires:  catch-devel
%if %{with python}
BuildRequires:  python3-devel
%endif

%global _description %{expand:
The purpose of this project is to provide a cross-platform library to parse,
modify and abstract ELF, PE and MachO formats.}

%description %{_description}

%package devel
Summary:        Development files for lief
Requires:       lief = %{version}-%{release}

%description devel %{_description}

This package contains the development files.

%if %{with python}
%package -n python3-lief
Summary:        Python API for lief
Requires:       lief = %{version}-%{release}

%description -n python3-lief %{_description}

This package contains python API.
%endif


%prep
%forgeautosetup -p1
mv third-party/tcb-span-* ./
rm -rf third-party/*
mv tcb-span-* third-party/


%generate_buildrequires
%if %{with python}
pushd api/python
%pyproject_buildrequires
popd
%endif


%conf
%cmake \
  -G Ninja \
  -DCMAKE_BUILD_TYPE:STRING=RelWithDebInfo \
  -DFETCHCONTENT_TRY_FIND_PACKAGE_MODE:STRING=ALWAYS \
  -DLIEF_TESTS:BOOL=OFF \
  -DLIEF_EXAMPLES:BOOL=OFF \
  -DLIEF_C_API:BOOL=ON \
  -DLIEF_PYTHON_API:BOOL=OFF \
  -DLIEF_RUST_API:BOOL=OFF \
  -DLIEF_SO_VERSION:BOOL=ON \
  -DLIEF_LOGGING_DEBUG:BOOL=OFF \
  -DLIEF_USE_MELKOR:BOOL=OFF \
  -DLIEF_OPT_NLOHMANN_JSON_EXTERNAL:BOOL=ON \
  -DLIEF_EXTERNAL_SPDLOG:BOOL=ON \
  -DLIEF_OPT_EXTERNAL_EXPECTED:BOOl=ON \
  -DLIEF_OPT_UTFCPP_EXTERNAL:BOOL=ON \
  -DLIEF_OPT_MBEDTLS_EXTERNAL:BOOL=ON \
  -DLIEF_OPT_FROZEN_EXTERNAL:BOOL=ON


%build
%cmake_build

%if %{with python}
build_dir=$(pwd)/%_vpath_builddir
pushd api/python
%{pyproject_wheel %{shrink:
  -C cmake.build-type=RelWithDebInfo
  -C cmake.define.LIEF_ROOT=${build_dir}
  -C cmake.define.LIEF_PY_LIEF_EXT=true
  -C cmake.define.LIEF_PY_LIEF_EXT_SHARED=true
}}
popd
%endif


%install
%cmake_install
%if %{with python}
pushd api/python
%pyproject_install
%pyproject_save_files -l lief
popd
%endif


%check
# %%ctest


%files
%license LICENSE
%{_libdir}/libLIEF.so.*

%files devel
%{_includedir}/LIEF
%{_libdir}/pkgconfig/LIEF.pc
%{_libdir}/cmake/LIEF
%{_libdir}/libLIEF.so

%if %{with python}
%files -n python3-lief -f %{pyproject_files}
%endif


%changelog
%autochangelog
