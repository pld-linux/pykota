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
BuildRequires:	ghostscript
BuildRequires:	net-snmp-utils
BuildRequires:	python-chardet
BuildRequires:	python-pkipplib
BuildRequires:	python-jaxml
BuildRequires:	python-ldap
BuildRequires:	python-mx-DateTime
BuildRequires:	python-mx-DateTime-devel
BuildRequires:	python-MySQLdb >= 1.2
BuildRequires:	python-PIL
BuildRequires:	python-PIL-devel
BuildRequires:	python-pkpgcounter
%ifarch %{ix86}
BuildRequires:	python-psyco
%endif
BuildRequires:	python-PyGreSQL
BuildRequires:	python-pyosd
BuildRequires:	python-PyPAM
BuildRequires:	python-pysnmp >= 3.4.2
BuildRequires:	python-ReportLab
BuildRequires:	python-sqlite >= 2.0.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Print Quota and Accounting Software Solution.

%description -l pl.UTF-8
Narzędzie do limitowania i rozliczania wydruków.

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
python checkdeps.py

python setup.py build

cd docs
mkdir html
docbook2html -o html pykota.sgml
docbook2pdf pykota.sgml

%install
rm -rf $RPM_BUILD_ROOT

python setup.py install \
	--root=$RPM_BUILD_ROOT \
	--optimize=2

%py_postclean

rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/%{name}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc CREDITS FAQ LICENSE README SECURITY TODO
%doc openoffice qa-assistant docs/*.sxi docs/*.pdf docs/html 
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
%{_datadir}/%{name}/ldap
%{_datadir}/%{name}/postgresql

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
