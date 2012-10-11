# To build:
# 
# sudo yum -y install rpmdevtools && rpmdev-setuptree
# 
# wget https://raw.github.com/nmilford/specfiles/master/activemq-5.7.0/activemq-5.7.spec -O ~/rpmbuild/SPECS/activemq-5.7.spec
# wget http://apache.claz.org/activemq/apache-activemq/5.7.0/apache-activemq-5.7.0-bin.zip  -O ~/rpmbuild/SOURCES/apache-activemq-5.7.0-bin.zip
# wget https://raw.github.com/nmilford/specfiles/master/activemq-5.7/activemq.init -O ~/rpmbuild/SOURCES/activemq.init
# 
# rpmbuild -bb ~/rpmbuild/SPECS/activemq-5.7.spec

%define __jar_repack %{nil}
%define amq_name activemq
%define amq_branch 5.7
%define amq_version 5.7.0
%define release_version 1
%define amq_home /opt/%{amq_name}-%{amq_version}
%define amq_etc /etc/%{amq_name}
%define amq_config %{etc_amq}/conf
%define amq_log /var/log/activemq
%define amq_pid /var/run/activemq
%define amq_data /var/lib/activemq/
%define amq_user activemq
%define amq_group activemq

Name: %{amq_name}
Version: %{amq_version}
Release: 1%{?dist}
Summary: Apache ActiveMQ
License: Apache
URL: http://activemq.apache.org/
Group: Network/Daemons
Source0: apache-activemq-%{version}-bin.zip
Source1: activemq.init
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: noarch
Packager: Nathan Milford <nathan@milford.io>

%description
ApacheMQ is a JMS Compliant Messaging System

%prep
%setup -q -n apache-activemq-%{version}

%build

# Change log file to /var/log/activemq/activemq.log
sed -i -e 's|log4j.appender.logfile.file=.*|log4j.appender.logfile.file=/var/log/activemq.log|' \
   %{_builddir}/apache-%{amq_name}-%{amq_version}/conf/log4j.properties

# Change the way su uses a user to start up activemq to prevent screen blackout.
sed -i -e '390s|      DOIT_PREFIX="su -c "|      DOIT_PREFIX="su $ACTIVEMQ_USER -c "|' \
   %{_builddir}/apache-%{amq_name}-%{amq_version}/bin/activemq

sed -i -e '391s|      DOIT_POSTFIX=" - $ACTIVEMQ_USER"|      DOIT_POSTFIX=""|' \
   %{_builddir}/apache-%{amq_name}-%{amq_version}/bin/activemq

# Make the control script source environment settings from /etc/activemq/activemq-env.sh
sed -i -e 's|ACTIVEMQ_CONFIGS=.*|source /etc/activemq/activemq-env.sh |' \
   %{_builddir}/apache-%{amq_name}-%{amq_version}/bin/activemq

# New home for environment settings.
cat <<EOF > %{_builddir}/apache-%{amq_name}-%{amq_version}/conf/activemq-env.sh
ACTIVEMQ_CONFIGS="/etc/activemq"
ACTIVEMQ_HOME="/opt/activemq"
ACTIVEMQ_BASE="/opt/activemq"
ACTIVEMQ_CONF="/etc/activemq"
ACTIVEMQ_USER="activemq"
ACTIVEMQ_DATA="/var/lib/activemq/data"
ACTIVEMQ_PIDFILE="/var/run/activemq/activemq.pid"
ACTIVEMQ_OPTS_MEMORY="-Xms1G -Xmx1G"
ACTIVEMQ_TMP="/var/lib/activemq/tmp/"
EOF

%clean
rm -rf %{buildroot}

