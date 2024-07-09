Name:      rockit-focuser-aaf5
Version:   %{_version}
Release:   1
Summary:   ASA AAF5 Focuser Controller
Url:       https://github.com/rockit-astro/focusd-aaf5
License:   GPL-3.0
BuildArch: noarch

%description


%build
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}/etc/bash_completion.d
mkdir -p %{buildroot}%{_sysconfdir}/focusd/
mkdir -p %{buildroot}%{_udevrulesdir}

%{__install} %{_sourcedir}/focus %{buildroot}%{_bindir}
%{__install} %{_sourcedir}/aaf5_focusd %{buildroot}%{_bindir}
%{__install} %{_sourcedir}/aaf5_focusd@.service %{buildroot}%{_unitdir}
%{__install} %{_sourcedir}/completion/focus %{buildroot}/etc/bash_completion.d
%{__install} %{_sourcedir}/10-h400-focuser.rules %{buildroot}%{_udevrulesdir}
%{__install} %{_sourcedir}/h400.json %{buildroot}%{_sysconfdir}/focusd/

%package server
Summary:  Focuser control server.
Group:    Unspecified
Requires: python3-rockit-focuser-aaf5 python3-pyserial
%description server

%files server
%defattr(0755,root,root,-)
%{_bindir}/aaf5_focusd
%defattr(0644,root,root,-)
%{_unitdir}/aaf5_focusd@.service

%package client
Summary:  Focuser control client.
Group:    Unspecified
Requires: python3-rockit-focuser-aaf5
%description client

%files client
%defattr(0755,root,root,-)
%{_bindir}/focus
/etc/bash_completion.d/focus

%package data-h400
Summary: Focuser data for the H400 test telescope
Group:   Unspecified
%description data-h400

%files data-h400
%defattr(0644,root,root,-)
%{_sysconfdir}/focusd/h400.json
%{_udevrulesdir}/10-h400-focuser.rules

%changelog