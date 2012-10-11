# Originally from https://raw.github.com/seveas/go.rpm/master/go.spec

# This was tweaked to skip tests the failed on RHEL/EL/CentOS 5. *shrug*
# See: https://groups.google.com/forum/?fromgroups=#!topic/golang-nuts/QnjpPVc3V-g

# To build:
# 
# sudo yum -y install rpmdevtools ed bison mercurial && rpmdev-setuptree
# 
# wget https://raw.github.com/nmilford/specfiles/master/go/go.spec -O ~/rpmbuild/SPECS/go.spec
# wget https://go.googlecode.com/files/go1.0.3.src.tar.gz -O ~/rpmbuild/SOURCES/go1.0.3.src.tar.gz
# 
# rpmbuild -bb ~/rpmbuild/SPECS/go.spec

Name:          go
Version:       1.0.3
Release:       1%{?dist}
Summary:       Go compiler and tools
Group:         Development/Languages
License:       BSD
URL:           http://golang.org/
Source0:       http://go.googlecode.com/files/%{name}%{version}.src.tar.gz
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: ed
BuildRequires: bison
BuildRequires: mercurial
%define _use_internal_dependency_generator 0
%define __find_requires %{nil}
%global debug_package %{nil}
%global __spec_install_post /usr/lib/rpm/check-rpaths   /usr/lib/rpm/check-buildroot  \
  /usr/lib/rpm/brp-compress

%ifarch %ix86
    %global GOARCH 386
%endif
%ifarch    x86_64
    %global GOARCH amd64
%endif

%description
Go is a systems programming language that aims to be both fast and convenient.

%package  vim
Summary:  go syntax files for vim
Group:    Applications/Editors
Requires: vim-common
Requires: %{name} = %{version}-%{release}

%description vim
Go syntax for vim.

%package  emacs
Summary:  go syntax files for emacs
Group:    Applications/Editors
Requires: emacs-common
Requires: %{name} = %{version}-%{release}

%description  emacs
Go syntax for emacs.

%prep
%setup -q -n go

%build
GOSRC="$(pwd)"
GOROOT="$(pwd)"
GOROOT_FINAL=%{_libdir}/go
GOOS=linux
GOBIN="$GOROOT/bin"
GOARCH="%{GOARCH}"
export GOARCH GOROOT GOOS GOBIN GOROOT_FINAL
export MAKE=%{__make}

mkdir -p "$GOBIN"
cd src

LC_ALL=C PATH="$PATH:$GOBIN" ./all.bash

%install
rm -rf %{buildroot}

GOROOT_FINAL=%{_libdir}/go
GOROOT="%{buildroot}%{_libdir}/go"
GOOS=linux
GOBIN="$GOROOT/bin"
GOARCH="%{GOARCH}"
export GOARCH GOROOT GOOS GOBIN GOROOT_FINAL

install -Dm644 misc/bash/go %{buildroot}%{_sysconfdir}/bash_completion.d/go
install -Dm644 misc/emacs/go-mode-load.el %{buildroot}%{_datadir}/emacs/site-lisp/go-mode-load.el
install -Dm644 misc/emacs/go-mode.el %{buildroot}%{_datadir}/emacs/site-lisp/go-mode.el
install -Dm644 misc/vim/syntax/go.vim %{buildroot}%{_datadir}/vim/vimfiles/syntax/go.vim
install -Dm644 misc/vim/ftdetect/gofiletype.vim %{buildroot}%{_datadir}/vim/vimfiles/ftdetect/gofiletype.vim
install -Dm644 misc/vim/ftplugin/go/fmt.vim %{buildroot}%{_datadir}/vim/vimfiles/ftplugin/go/fmt.vim
install -Dm644 misc/vim/ftplugin/go/import.vim %{buildroot}%{_datadir}/vim/vimfiles/ftplugin/go/import.vim
install -Dm644 misc/vim/indent/go.vim %{buildroot}%{_datadir}/vim/vimfiles/indent/go.vim

mkdir -p $GOROOT/{misc,lib,src}
mkdir -p %{buildroot}%{_bindir}/

cp -ar pkg include lib bin $GOROOT
cp -ar src/pkg src/cmd $GOROOT/src
cp -ar misc/cgo $GOROOT/misc

ln -sf %{_libdir}/go/bin/go %{buildroot}%{_bindir}/go
ln -sf %{_libdir}/go/bin/godoc %{buildroot}%{_bindir}/godoc
ln -sf %{_libdir}/go/bin/gofmt %{buildroot}%{_bindir}/gofmt

ln -sf %{_libdir}/go/pkg/tool/linux_%{GOARCH}/cgo %{buildroot}%{_bindir}/cgo
ln -sf %{_libdir}/go/pkg/tool/linux_%{GOARCH}/ebnflint %{buildroot}%{_bindir}/ebnflint

%ifarch %ix86
for tool in 8a 8c 8g 8l; do
%else
for tool in 6a 6c 6g 6l; do
%endif
ln -sf %{_libdir}/go/pkg/tool/linux_%{GOARCH}/$tool %{buildroot}%{_bindir}/$tool
done

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS CONTRIBUTORS LICENSE README doc/*
%{_libdir}/go
%ifarch %ix86
%{_bindir}/8*
%else
%{_bindir}/6*
%endif
%{_bindir}/cgo
%{_bindir}/ebnflint
%{_bindir}/go*
%{_sysconfdir}/bash_completion.d/go

%files vim
%defattr(-,root,root,-)
%{_datadir}/vim/vimfiles/ftdetect/gofiletype.vim
%{_datadir}/vim/vimfiles/ftplugin/go/fmt.vim
%{_datadir}/vim/vimfiles/ftplugin/go/import.vim
%{_datadir}/vim/vimfiles/indent/go.vim
%{_datadir}/vim/vimfiles/syntax/go.vim

%files emacs
%defattr(-,root,root,-)
%{_datadir}/emacs/site-lisp/go-mode*.el

%changelog
* Mon Oct 10 2012 Nathan Milford <nathan@milford.io> - 1.0.3
- Skipped tests that fail on RHEl5 because of the O_CLOEXEC issue. Probably a bad idea, but it works so far.
* Mon Oct 01 2012 Kamil Kisiel <kamil@kamilkisiel.net> - 1.0.3
- Update to 1.0.3
* Sun Sep 02 2012 Dennis Kaarsemaker <dennis.kaarsemaker@booking.com> - 1.0.2
- Rename to 'go' and update to 1.0.2
* Sat Feb 12 2012 Dennis Kaarsemaker <dennis.kaarsemaker@booking.com> - 0.20120225
- Go mercurial tip 120120225, package roughly based on Tonnere Lombard's  old one
