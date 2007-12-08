# TODO: files, initscript, make it working
Name:		pykota
Summary:	Print Quota and Accounting Software Solution
Summary(pl.UTF-8):	Narzędzie do limitowania i rozliczania wydruków
Version:	1.26
Release:	0.1
License:	GPLv2
Group:		Applications/Printing
# NOTE: from svn:
# svn co svn://svn.librelogiciel.com/pykota/tags/1.26/
Source0:	%{name}-%{version}.tar.bz2
# Source0-md5:	6e4b3232420592695388cbb27511e668
URL:		http://www.pykota.com/
BuildRequires:	docbook-utils
BuildRequires:	docbook-dtd41-sgml
Requires:	ghostscript
Requires:	python-chardet
Requires:	python-pkipplib
Requires:	python-jaxml
Requires:	python-mx-DateTime
Requires:	python-PIL
Requires:	python-pkpgcounter
%ifarch %{ix86}
Requires:	python-psyco
%endif
Requires:	python-pyosd
Requires:	python-PyPAM
Requires:	python-pysnmp >= 3.4.2
Requires:	python-ReportLab
Suggests:	net-snmp-utils
Suggests:	netatalk
Requires:	%{name}-storage
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		schemadir	/usr/share/openldap/schema

%description
Print Quota and Accounting Software Solution.

%description -l pl.UTF-8
Narzędzie do limitowania i rozliczania wydruków.

%package storage-ldap
Summary:	LDAP storage backend for pykota
Summary(pl.UTF-8):	Backend przechowywania danych w LDAP dla pykoty
Group:		Applications/Printing
Requires:	python-ldap
Provides:	%{name}-storage = %{name}-%{version}-%{release}

%description storage-ldap
LDAP storage backend for pykota.

%description storage-ldap -l pl.UTF-8
Backend przechowywania danych w LDAP dla pykoty.

%package storage-mysql
Summary:	MySQL storage backend for pykota
Summary(pl.UTF-8):	Backend przechowywania danych w MySQL dla pykoty
Group:		Applications/Printing
Requires:	python-MySQLdb >= 1.2
Provides:	%{name}-storage = %{name}-%{version}-%{release}

%description storage-mysql
MySQL storage backend for pykota.

%description storage-mysql -l pl.UTF-8
Backend przechowywania danych w MySQL dla pykoty.

%package storage-postgres
Summary:	PostgreSQL storage backend for pykota
Summary(pl.UTF-8):	Backend przechowywania danych w PostgreSQL dla pykoty
Group:		Applications/Printing
Requires:	python-PyGreSQL
Provides:	%{name}-storage = %{name}-%{version}-%{release}

%description storage-postgres
PostgreSQL storage backend for pykota.

%description storage-postgres -l pl.UTF-8
Backend przechowywania danych w PostgreSQL dla pykoty.

%package storage-sqlite
Summary:	SQLite storage backend for pykota
Summary(pl.UTF-8):	Backend przechowywania danych w SQLite dla pykoty
Group:		Applications/Printing
Requires:	python-sqlite >= 2.0.5
Provides:	%{name}-storage = %{name}-%{version}-%{release}

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

%description -n openldap-schema-pykota
This package contains pykota.schema for openldap.

%description -n openldap-schema-pykota -l pl.UTF-8
Ten pakiet zawiera schemat pykoty dla openldap-a.

%prep
%setup -q
mv -f po/{el_GR,el}
mv -f po/{nb_NO,nb}
mv -f po/{sv_SE,sv}

mv -f man/{el_GR,el}
mv -f man/{nb_NO,nb}
mv -f man/{sv_SE,sv}

find -name .svn | xargs rm -rf

%build
python setup.py build

cd docs
mkdir html
docbook2html -o html pykota.sgml
docbook2pdf pykota.sgml

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{schemadir}

python setup.py install \
	--root=$RPM_BUILD_ROOT \
	--optimize=2

%py_postclean

install initscripts/ldap/pykota.schema $RPM_BUILD_ROOT%{schemadir}

rm -rf $RPM_BUILD_ROOT%{_datadir}/{doc/%{name},%{name}/{ldap,mysql,postgresql,sqlite}}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

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
%doc openoffice qa-assistant docs/*.sxi docs/*.pdf docs/html 
%attr(755,root,root) %{_bindir}/*
%dir %{py_sitescriptdir}/%{name}
%{py_sitescriptdir}/%{name}/*.py[co]
%dir %{py_sitescriptdir}/%{name}/storages
%{py_sitescriptdir}/%{name}/storages/__init__.py[co]
%{py_sitescriptdir}/%{name}/storages/sql.py[co]
%dir %{py_sitescriptdir}/%{name}/reporters
%{py_sitescriptdir}/%{name}/reporters/*.py[co]
%dir %{py_sitescriptdir}/%{name}/loggers
%{py_sitescriptdir}/%{name}/loggers/*.py[co]
%dir %{py_sitescriptdir}/%{name}/accounters
%{py_sitescriptdir}/%{name}/accounters/*.py[co]
%{py_sitescriptdir}/*.egg-info
%dir %{_datadir}/%{name}
%attr(755,root,root) %{_datadir}/%{name}/*.sh
%attr(755,root,root) %{_datadir}/%{name}/*.py
%attr(755,root,root) %{_datadir}/%{name}/cupspykota
%{_datadir}/%{name}/*.pjl
%{_datadir}/%{name}/*.ps
%{_datadir}/%{name}/logos
%dir %{_datadir}/%{name}/cgi-bin
%attr(755,root,root) %{_datadir}/%{name}/cgi-bin/*.cgi

%{_mandir}/man?/*
%lang(el) %{_mandir}/el/man?/*
%lang(de) %{_mandir}/de/man?/*
%lang(es) %{_mandir}/es/man?/*
%lang(fr) %{_mandir}/fr/man?/*
%lang(it) %{_mandir}/it/man?/*
%lang(nb) %{_mandir}/nb/man?/*
%lang(pl) %{_mandir}/pl/man?/*
%lang(pt) %{_mandir}/pt/man?/*
%lang(pt_BR) %{_mandir}/pt_BR/man?/*
%lang(sv) %{_mandir}/sv/man?/*
%lang(th) %{_mandir}/th/man?/*
%lang(tr) %{_mandir}/tr/man?/*
%lang(zh_TW) %{_mandir}/zh_TW/man?/*

%files storage-ldap
%defattr(644,root,root,755)
%{py_sitescriptdir}/%{name}/storages/ldap*.py[co]

%files storage-mysql
%defattr(644,root,root,755)
%doc initscripts/mysql/*
%{py_sitescriptdir}/%{name}/storages/mysql*.py[co]

%files storage-postgres
%defattr(644,root,root,755)
%doc initscripts/postgresql/*
%{py_sitescriptdir}/%{name}/storages/pg*.py[co]

%files storage-sqlite
%defattr(644,root,root,755)
%doc initscripts/sqlite/*
%{py_sitescriptdir}/%{name}/storages/sqlite*.py[co]

%files -n openldap-schema-pykota
%defattr(644,root,root,755)
%doc initscripts/ldap/{README.ldap,pykota-sample.ldif}
%{schemadir}/pykota.schema
