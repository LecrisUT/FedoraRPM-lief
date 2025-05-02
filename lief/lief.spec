# Python API needs some
%bcond python 0

Name:           lief
Version:        0.16.5
Release:        %autorelease
Summary:        Library to Instrument Executable Formats

# TODO: License check
License:        Apache-2.0

%global         forgeurl0 https://github.com/lief-project/LIEF
%global         tag0      c93ee79b2a134b63593152dd4148b8a7cb94980b
%forgemeta

URL:            https://lief.re
Source:         %{forgesource0}

Provides:       bundled(span)

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  json-devel
BuildRequires:  spdlog-devel
BuildRequires:  expected-devel
BuildRequires:  utf8cpp-devel
BuildRequires:  mbedtls-devel
BuildRequires:  frozen-devel
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


%generate_buildrequires
%if %{with python}
pushd api/python
%pyproject_buildrequires
popd
%endif


%conf
%cmake \
  -DLIEF_TESTS:BOOL=ON \
  -DLIEF_C_API:BOOL=ON \
  -DLIEF_PYTHON_API:BOOL=OFF \
  -DLIEF_RUST_API:BOOL=OFF \
  -DLIEF_LOGGING_DEBUG:BOOL=OFF \
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
%ctest


%files
%license LICENSE

%files devel
%config %{_sysconfdir}/profile.d/atuin.sh

%if %{with python}
%files -n python3-lief -f %{pyproject_files}
%endif


%changelog
%autochangelog
