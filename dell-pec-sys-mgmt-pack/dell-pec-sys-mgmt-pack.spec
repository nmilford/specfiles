# To Build:
#
# sudo yum -y install rpmdevtools && rpmdev-setuptree
#
# wget https://raw.github.com/nmilford/specfiles/master/dell-pec-sys-mgmt-pack/dell-pec-sys-mgmt-pack.spec -O ~/rpmbuild/SPECS/dell-pec-sys-mgmt-pack.spec
# wget http://poweredgec.com/files/sys_mgmt_pack-2012-11-01.tgz -O ~/rpmbuild/SOURCES/sys_mgmt_pack-2012-11-01.tgz
# wget http://poweredgec.com/files/pec-logs-2012-10-22.tgz -O ~/rpmbuild/SOURCES/pec-logs-2012-10-22.tgz
#
# rpmbuild -bb ~/rpmbuild/SPECS/dell-pec-sys-mgmt-pack.spec

%define target_root /opt/dell/pec
%define target_bin  %{target_root}/bin
%define target_docs %{target_root}/docs
%define target_examples %{target_root}/share/examples

Name:      dell-pec-sys-mgmt-pack
Version:   2012.11.01
Release:   1%{?dist}
Summary:   Dell PowerEdge C Systems Management Tools
License:   Unknown
Group:     System Tools
URL:       http://poweredgec.com/
Source0:   http://poweredgec.com/files/sys_mgmt_pack-2012-11-01.tgz
Source1:   http://poweredgec.com/files/pec-logs-2012-10-22.tgz
Requires:  perl >= 5.8, OpenIPMI, OpenIPMI-tools, net-snmp, net-snmp-utils, dmidecode
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
Dell PowerEdge C Systems Management Tools

%prep
rm -rf %{_builddir}/%{name}-%{version}
mkdir -p %{_builddir}/%{name}-%{version}
cd %{_builddir}/%{name}-%{version}
tar zxvf %{SOURCE0}
tar zxvf %{SOURCE1}

%install
install -d -m 755 %{buildroot}/opt
install -d -m 755 %{buildroot}/%{target_root}/


install -d -m 755 %{buildroot}/%{target_docs}/
install    -m 644 %{_builddir}/%{name}-%{version}/sys_mgmt_pack/CHANGELOG*  %{buildroot}/%{target_docs}/
install    -m 644 %{_builddir}/%{name}-%{version}/sys_mgmt_pack/README*     %{buildroot}/%{target_docs}/
install    -m 644 %{_builddir}/%{name}-%{version}/sys_mgmt_pack/INSTALLING* %{buildroot}/%{target_docs}/
install    -m 644 %{_builddir}/%{name}-%{version}/sys_mgmt_pack/*.pdf       %{buildroot}/%{target_docs}/
install    -m 644 %{_builddir}/%{name}-%{version}/sys_mgmt_pack/setupbios/CHANGELOG.setupbios %{buildroot}/%{target_docs}/
install    -m 644 %{_builddir}/%{name}-%{version}/sys_mgmt_pack/setupbios/README.setupbios    %{buildroot}/%{target_docs}/
install    -m 644 %{_builddir}/%{name}-%{version}/sys_mgmt_pack/setupbios/README.setupbios    %{buildroot}/%{target_docs}/
install    -m 644 %{_builddir}/%{name}-%{version}/README.pec-logs           %{buildroot}/%{target_docs}/


install -d -m 755 %{buildroot}/%{target_bin}/
install    -m 644 %{_builddir}/%{name}-%{version}/sys_mgmt_pack/bmc.*          %{buildroot}/%{target_bin}/
install    -m 755 %{_builddir}/%{name}-%{version}/sys_mgmt_pack/bmc            %{buildroot}/%{target_bin}/
install    -m 755 %{_builddir}/%{name}-%{version}/sys_mgmt_pack/sas2ircu       %{buildroot}/%{target_bin}/
install    -m 755 %{_builddir}/%{name}-%{version}/sys_mgmt_pack/ldstate        %{buildroot}/%{target_bin}/
install    -m 755 %{_builddir}/%{name}-%{version}/sys_mgmt_pack/ipmiflash      %{buildroot}/%{target_bin}/
install    -m 644 %{_builddir}/%{name}-%{version}/sys_mgmt_pack/poweredgec.mib %{buildroot}/%{target_bin}/
install    -m 755 %{_builddir}/%{name}-%{version}/sys_mgmt_pack/pecagent       %{buildroot}/%{target_bin}/
install    -m 644 %{_builddir}/%{name}-%{version}/sys_mgmt_pack/pecagent.conf  %{buildroot}/%{target_bin}/
install    -m 644 %{_builddir}/%{name}-%{version}/sys_mgmt_pack/setupbios/bios_settings.* %{buildroot}/%{target_bin}/
install    -m 755 %{_builddir}/%{name}-%{version}/sys_mgmt_pack/setupbios/setupbios       %{buildroot}/%{target_bin}/
install    -m 755 %{_builddir}/%{name}-%{version}/sys_mgmt_pack/setupbios/alternate_version/setupbios.static %{buildroot}/%{target_bin}/
install    -m 755 %{_builddir}/%{name}-%{version}/pec-logs.sh                  %{buildroot}/%{target_bin}/

install -d -m 755 %{buildroot}/%{target_examples}/
install    -m 644 %{_builddir}/%{name}-%{version}/sys_mgmt_pack/examples_pecagent/* %{buildroot}/%{target_examples}/
install    -m 644 %{_builddir}/%{name}-%{version}/sys_mgmt_pack/examples/*  %{buildroot}/%{target_examples}/


install -d -m 755 %{buildroot}/etc/profile.d/
cat <<EOF >> %{buildroot}/etc/profile.d/pec.sh 
export PEC_HOME="%{target_root}"
PATH=%{target_root}/bin:${PATH}
EOF


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{target_root}/*
%{target_bin}/*
%{target_docs}/*
%{target_examples}/*
/etc/profile.d/pec.sh

%changelog
* Mon Jan 14 2013 Nathan Milford <nathan@milford.io> - 1.0-1
- Initial Release.

