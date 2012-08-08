# To build:
# 
# sudo yum -y install rpmdevtools && rpmdev-setuptree
# 
# wget https://raw.github.com/nmilford/specfiles/master/kafka-0.7/kafka-0.7.spec -O ~/rpmbuild/SPECS/kafka-0.7.spec
# wget http://mirror.symnds.com/software/Apache/incubator/kafka/kafka-0.7.1-incubating/kafka-0.7.1-incubating-src.tgz -O ~/rpmbuild/SOURCES/kafka-0.7.1-incubating-src.tgz 
# wget https://raw.github.com/nmilford/specfiles/master/kafka-0.7/kafka -O ~/rpmbuild/SOURCES/kafka
# wget https://raw.github.com/nmilford/specfiles/master/kafka-0.7/kafka-server -O ~/rpmbuild/SOURCES/kafka-server
# wget https://raw.github.com/nmilford/specfiles/master/kafka-0.7/kafka.nofiles.conf -O ~/rpmbuild/SOURCES/kafka.nofiles.conf
# 
# rpmbuild -bb ~/rpmbuild/SPECS/storm-0.8.spec

%define kafka_name kafka
%define kafka_branch 0.7
%define kafka_version 0.7.1
%define release_version 1 
%define kafka_home /opt/%{kafka_name}-%{kafka_version}
%define etc_kafka /etc/%{name}
%define config_kafka %{etc_kafka}/conf
%define kafka_user kafka
%define kafka_group kafka

Name: %{kafka_name}
Version: %{kafka_version}
Release: %{release_version}
Summary: Apache Kafka is a high-throughput distributed publish-subscribe messaging system.
License: Apache 2.0 
URL: http://incubator.apache.org/kafka/
Group: Development/Libraries
Source0: %{kafka_name}-%{kafka_version}-incubating-src.tgz
Source1: kafka-server
Source2: kafka
Source3: kafka.nofiles.conf
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-%(%{__id_u} -n)
Requires: jdk, sh-utils, textutils, /usr/sbin/useradd, /usr/sbin/usermod, /sbin/chkconfig, /sbin/service
Provides: kafka
Packager: Nathan Milford <nathan@milford.io>
BuildArch: noarch

%description
Kafka provides a publish-subscribe solution that can handle all activity stream
data and processing on a consumer-scale web site. This kind of activity (page
views, searches, and other user actions) are a key ingredient in many of the
social feature on the modern web. Kafka aims to unify offline and online 
processing by providing a mechanism for parallel load into Hadoop as well as
the ability to partition real-time consumption over a cluster of machines.

%prep
%setup -n %{kafka_name}-%{kafka_version}-incubating

%build
./sbt update
./sbt package

%clean
rm -rf %{buildroot}

%install
install -d -m 755 %{buildroot}/%{kafka_home}/
install    -m 644 %{_builddir}/%{kafka_name}-%{kafka_version}-incubating/CHANGES.txt      %{buildroot}/%{kafka_home}/
install    -m 644 %{_builddir}/%{kafka_name}-%{kafka_version}-incubating/DISCLAIMER       %{buildroot}/%{kafka_home}/
install    -m 644 %{_builddir}/%{kafka_name}-%{kafka_version}-incubating/LICENSE          %{buildroot}/%{kafka_home}/
install    -m 644 %{_builddir}/%{kafka_name}-%{kafka_version}-incubating/NOTICE           %{buildroot}/%{kafka_home}/
install    -m 644 %{_builddir}/%{kafka_name}-%{kafka_version}-incubating/README.md        %{buildroot}/%{kafka_home}/

