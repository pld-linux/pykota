# NOTE:
#	- only apache is supported (feel free to add support for other httpds)
#	- CGI scripts must be run with uid/gid pykota/pykota privs
#	- that's why they're placed in /home/services/httpd/cgi-bin (suexec req)
#
# Conditional build:
%bcond_without	doc	# don't build HTML/PDF documentation

Summary:	Print Quota and Accounting Software Solution
Summary(pl.UTF-8):	Narzędzie do limitowania i rozliczania wydruków
Name:		pykota
Version:	1.26
Release:	12
License:	GPL v2
Group:		Applications/Printing
# NOTE: from svn:
# svn co svn://svn.librelogiciel.com/pykota/tags/1.26/
Source0:	%{name}-%{version}.tar.bz2
# Source0-md5:	6e4b3232420592695388cbb27511e668
Source1:	%{name}-apache.conf
Source2:	%{name}-httpd.conf
Patch0:		%{name}-conf.patch
Patch1:		%{name}-css.patch
URL:		http://www.pykota.com/
%if %{with doc}
BuildRequires:	docbook-dtd41-sgml
BuildRequires:	docbook-utils
BuildRequires:	texlive-fonts-jknappen
BuildRequires:	texlive-fonts-marvosym
BuildRequires:	texlive-fonts-other
BuildRequires:	texlive-fonts-stmaryrd
BuildRequires:	texlive-fonts-type1-urw
BuildRequires:	texlive-latex-cyrillic
BuildRequires:	texlive-latex-marvosym
BuildRequires:	texlive-xmltex
%endif
BuildRequires:	sqlite3
Requires:	%{name}-common = %{version}-%{release}
Requires:	%{name}-storage = %{version}-%{release}
Requires:	cups >= 1:1.2.0
Requires:	ghostscript
Requires:	python-PIL
Requires:	python-PyPAM
Requires:	python-ReportLab
Requires:	python-chardet
Requires:	python-jaxml
Requires:	python-mx-DateTime >= 2.0.3
Requires:	python-pkipplib
Requires:	python-pkpgcounter
Requires:	python-pyosd
Requires:	python-pysnmp >= 3.4.2
Suggests:	net-snmp-utils >= 4.2.5
Suggests:	netatalk
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		cups_serverbin	%{_prefix}/lib/cups
%define		schemadir	/usr/share/openldap/schema
%define		httpdir		/home/services/httpd
%define		_webapps	/etc/webapps
%define		_webapp		%{name}

%description
Print Quota and Accounting Software Solution.

%description -l pl.UTF-8
Narzędzie do limitowania i rozliczania wydruków.

%package common
Summary:	Common files for pykota
Summary(pl.UTF-8):	Wspólne pliki dla pytkoty
Group:		Applications/Printing
Provides:	group(pykota)
Provides:	user(pykota)

%description common
Common files for pykota.

%description common -l pl.UTF-8
Wspólne pliki dla pytkoty.

%package cgi
Summary:	CGI interface for pykota
Summary(pl.UTF-8):	Interfejs CGI dla pytkoty
Group:		Applications/Printing
Requires:	%{name} = %{version}-%{release}
Requires:	webapps
Requires:	webserver
Requires:	webserver(access)
Requires:	webserver(cgi)
Conflicts:	apache-base < 2.4.0-1

%description cgi
CGI interface for pykota.

%description cgi -l pl.UTF-8
Interfejs CGI dla pykoty.

%package storage-ldap
Summary:	LDAP storage backend for pykota
Summary(pl.UTF-8):	Backend przechowywania danych w LDAP dla pykoty
Group:		Applications/Printing
Requires:	%{name}-common = %{version}-%{release}
Requires:	python-ldap
Provides:	%{name}-storage = %{version}-%{release}

%description storage-ldap
LDAP storage backend for pykota.

%description storage-ldap -l pl.UTF-8
Backend przechowywania danych w LDAP dla pykoty.

%package storage-mysql
Summary:	MySQL storage backend for pykota
Summary(pl.UTF-8):	Backend przechowywania danych w MySQL dla pykoty
Group:		Applications/Printing
Requires:	%{name}-common = %{version}-%{release}
Requires:	python-MySQLdb >= 1.2
Provides:	%{name}-storage = %{version}-%{release}

