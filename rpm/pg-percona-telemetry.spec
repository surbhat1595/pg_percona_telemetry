%global sname percona-pg-telemetry
%global pgrel @@PG_REL@@
%global rpm_release @@RPM_RELEASE@@
%global pginstdir /usr/pgsql-@@PG_REL@@/

Summary:        Statistics collector for PostgreSQL
Name:           %{sname}%{pgrel}
Version:        @@VERSION@@
Release:        %{rpm_release}%{?dist}
License:        PostgreSQL
Source0:        percona-pg-telemetry%{pgrel}-%{version}.tar.gz
URL:            https://github.com/Percona-Lab/percona_pg_telemetry
BuildRequires:  percona-postgresql%{pgrel}-devel
Requires:       percona-telemetry-agent
Provides:       percona-pg-telemetry%{pgrel}
Conflicts:      percona-pg-telemetry%{pgrel}
Obsoletes:      percona-pg-telemetry%{pgrel}
Epoch:          1
Packager:       Percona Development Team <https://jira.percona.com>
Vendor:         Percona, Inc

%description
The percona_pg_telemetry is an extension for Percona telemetry data collection for PostgreSQL.

%prep
%setup -q -n percona-pg-telemetry%{pgrel}-%{version}


%build
sed -i 's:PG_CONFIG = pg_config:PG_CONFIG = /usr/pgsql-%{pgrel}/bin/pg_config:' Makefile
%{__make} USE_PGXS=1 %{?_smp_mflags}


%install
%{__rm} -rf %{buildroot}
%{__make} USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}
%{__install} -d %{buildroot}%{pginstdir}/share/extension
%{__install} -m 755 README.md %{buildroot}%{pginstdir}/share/extension/README-percona_pg_telemetry


%clean
%{__rm} -rf %{buildroot}


%post -p /sbin/ldconfig
mkdir -p /usr/local/percona/telemetry/pg
chown postgres:percona-telemetry /usr/local/percona/telemetry/pg
chmod 775 /usr/local/percona/telemetry/pg
chmod g+s /usr/local/percona/telemetry/pg
chmod u+s /usr/local/percona/telemetry/pg
chgrp percona-telemetry /usr/local/percona/telemetry_uuid
chmod 664 /usr/local/percona/telemetry_uuid

%postun -p /sbin/ldconfig
rm -rf /usr/local/percona/telemetry/pg

%files
%defattr(755,root,root,755)
%doc %{pginstdir}/share/extension/README-percona_pg_telemetry
%{pginstdir}/lib/percona_pg_telemetry.so
%{pginstdir}/share/extension/percona_pg_telemetry--*.sql
%{pginstdir}/share/extension/percona_pg_telemetry.control
%{pginstdir}/lib/bitcode/percona_pg_telemetry*.bc
%{pginstdir}/lib/bitcode/percona_pg_telemetry/*.bc


%changelog
* Fri Apr 26 2024 Surabhi Bhat <surabhi.bhat@percona.com> - 1.0.0-1
- Initial build
