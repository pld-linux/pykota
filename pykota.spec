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
# Requires: from http://www.librelogiciel.com/software/PyKota/Download/action_Download
BuildRequires:	python-ldap
BuildRequires:	python-mx-DateTime
BuildRequires:	python-MySQLdb
BuildRequires:	python-psyco
BuildRequires:	python-PyGreSQL
BuildRequires:	python-PyPAM
BuildRequires:	python-pysnmp
BuildRequires:	python-ReportLab
BuildRequires:	python-sqlite
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Print Quota and Accounting Software Solution.

%description -l pl.UTF-8
Narzędzie do limitowania i rozliczania wydruków.

%prep
%setup -q

%build
python checkdeps.py

python setup.py build

%install
rm -rf $RPM_BUILD_ROOT

python setup.py install \
	--root=$RPM_BUILD_ROOT --optimize=2

mv -f $RPM_BUILD_ROOT%{_mandir}/{el_GR,el}
mv -f $RPM_BUILD_ROOT%{_mandir}/{nb_NO,nb}
mv -f $RPM_BUILD_ROOT%{_mandir}/{sv_SE,sv}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%dir %{py_sitescriptdir}/%{name}
%{py_sitescriptdir}/%{name}/*.py[co]
%dir %{py_sitescriptdir}/%{name}/storages
%{py_sitescriptdir}/%{name}/storages/*.py[co]
%dir %{py_sitescriptdir}/%{name}/reporters
%{py_sitescriptdir}/%{name}/reporters/*.py[co]
%dir %{py_sitescriptdir}/%{name}/loggers
%{py_sitescriptdir}/%{name}/loggers/*.py[co]
%dir %{py_sitescriptdir}/%{name}/accounters
%{py_sitescriptdir}/%{name}/accounters/*.py[co]
%dir %{_datadir}/%{name}
%attr(755,root,root) %{_datadir}/%{name}/*.sh
%attr(755,root,root) %{_datadir}/%{name}/*.php
%attr(755,root,root) %{_datadir}/%{name}/*.py
%attr(755,root,root) %{_datadir}/%{name}/cupspykota
%{_datadir}/%{name}/*.pjl
%{_datadir}/%{name}/*.pl
%{_datadir}/%{name}/*.ps
%{_datadir}/%{name}/logos
%dir %{_datadir}/%{name}/cgi-bin
%attr(755,root,root) %{_datadir}/%{name}/cgi-bin/*.cgi
%{_datadir}/%{name}/ldap
%{_datadir}/%{name}/postgresql

%{_mandir}/man?/*
%lang(el) %{_mandir}/el/man?/*
%lang(de) %{_mandir}/de/man?/*
%lang(es) %{_mandir}/es/man?/*
%lang(fr) %{_mandir}/fr/man?/*
%lang(it) %{_mandir}/it/man?/*
%lang(nb) %{_mandir}/nb_NO/man?/*
%lang(pl) %{_mandir}/pl/man?/*
%lang(pt) %{_mandir}/pt/man?/*
%lang(pt_BR) %{_mandir}/pt_BR/man?/*
%lang(sv) %{_mandir}/sv/man?/*
%lang(th) %{_mandir}/th/man?/*
%lang(tr) %{_mandir}/tr/man?/*
%lang(zh_TW) %{_mandir}/zh_TW/man?/*