%description storage-mysql
MySQL storage backend for pykota.

%description storage-mysql -l pl.UTF-8
Backend przechowywania danych w MySQL dla pykoty.

%package storage-postgres
Summary:	PostgreSQL storage backend for pykota
Summary(pl.UTF-8):	Backend przechowywania danych w PostgreSQL dla pykoty
Group:		Applications/Printing
Requires:	%{name}-common = %{version}-%{release}
Requires:	python-PyGreSQL
Provides:	%{name}-storage = %{version}-%{release}

%description storage-postgres
PostgreSQL storage backend for pykota.

%description storage-postgres -l pl.UTF-8
Backend przechowywania danych w PostgreSQL dla pykoty.

%package storage-sqlite
Summary:	SQLite storage backend for pykota
Summary(pl.UTF-8):	Backend przechowywania danych w SQLite dla pykoty
Group:		Applications/Printing
Requires:	%{name}-common = %{version}-%{release}
Requires:	python-sqlite >= 2.0.5
Provides:	%{name}-storage = %{version}-%{release}

%description storage-sqlite
SQLite storage backend for pykota.

%description storage-sqlite -l pl.UTF-8
Backend przechowywania danych w SQLite dla pykoty.

%package -n openldap-schema-pykota
Summary:	pykota LDAP chema
Summary(pl.UTF-8):	Schemat LDAP dla pykoty
Group:		Networking/Daemons
Requires(post,postun):	sed >= 4.0
Requires:	openldap-servers
BuildArch:	noarch

%description -n openldap-schema-pykota
This package contains pykota.schema for openldap.

%description -n openldap-schema-pykota -l pl.UTF-8
Ten pakiet zawiera schemat pykoty dla openldapa.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1

mv po/{el_GR,el}
mv po/{nb_NO,nb}
mv po/{sv_SE,sv}

mv man/{el_GR,el}
mv man/{nb_NO,nb}
mv man/{sv_SE,sv}

find -name .svn | xargs rm -rf

%build
%py_build

%if %{with doc}
cd docs
mkdir html
docbook2html -o html pykota.sgml
docbook2pdf pykota.sgml
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{schemadir},%{_sysconfdir}/%{name}} \
	$RPM_BUILD_ROOT%{cups_serverbin}/backend \
	$RPM_BUILD_ROOT/var/lib/%{name} \
	$RPM_BUILD_ROOT%{httpdir}/cgi-bin/%{name} \
	$RPM_BUILD_ROOT%{_webapps}/%{_webapp}

%py_install