%install
install -d -m 755 %{buildroot}/%{amq_home}
install    -m 644 %{_builddir}/apache-%{amq_name}-%{amq_version}/*.jar   %{buildroot}/%{amq_home}/
install    -m 644 %{_builddir}/apache-%{amq_name}-%{amq_version}/*.txt   %{buildroot}/%{amq_home}/
install    -m 644 %{_builddir}/apache-%{amq_name}-%{amq_version}/*.html  %{buildroot}/%{amq_home}/
install    -m 644 %{_builddir}/apache-%{amq_name}-%{amq_version}/LICENSE %{buildroot}/%{amq_home}/
install    -m 644 %{_builddir}/apache-%{amq_name}-%{amq_version}/NOTICE  %{buildroot}/%{amq_home}/

install -d -m 755 %{buildroot}/%{amq_home}/bin
install    -m 755 %{_builddir}/apache-%{amq_name}-%{amq_version}/bin/activemq       %{buildroot}/%{amq_home}/bin
install    -m 755 %{_builddir}/apache-%{amq_name}-%{amq_version}/bin/activemq-admin %{buildroot}/%{amq_home}/bin
install    -m 644 %{_builddir}/apache-%{amq_name}-%{amq_version}/bin/*.jar          %{buildroot}/%{amq_home}/bin

install -d -m 755 %{buildroot}/%{amq_home}/conf
install    -m 644 %{_builddir}/apache-%{amq_name}-%{amq_version}/conf/* %{buildroot}/%{amq_home}/conf

install -d -m 755 %{buildroot}/%{amq_log}
install    -m 644 %{_builddir}/apache-%{amq_name}-%{amq_version}/data/activemq.log %{buildroot}/%{amq_log}

install -d -m 755 %{buildroot}/%{amq_home}/lib
install    -m 644 %{_builddir}/apache-%{amq_name}-%{amq_version}/lib/*.jar %{buildroot}/%{amq_home}/lib
install    -m 644 %{_builddir}/apache-%{amq_name}-%{amq_version}/lib/*.txt %{buildroot}/%{amq_home}/lib

install -d -m 755 %{buildroot}/%{amq_home}/lib/optional
install    -m 644 %{_builddir}/apache-%{amq_name}-%{amq_version}/lib/optional/*.jar %{buildroot}/%{amq_home}/lib/optional

install -d -m 755 %{buildroot}/%{amq_home}/lib/camel
install    -m 644 %{_builddir}/apache-%{amq_name}-%{amq_version}/lib/camel/*.jar %{buildroot}/%{amq_home}/lib/camel

install -d -m 755 %{buildroot}/%{amq_home}/lib/extra
install    -m 644 %{_builddir}/apache-%{amq_name}-%{amq_version}/lib/extra/*.jar %{buildroot}/%{amq_home}/lib/extra

install -d -m 755 %{buildroot}/%{amq_home}/lib/web
install    -m 644 %{_builddir}/apache-%{amq_name}-%{amq_version}/lib/web/*.jar %{buildroot}/%{amq_home}/lib/web

install -d -m 755 %{buildroot}/%{amq_home}/webapps
install    -m 644 %{_builddir}/apache-%{amq_name}-%{amq_version}/webapps/favicon.ico %{buildroot}/%{amq_home}/webapps
install    -m 644 %{_builddir}/apache-%{amq_name}-%{amq_version}/webapps/index.html  %{buildroot}/%{amq_home}/webapps

install -d -m 755 %{buildroot}/%{amq_home}/webapps/admin
install    -m 644 %{_builddir}/apache-%{amq_name}-%{amq_version}/webapps/admin/*.html %{buildroot}/%{amq_home}/webapps/admin
install    -m 644 %{_builddir}/apache-%{amq_name}-%{amq_version}/webapps/admin/*.jsp %{buildroot}/%{amq_home}/webapps/admin


install -d -m 755 %{buildroot}/%{amq_home}/webapps/admin/decorators
install    -m 644 %{_builddir}/apache-%{amq_name}-%{amq_version}/webapps/admin/decorators/*.jsp %{buildroot}/%{amq_home}/webapps/admin/decorators

install -d -m 755 %{buildroot}/%{amq_home}/webapps/admin/images
install    -m 644 %{_builddir}/apache-%{amq_name}-%{amq_version}/webapps/admin/images/*.gif %{buildroot}/%{amq_home}/webapps/admin/images
install    -m 644 %{_builddir}/apache-%{amq_name}-%{amq_version}/webapps/admin/images/*.png %{buildroot}/%{amq_home}/webapps/admin/images

install -d -m 755 %{buildroot}/%{amq_home}/webapps/admin/js
install    -m 644 %{_builddir}/apache-%{amq_name}-%{amq_version}/webapps/admin/js/*.js %{buildroot}/%{amq_home}/webapps/admin/js

install -d -m 755 %{buildroot}/%{amq_home}/webapps/admin/js/mochi
install    -m 644 %{_builddir}/apache-%{amq_name}-%{amq_version}/webapps/admin/js/mochi/*.js %{buildroot}/%{amq_home}/webapps/admin/js/mochi

install -d -m 755 %{buildroot}/%{amq_home}/webapps/admin/js/plotkit
install    -m 644 %{_builddir}/apache-%{amq_name}-%{amq_version}/webapps/admin/js/plotkit/*.svg %{buildroot}/%{amq_home}/webapps/admin/js/plotkit
install    -m 644 %{_builddir}/apache-%{amq_name}-%{amq_version}/webapps/admin/js/plotkit/*.htc %{buildroot}/%{amq_home}/webapps/admin/js/plotkit
install    -m 644 %{_builddir}/apache-%{amq_name}-%{amq_version}/webapps/admin/js/plotkit/*.js %{buildroot}/%{amq_home}/webapps/admin/js/plotkit

install -d -m 755 %{buildroot}/%{amq_home}/webapps/admin/META-INF
install    -m 644 %{_builddir}/apache-%{amq_name}-%{amq_version}/webapps/admin/META-INF/LICENSE %{buildroot}/%{amq_home}/webapps/admin/META-INF
install    -m 644 %{_builddir}/apache-%{amq_name}-%{amq_version}/webapps/admin/META-INF/NOTICE %{buildroot}/%{amq_home}/webapps/admin/META-INF

install -d -m 755 %{buildroot}/%{amq_home}/webapps/admin/styles
install    -m 644 %{_builddir}/apache-%{amq_name}-%{amq_version}/webapps/admin/styles/*.css %{buildroot}/%{amq_home}/webapps/admin/styles

install -d -m 755 %{buildroot}/%{amq_home}/webapps/admin/test
install    -m 644 %{_builddir}/apache-%{amq_name}-%{amq_version}/webapps/admin/test/*.jsp %{buildroot}/%{amq_home}/webapps/admin/test

install -d -m 755 %{buildroot}/%{amq_home}/webapps/admin/WEB-INF
install    -m 644 %{_builddir}/apache-%{amq_name}-%{amq_version}/webapps/admin/WEB-INF/*.xml %{buildroot}/%{amq_home}/webapps/admin/WEB-INF

install -d -m 755 %{buildroot}/%{amq_home}/webapps/admin/WEB-INF/classes
install -d -m 755 %{buildroot}/%{amq_home}/webapps/admin/WEB-INF/classes/org
install -d -m 755 %{buildroot}/%{amq_home}/webapps/admin/WEB-INF/classes/org/apache
install -d -m 755 %{buildroot}/%{amq_home}/webapps/admin/WEB-INF/classes/org/apache/activemq
install -d -m 755 %{buildroot}/%{amq_home}/webapps/admin/WEB-INF/classes/org/apache/activemq/web
install    -m 644 %{_builddir}/apache-%{amq_name}-%{amq_version}/webapps/admin/WEB-INF/classes/org/apache/activemq/web/*.class %{buildroot}/%{amq_home}/webapps/admin/WEB-INF/classes/org/apache/activemq/web

install -d -m 755 %{buildroot}/%{amq_home}/webapps/admin/WEB-INF/classes/org/apache/activemq/web/controller
install    -m 644 %{_builddir}/apache-%{amq_name}-%{amq_version}/webapps/admin/WEB-INF/classes/org/apache/activemq/web/controller/*.class %{buildroot}/%{amq_home}/webapps/admin/WEB-INF/classes/org/apache/activemq/web/controller

install -d -m 755 %{buildroot}/%{amq_home}/webapps/admin/WEB-INF/classes/org/apache/activemq/web/filter
install    -m 644 %{_builddir}/apache-%{amq_name}-%{amq_version}/webapps/admin/WEB-INF/classes/org/apache/activemq/web/filter/*.class %{buildroot}/%{amq_home}/webapps/admin/WEB-INF/classes/org/apache/activemq/web/filter

install -d -m 755 %{buildroot}/%{amq_home}/webapps/admin/WEB-INF/classes/org/apache/activemq/web/handler
install    -m 644 %{_builddir}/apache-%{amq_name}-%{amq_version}/webapps/admin/WEB-INF/classes/org/apache/activemq/web/handler/*.class %{buildroot}/%{amq_home}/webapps/admin/WEB-INF/classes/org/apache/activemq/web/handler

install -d -m 755 %{buildroot}/%{amq_home}/webapps/admin/WEB-INF/jsp
install -d -m 755 %{buildroot}/%{amq_home}/webapps/admin/WEB-INF/jspf
install    -m 644 %{_builddir}/apache-%{amq_name}-%{amq_version}/webapps/admin/WEB-INF/jspf/*.jspf %{buildroot}/%{amq_home}/webapps/admin/WEB-INF/jspf

install -d -m 755 %{buildroot}/%{amq_home}/webapps/admin/WEB-INF/tags
install -d -m 755 %{buildroot}/%{amq_home}/webapps/admin/WEB-INF/tags/form
install    -m 644 %{_builddir}/apache-%{amq_name}-%{amq_version}/webapps/admin/WEB-INF/tags/form/*.tag %{buildroot}/%{amq_home}/webapps/admin/WEB-INF/tags/form

install -d -m 755 %{buildroot}/%{amq_home}/webapps/admin/WEB-INF/tags/jms
install    -m 644 %{_builddir}/apache-%{amq_name}-%{amq_version}/webapps/admin/WEB-INF/tags/jms/*.tag %{buildroot}/%{amq_home}/webapps/admin/WEB-INF/tags/jms

install -d -m 755 %{buildroot}/%{amq_home}/webapps/admin/xml
install    -m 644 %{_builddir}/apache-%{amq_name}-%{amq_version}/webapps/admin/xml/*.jsp %{buildroot}/%{amq_home}/webapps/admin/xml

install -d -m 755 %{buildroot}/%{amq_log}
install    -m 644 %{_builddir}/apache-%{amq_name}-%{amq_version}/data/activemq.log       %{buildroot}/%{amq_log}

cd %{buildroot}/opt
ln -s %{amq_name}-%{amq_version} %{amq_name}                                                                                                           
cd -

install -d -m 755 %{buildroot}/etc/
cd %{buildroot}/etc
ln -s %{amq_home}/conf %{amq_name}
cd -

install -d -m 755 %{buildroot}/%{amq_pid}
install -d -m 755 %{buildroot}/%{amq_data}
install -d -m 755 %{buildroot}/%{amq_data}/data

install -d -m 755 %{buildroot}/%{_initrddir}
install    -m 755 %_sourcedir/%{amq_name}.init %{buildroot}/%{_initrddir}/%{amq_name}

%pre
getent group %{amq_group} >/dev/null || groupadd -r %{amq_group}
getent passwd %{amq_user} >/dev/null || /usr/sbin/useradd --comment "ActiveMQ Daemon User" --shell /bin/bash -M -r -g %{amq_group} --home /opt/%{amq_name} %{amq_user}

# Clear old symlinks
if [ -h /etc/activemq ]; then
  rm -f /etc/activemq
fi

if [ -h /opt/activemq ]; then
  rm -f /opt/activemq
fi

%post
/sbin/chkconfig --add activemq

%preun
if [ $1 = 0 ]; then
  /usr/java/default/bin/jps|grep run.jar > /dev/null 2>&1
  [ $? = 0 ] && /etc/init.d/activemq stop
  [ -f /etc/init.d/activemq ] && /sbin/chkconfig --del activemq
fi

%files
%defattr(-,%{amq_user},%{amq_group})
%{amq_home}
%{amq_home}/*.jar
%doc %{amq_home}/LICENSE
%doc %{amq_home}/NOTICE  
%doc %{amq_home}/README.txt
%doc %{amq_home}/WebConsole-README.txt
%doc %{amq_home}/user-guide.html
%{amq_home}/bin/*
%{amq_home}/conf/*
%{amq_log}
%{amq_pid}
%{amq_data}
%{amq_home}/lib/*
%{amq_home}/webapps/*
/etc/activemq
/opt/activemq
%attr(755,root,root) %{_initrddir}/%{amq_name}

%changelog
 * Mon Oct 08 2012 Nathan Milford <nathan@milford.io> [5.7.0-1]
 - First shot with ActiveMQ 5.7.0.
