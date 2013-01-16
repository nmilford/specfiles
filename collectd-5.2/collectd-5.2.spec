# To Build:
#
# sudo yum -y install rpmdevtools && rpmdev-setuptree
#
# wget https://raw.github.com/nmilford/specfiles/master/collectd-5.2/collectd-5.2.spec -O ~/rpmbuild/SPECS/collectd-5.2.spec
# wget http://collectd.org/files/collectd-5.2.0.tar.gz -O ~/rpmbuild/SOURCES/collectd-5.2.0.tar.gz
#
# QA_RPATHS=[0-7] rpmbuild -bb ~/rpmbuild/SPECS/collectd-5.2.spec

%define python_path /usr/bin/python26

AutoReqProv: no
Summary:	Statistics collection daemon for filling RRD files.
Name:		  collectd
Version:	5.2.0
Release:	1%{?dist}
Source:		http://collectd.org/files/%{name}-%{version}.tar.gz
License:	GPL
Group:		System Environment/Daemons
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
BuildPrereq:	curl-devel, libesmtp-devel, libmemcached-devel, net-snmp-devel, OpenIPMI-devel, libpcap-devel, librabbitmq-devel lm_sensors-devel, libevent-devel, libgcrypt-devel, openssl-devel, jdk
Vendor:		collectd development team <collectd@verplant.org>

%description
collectd is a small daemon which collects system information periodically and
provides mechanisms to monitor and store the values in a variety of ways. It
is written in C for performance. Since the daemon doesn't need to startup
every time it wants to update the values it's very fast and easy on the
system. Also, the statistics are very fine grained since the files are updated
every 10 seconds.

%prep
rm -rf $RPM_BUILD_ROOT
%setup

%build
./configure CFLAGS=-"DLT_LAZY_OR_NOW='RTLD_LAZY|RTLD_GLOBAL'" --prefix=%{_prefix} --sbindir=%{_sbindir} --mandir=%{_mandir} --libdir=%{_libdir} --sysconfdir=%{_sysconfdir} --enable-java --with-python=%{python_path} --disable-battery  --disable-rpath
make

%install
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc/collectd/collectd.d
mkdir -p $RPM_BUILD_ROOT/var/lib/collectd
mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d

install -d -m 755 %{buildroot}/%{_initrddir}
install    -m 755 %_sourcedir/collectd     %{buildroot}/%{_initrddir}/collectd

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add collectd
/sbin/chkconfig collectd on

%preun
if [ "$1" = 0 ]; then
   /sbin/chkconfig collectd off
   /etc/init.d/collectd stop
   /sbin/chkconfig --del collectd
fi
exit 0

%postun
if [ "$1" -ge 1 ]; then
    /etc/init.d/collectd restart
fi
exit 0

%files

%attr(0644,root,root) %{_libdir}/%{name}/*.a 
%attr(0644,root,root) %{_libdir}/%{name}/*.so* 
%attr(0644,root,root) %{_libdir}/%{name}/*.la
%attr(0644,root,root) %{_libdir}/libcollectdclient.*
%attr(0644,root,root) /usr/include/collectd/client.h
%attr(0644,root,root) /usr/include/collectd/lcc_features.h
%attr(0644,root,root) %{_libdir}/libcollectdclient.*
%attr(0644,root,root) %{_libdir}/pkgconfig/libcollectdclient.pc
%attr(0644,root,root) %{_mandir}/man1/*
%attr(0644,root,root) %{_mandir}/man5/*
%attr(0755,root,root) %{_sbindir}/collectd
%attr(0755,root,root) %{_sbindir}/collectdmon
%attr(0755,root,root) %{_bindir}/collectd-nagios
%attr(0755,root,root) %{_bindir}/collectdctl
%attr(0755,root,root) %{_bindir}/collectd-tg
%attr(0644,root,root) %{_datadir}/%{name}/types.db
%config %attr(0644,root,root) /etc/collectd.conf
%attr(0755,root,root) /etc/rc.d/init.d/collectd
%attr(0644,root,root) /usr/include/collectd/*.h
%exclude %{_libdir}/perl5/5.8.8/%{_arch}-linux-thread-multi/perllocal.pod
%attr(0644,root,root) %{_libdir}/perl5/site_perl/5.8.8/%{_arch}-linux-thread-multi/auto/Collectd/.packlist
%attr(0644,root,root) /usr/lib/perl5/site_perl/5.8.8/Collectd.pm
%attr(0644,root,root) /usr/lib/perl5/site_perl/5.8.8/Collectd/Unixsock.pm
%attr(0644,root,root) /usr/lib/perl5/site_perl/5.8.8/Collectd/Plugins/OpenVZ.pm
%attr(0644,root,root) /usr/share/man/man3/Collectd::Unixsock.3pm.gz
%exclude /usr/share/collectd/postgresql_default.conf

%dir /var/lib/collectd
%attr(0644,root,root) /usr/share/collectd/java/collectd-api.jar
%attr(0644,root,root) /usr/share/collectd/java/generic-jmx.jar

%dir /etc/collectd/collectd.d

%changelog
* Wed Jan 16 2013 Nathan Milford <nathan@milford.io> 5.2.0
- Moved to 5.2.0
* Tue Jan 03 2011 Monetate <jason.stelzer@monetate.com> 5.0.1
- New upstream version
- Changes to support 5.0.1