install -p cgi-bin/*.cgi $RPM_BUILD_ROOT%{httpdir}/cgi-bin/%{name}
install -p stylesheets/pykota.css $RPM_BUILD_ROOT%{httpdir}/cgi-bin/%{name}

cp -p initscripts/ldap/pykota.schema $RPM_BUILD_ROOT%{schemadir}

cp -p conf/pykota.conf.sample $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/pykota.conf
cp -p conf/pykotadmin.conf.sample $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/pykotadmin.conf

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_webapps}/%{_webapp}/apache.conf
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_webapps}/%{_webapp}/httpd.conf

ln -s %{_datadir}/%{name}/cupspykota $RPM_BUILD_ROOT%{cups_serverbin}/backend/cupspykota

sqlite3 $RPM_BUILD_ROOT/var/lib/%{name}/pykota.db <initscripts/sqlite/pykota-sqlite.sql

rm -rf $RPM_BUILD_ROOT%{_datadir}/{doc/%{name},%{name}/{conf,ldap,mysql,postgresql,sqlite,stylesheets}}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre common
%groupadd -r -g 501 pykota
%useradd -r -u 501 -d /etc/%{name} -s /bin/sh -c "PyKota User" -g pykota pykota

%postun common
if [ "$1" = "0" ]; then
	%userremove %{name}
	%groupremove %{name}
fi

%triggerin cgi -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun cgi -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin cgi -- apache-base
%webapp_register httpd %{_webapp}

%triggerun cgi -- apache-base
%webapp_unregister httpd %{_webapp}

%post -n openldap-schema-pykota
# dependant schemas: cosine(uid) inetorgperson(displayName) nis(gidNumber)
%openldap_schema_register %{schemadir}/pykota.schema -d cosine,inetorgperson,nis
%service -q ldap restart

%postun -n openldap-schema-pykota
if [ "$1" = "0" ]; then
	%openldap_schema_unregister %{schemadir}/pykota.schema
	%service -q ldap restart
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc CREDITS FAQ LICENSE README SECURITY TODO
%doc openoffice qa-assistant docs/*.sxi
%{?with_doc:%doc docs/*.pdf docs/html}
%attr(750,lp,pykota) %dir %{_sysconfdir}/%{name}
%attr(640,lp,pykota) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/pykota.conf
%attr(640,lp,pykota) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/pykotadmin.conf
%attr(755,root,root) %{_bindir}/*
%{py_sitescriptdir}/%{name}/*.py*
%{py_sitescriptdir}/%{name}/storages/__init__.py*
%{py_sitescriptdir}/%{name}/storages/sql.py*
%dir %{py_sitescriptdir}/%{name}/reporters
%{py_sitescriptdir}/%{name}/reporters/*.py*
%dir %{py_sitescriptdir}/%{name}/loggers
%{py_sitescriptdir}/%{name}/loggers/*.py*
%dir %{py_sitescriptdir}/%{name}/accounters
%{py_sitescriptdir}/%{name}/accounters/*.py*
%{py_sitescriptdir}/*.egg-info
%dir %{_datadir}/%{name}
%attr(755,root,root) %{_datadir}/%{name}/*.sh
%attr(755,root,root) %{_datadir}/%{name}/*.py
%attr(755,root,root) %{_datadir}/%{name}/cupspykota
%{_datadir}/%{name}/*.pjl
%{_datadir}/%{name}/*.ps
%{_datadir}/%{name}/logos

%attr(755,root,root) %{cups_serverbin}/backend/cupspykota

%{_mandir}/man?/*
# commented out fake placeholders
#%lang(de) %{_mandir}/de/man?/*
#%lang(el) %{_mandir}/el/man?/*
#%lang(es) %{_mandir}/es/man?/*
%lang(fr) %{_mandir}/fr/man?/*
#%lang(it) %{_mandir}/it/man?/*
#%lang(nb) %{_mandir}/nb/man?/*
#%lang(pl) %{_mandir}/pl/man?/*
#%lang(pt) %{_mandir}/pt/man?/*
#%lang(pt_BR) %{_mandir}/pt_BR/man?/*
#%lang(sv) %{_mandir}/sv/man?/*
#%lang(th) %{_mandir}/th/man?/*
#%lang(tr) %{_mandir}/tr/man?/*
#%lang(zh_TW) %{_mandir}/zh_TW/man?/*

%files cgi
%defattr(644,root,root,755)
%doc cgi-bin/README
%dir %{_webapps}/%{_webapp}
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_webapps}/%{_webapp}/httpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_webapps}/%{_webapp}/apache.conf
%attr(755,pykota,pykota) %dir %{httpdir}/cgi-bin/%{name}
%attr(755,pykota,pykota) %{httpdir}/cgi-bin/%{name}/*.cgi
%{httpdir}/cgi-bin/%{name}/*.css

%files common
%defattr(644,root,root,755)
%dir %{py_sitescriptdir}/%{name}
%dir %{py_sitescriptdir}/%{name}/storages

%files storage-ldap
%defattr(644,root,root,755)
%{py_sitescriptdir}/%{name}/storages/ldap*.py*

%files storage-mysql
%defattr(644,root,root,755)
%doc initscripts/mysql/*
%{py_sitescriptdir}/%{name}/storages/mysql*.py*

%files storage-postgres
%defattr(644,root,root,755)
%doc initscripts/postgresql/*
%{py_sitescriptdir}/%{name}/storages/pg*.py*

%files storage-sqlite
%defattr(644,root,root,755)
%doc initscripts/sqlite/*
%{py_sitescriptdir}/%{name}/storages/sqlite*.py*
%attr(750,lp,pykota) %dir /var/lib/%{name}
%attr(660,lp,pykota) %config(noreplace) %verify(not md5 mtime size) /var/lib/%{name}/pykota.db

%files -n openldap-schema-pykota
%defattr(644,root,root,755)
%doc initscripts/ldap/{README.ldap,pykota-sample.ldif}
%{schemadir}/pykota.schema