install -d -m 755 %{buildroot}/%{kafka_home}/bin/
install    -m 644 %{_builddir}/%{kafka_name}-%{kafka_version}-incubating/bin/*.properties %{buildroot}/%{kafka_home}/bin
install    -m 755 %{_builddir}/%{kafka_name}-%{kafka_version}-incubating/bin/*.sh         %{buildroot}/%{kafka_home}/bin

install -d -m 755 %{buildroot}/%{kafka_home}/config/
install    -m 644 %{_builddir}/%{kafka_name}-%{kafka_version}-incubating/config/*         %{buildroot}/%{kafka_home}/config

install -d -m 755 %{buildroot}/%{kafka_home}/core/
install -d -m 755 %{buildroot}/%{kafka_home}/core/lib/
#install    -m 644 %{_builddir}/%{kafka_name}-%{kafka_version}-incubating/core/lib/*       %{buildroot}/%{kafka_home}/core/lib

install -d -m 755 %{buildroot}/%{kafka_home}/core/lib_managed/
install -d -m 755 %{buildroot}/%{kafka_home}/core/lib_managed/scala_2.8.0/compile/
install -d -m 755 %{buildroot}/%{kafka_home}/core/lib_managed/scala_2.8.0/test/
install    -m 644 %{_builddir}/%{kafka_name}-%{kafka_version}-incubating/core/lib_managed/scala_2.8.0/compile/*  %{buildroot}/%{kafka_home}/core/lib_managed/scala_2.8.0/compile/
install    -m 644 %{_builddir}/%{kafka_name}-%{kafka_version}-incubating/core/lib_managed/scala_2.8.0/test/*     %{buildroot}/%{kafka_home}/core/lib_managed/scala_2.8.0/test/

install -d -m 755 %{buildroot}/%{kafka_home}/core/target/
install -d -m 755 %{buildroot}/%{kafka_home}/core/target/scala_2.8.0/
install    -m 644 %{_builddir}/%{kafka_name}-%{kafka_version}-incubating/core/target/scala_2.8.0/kafka-0.7.1.jar %{buildroot}/%{kafka_home}/core/target/scala_2.8.0/

install -d -m 755 %{buildroot}/%{kafka_home}/project/
install    -m 644 %{_builddir}/%{kafka_name}-%{kafka_version}-incubating/project/build.properties  %{buildroot}/%{kafka_home}/project/build.properties

install -d -m 755 %{buildroot}/%{kafka_home}/project/boot/
install -d -m 755 %{buildroot}/%{kafka_home}/project/boot/scala-2.8.0/
install -d -m 755 %{buildroot}/%{kafka_home}/project/boot/scala-2.8.0/lib/
install    -m 644 %{_builddir}/%{kafka_name}-%{kafka_version}-incubating/project/boot/scala-2.8.0/lib/* %{buildroot}/%{kafka_home}/project/boot/scala-2.8.0/lib/

cd %{buildroot}/opt/
ln -s %{kafka_name}-%{kafka_version} %{kafka_name}
cd -

install -d -m 755 %{buildroot}/etc/
cd %{buildroot}/etc
ln -s %{kafka_home}/config %{kafka_name}
cd -

install -d -m 755 %{buildroot}/%{_initrddir}
install    -m 755 %_sourcedir/kafka-server     %{buildroot}/%{_initrddir}/kafka-server

install -d -m 755 %{buildroot}/%{_sysconfdir}/sysconfig/
install    -m 644 %_sourcedir/kafka            %{buildroot}/%{_sysconfdir}/sysconfig/kafka

install -d -m 755 %{buildroot}/%{_sysconfdir}/security/limits.d/
install    -m 644 %_sourcedir/kafka.nofiles.conf %{buildroot}/%{_sysconfdir}/security/limits.d/kafka.nofiles.conf

install -d -m 755 %{buildroot}/var/log/kafka

%pre
getent group %{kafka_group} >/dev/null || groupadd -r %{kafka_group}
getent passwd %{kafka_user} >/dev/null || /usr/sbin/useradd --comment "Kafka Daemon User" --shell /bin/bash -M -r -g %{kafka_group} --home %{kafka_home} %{kafka_user}

%files
%defattr(-,%{kafka_user},%{kafka_group})

/opt/%{kafka_name}
%{kafka_home}
%{kafka_home}/*
%{kafka_home}/bin/*.properties
%attr(755,%{kafka_user},%{kafka_group}) %{kafka_home}/bin/*.sh
/etc/kafka/
%attr(755,%{kafka_user},%{kafka_group}) /var/log/kafka/
/etc/sysconfig/kafka
/etc/security/limits.d/kafka.nofiles.conf
%{_initrddir}/%{kafka_name}-server

%post
chkconfig --add %{kafka_name}-server
%preun 
service %{kafka_name}-server stop > /dev/null 2>&1
chkconfig --del %{kafka_name}-server
%postun
service %{kafka_name}-server restart >/dev/null 2>&1

%changelog
* Wed Aug 08 2012 Nathan Milford <nathan@milford.io> [0.7.1-1]
- Bumped to Kafka 0.7.1.
* Sun Jun 03 2012 Nathan Milford <nathan@milford.io> [0.7.0-1]
- First shot with Kafka 0.7.0.
