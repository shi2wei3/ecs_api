Name:           ecs_api
Version:        0.1
Release:        0%{?dist}
Summary:        ECS API
Group:          Development/Languages

License:        GPLv2+
URL:            https://github.com/shi2wei3/ecs_api
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python-setuptools
Requires:       python-requests

%description
ECS API

%prep
%setup -q -n %{name}-%{version}

%build
%{__python} setup.py build

%install
# install app
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%files
%{python_sitelib}/*
%{_bindir}/*

%changelog
* Fri Feb 24 2017 Wei Shi <wshi@redhat.com> - 0.1-0
- Create app
