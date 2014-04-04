%define name app-name
%define desc Desc for app-name

Name:    %{name}
Summary: %{desc}
Version: %(date +%Y%m%d%H%M)
Release: 1%{?dist}
License: None
Source:  https://github.com/nottings/flask_wsgi_nginx_app_skeleton.git

BuildRequires: rpm-build, make, python, python-pip, python-virtualenv, git, gcc, systemd
Requires:      python, nginx >= 1.4, systemd, systemd-units

%description
%{desc}

%prep
rm -rf %{buildroot}
mkdir %{buildroot}

%build
make -f %{srcdir}/Makefile venv DEST=%{_builddir}

%install
cp -r %{_builddir}/* %{buildroot}
mkdir -p %{buildroot}/usr/lib/systemd/system %{buildroot}/usr/bin %{buildroot}/etc/nginx/conf.d
cp %{srcdir}/support/*.service %{buildroot}/usr/lib/systemd/system/
cp %{srcdir}/support/nginx.conf %{buildroot}/etc/nginx/conf.d/%{name}.conf
ln -sf /opt/%{name}/bin/%{name} %{buildroot}/usr/bin/%{name}

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
    useradd -r -g %{name} -d /opt/%{name} -s /sbin/nologin \
    -c "User that runs the %{name} service" %{name}

%post
if [ $1 -eq 1 ] ; then  # Initial installation
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
    /bin/systemctl enable %{name}.service >/dev/null 2>&1 || :

    rm -f /etc/nginx/conf.d/default.conf
fi

%preun
if [ $1 -eq 0 ] ; then  # Package uninstall, not upgrade
    /bin/systemctl --no-reload disable %{name}.service > /dev/null 2>&1 || :
    /bin/systemctl stop %{name}.service > /dev/null 2>&1 || :
fi

%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then  # Package upgrade, not uninstall
    /bin/systemctl try-restart %{name}.service >/dev/null 2>&1 || :
fi

%files
%attr(-, %{name}, %{name}) /opt/%{name}/
%attr(-, root, root) /usr/lib/systemd/system/%{name}.service
%attr(-, root, root) /usr/bin/%{name}
%attr(-, root, root) /etc/nginx/conf.d/%{name}.conf
