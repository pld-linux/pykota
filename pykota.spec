# TODO: files, initscript, make it working
%define	svn_tag	1904
Name:		pykota
Summary:	Print Quota and Accounting Software Solution
Summary(pl):	Narzêdzie do limitowania i rozliczania wydruków
Version:	0.%{svn_tag}
Release:	0.1
License:	GPL v 2
Group:		Applications/Printing
# NOTE: from svn:
# svn co svn://svn.librelogiciel.com/pykota/trunk pykota
Source0:	%{name}-%{svn_tag}.tar.bz2
# Source0-md5:	0e00c7850342de4dea0cd7d000772e2a
URL:		http://www.librelogiciel.com/software/PyKota/action_Presentation
# Requires: from http://www.librelogiciel.com/software/PyKota/Download/action_Download
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Print Quota and Accounting Software Solution.

%description -l pl
Narzêdzie do limitowania i rozliczania wydruków.

%prep
%setup -q -n %{name}

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT

python setup.py install \
	--root=$RPM_BUILD_ROOT --optimize=2

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
%{_datadir}/%{name}/*.pjl
%{_datadir}/%{name}/*.pl
%{_datadir}/%{name}/*.ps
%{_datadir}/%{name}/logos
# %{_datadir}/%{name}/ldap
