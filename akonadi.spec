
Summary: PIM Storage Service
Name:    akonadi
Version: 1.2.1
Release: 2%{?dist}

Group:   System Environment/Libraries
License: LGPLv2+
URL:     http://download.akonadi-project.org/
Source0: http://download.akonadi-project.org/akonadi-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# shrink default initial db size a bit (approx 140mb->28mb)
%define mysql_conf_timestamp 20090220
Patch1: akonadi-1.1.1-mysql_conf.patch

## upstream patches

BuildRequires: cmake >= 2.6.0
BuildRequires: qt4-devel >= 4.4
BuildRequires: automoc4
BuildRequires: mysql-devel
BuildRequires: mysql-server
# for xsltproc
BuildRequires: libxslt
BuildRequires: shared-mime-info
BuildRequires: boost-devel
BuildRequires: soprano-devel

# when/if akonadi grows support for other backends, consider splitting
# these similar to how phonon is done currently.
Requires: qt4-mysql
# not *strictly* required, but we need a functional default configuration
Requires: mysql-server
Requires(postun): /sbin/ldconfig

%description
%{summary}.
Requires an available instance of mysql server at runtime.  
Akonadi can spawn a per-user one automatically if the mysql-server 
package is installed on the machine.
See also: %{_sysconfdir}/akonadi/mysql-global.conf

%package devel
Summary: Developer files for %{name}
Group:   Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: qt4-devel
Requires: pkgconfig
%description devel
%{summary}.


%prep
%setup -q 

%patch1 -p1 -b .mysql_conf
touch -d %{mysql_conf_timestamp} server/src/storage/mysql-global.conf


%build

mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} \
  -DCONFIG_INSTALL_DIR=%{_sysconfdir} \
  ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT -C %{_target_platform}

mkdir -p $RPM_BUILD_ROOT%{_datadir}/akonadi/agents

touch -d %{mysql_conf_timestamp} $RPM_BUILD_ROOT%{_sysconfdir}/akonadi/mysql-local.conf


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%posttrans
update-mime-database %{_datadir}/mime &> /dev/null || :

%postun
/sbin/ldconfig ||:
if [ $1 -eq 0 ] ; then
  update-mime-database %{_datadir}/mime &> /dev/null ||:
fi


%files
%defattr(-,root,root,-)
%doc AUTHORS lgpl-license
%dir %{_sysconfdir}/akonadi/
%config(noreplace) %{_sysconfdir}/akonadi/mysql-global.conf
%config(noreplace) %{_sysconfdir}/akonadi/mysql-local.conf
%{_bindir}/akonadi_control
%{_bindir}/akonadictl
%{_bindir}/akonadiserver
%{_libdir}/libakonadi*.so.1*
%{_datadir}/dbus-1/interfaces/org.freedesktop.Akonadi.*.xml
%{_datadir}/dbus-1/services/org.freedesktop.Akonadi.*.service
%{_datadir}/mime/packages/akonadi-mime.xml
%{_datadir}/akonadi/

%files devel
%defattr(-,root,root,-)
%{_includedir}/akonadi/
%{_libdir}/pkgconfig/akonadi.pc
%{_libdir}/libakonadi*.so
%{_libdir}/cmake/Akonadi/


%changelog
* Mon Dec 07 2009 Rex Dieter <rdieter@fedoraproject.org> 1.2.1-2
- restore mysql-related dependencies

* Tue Sep  1 2009 Lukáš Tinkl <ltinkl@redhat.com> - 1.2.1-1
- Akonadi 1.2.1

* Fri Aug 28 2009 Rex Dieter <rdieter@fedoraproject.org> 1.2.0-2.2
- temporarily drop mysql-related bits, to workaround broken rawhide deps

* Tue Aug 25 2009 Karsten Hopp <karsten@redhat.com> 1.2.0-2
- bump and rebuild, as s390x picked up an old boost library

* Thu Jul 30 2009 Lukáš Tinkl <ltinkl@redhat.com> - 1.2.0-1
- Akonadi 1.2.0

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.95-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 25 2009 Than Ngo <than@redhat.com> - 1.1.95-1
- 1.1.95

* Wed Jun 03 2009 Rex Dieter <rdieter@fedoraproject.org> 1.1.90-1
- akonadi-1.1.90

* Tue May 26 2009 Rex Dieter <rdieter@fedoraproject.org> 1.1.85-3
- akonadi.pc.cmake: s/AKONADI_LIB_VERSION_STRING/AKONADI_VERSION_STRING/

* Tue May 12 2009 Than Ngo <than@redhat.com> 1.1.85-2
- fix rpm file list

* Wed May 06 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.1.85-1
- akonadi-1.1.85

* Thu Apr 30 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.1.2-1
- akonadi-1.1.2
- optimize scriptlets a bit

* Wed Feb 25 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.1.1-6
- rev startup patch
- BR: cmake >= 2.6.0
- preserve timestamp's on mysql*.conf's

* Tue Feb 24 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.1.1-5
- own %%_sysconfig/akonadi/mysql-local.conf
- startup patch: reset conf only when needed, and clear mysql log file on update

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.1.1-3
- shrink default db initial size a bit (approx 140mb->28mb)
- drop extraneous RPATH-cmake baggage

* Wed Jan 21 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.1.1-1
- 1.1.1

* Sun Jan 04 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.1.0-1
- 1.1.0

* Tue Dec 16 2008 Rex Dieter <rdieter@fedoraproject.org> - 1.0.81-1
- 1.0.81

* Mon Dec 08 2008 Rex Dieter <rdieter@fedoraproject.org> - 1.0.80-3
- restore Requires: mysql-server

* Mon Dec 01 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1.0.80-2
- own /usr/share/akonadi and /usr/share/akonadi/agents (#473595)

* Wed Nov 26 2008 Than Ngo <than@redhat.com> -  1.0.80-1
- 1.0.80

* Wed Oct 22 2008 Rex Dieter <rdieter@fedoraproject.org> 1.0.0-4
- drop Requires: mysql-server (for now), mention in %%description

* Wed Jul 30 2008 Rex Dieter <rdieter@fedoraproject.org> 1.0.0-3
- Requires: mysql-server

* Wed Jul 30 2008 Rex Dieter <rdieter@fedoraproject.org> 1.0.0-2
- BR: mysql-server
- Requires: qt4-mysql
- cleanup spec

* Wed Jul 23 2008 Than Ngo <than@redhat.com> -  1.0.0-1
- 1.0.0

* Wed Jun 18 2008 Rex Dieter <rdieter@fedoraproject.org> 0.82.0-1
- akonadi-0.82.0

* Tue Jun  3 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.81.0-0.2.20080526svn812787
- BR automoc, drop automoc hack

* Mon May 26 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.81.0-0.1.20080526svn812787
- update to revision 812787 from KDE SVN (to match KDE 4.1 Beta 1)
- restore builtin automoc4 for now
- update file list, require pkgconfig in -devel (.pc file now included)

* Mon May  5 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.80.0-2
- -devel: remove bogus Requires: pkgconfig

* Sat May  3 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.80.0-1
- first Fedora package
