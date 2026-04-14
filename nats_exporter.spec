%global debug_package %{nil}
%global user prometheus
%global group prometheus

Name: nats_exporter
Version: 0.19.2
Release: 1%{?dist}
Summary: A prometheus exporter for NATS
License: ASL 2.0
URL:     https://github.com/nats-io/prometheus-nats-exporter

Source0: https://github.com/nats-io/prometheus-nats-exporter/releases/download/v%{version}/prometheus-nats-exporter-v%{version}-linux-x86_64.tar.gz
Source1: %{name}.unit
Source2: %{name}.default

%{?systemd_requires}
Requires(pre): shadow-utils

%description
A prometheus exporter for NATS

%prep
%setup -q -D -c prometheus-nats-exporter-v%{version}-linux-x86_64
mv -v prometheus-nats-exporter %{name}

%build
/bin/true

%install
mkdir -vp %{buildroot}%{_sharedstatedir}/prometheus
install -D -m 755 %{name} %{buildroot}%{_bindir}/%{name}
install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/default/%{name}
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
useradd -r -g prometheus -d %{_sharedstatedir}/prometheus -s /sbin/nologin -c "Prometheus services" prometheus
exit 0

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%config(noreplace) %{_sysconfdir}/default/%{name}
%dir %attr(755, %{user}, %{group}) %{_sharedstatedir}/prometheus
%{_unitdir}/%{name}.service

%changelog
* Tue Mar 31 2026 Ivan Garcia <igarcia@cloudox.org> - 0.19.2
- Initial packaging for the 0.19.2 branch
