Summary:	IRC Conference module for Jabber
Summary(pl):	Modu� konferencyjny IRC systemu Jabber
Name:		jjigw
Version:	0.1
Release:	1
License:	GPL
Group:		Applications/Communications
Source0:	http://www.jabberstudio.org/files/%{name}/%{name}-%{version}.tar.gz
# Source0-md5:	e689cf175d973c970a206325dab77374
Source1:	jjigw.xml
Source2:	jjigw.init
Source3:	jjigw.sysconfig
URL:		http://www.jabberstudio.org/projects/jjigw/
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Requires(post):	perl-base
Requires(post):	textutils
Requires:	python-libxml2
Requires:	python-pyxmpp
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
JJIGW is a Jabber-to-IRC gateway compatible with the Multi User Chat protocol,
it allows you to join IRC channels and communicate with IRC users via your
Jabber client. 

%prep
%setup -q

%build
%{__make} prefix=/usr

%install
install -d $RPM_BUILD_ROOT{/etc/{jabber,rc.d/init.d,sysconfig},%{_bindir}}
%{__make} install DESTDIR=$RPM_BUILD_ROOT prefix=%{_prefix}
perl -pi -e 's#/usr/etc#/etc/jabber#g' $RPM_BUILD_ROOT/%{_bindir}/*
install %{SOURCE1} $RPM_BUILD_ROOT/etc/jabber/
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/jjigw
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/jjigw

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /etc/jabber/secret ] ; then
	SECRET=`cat /etc/jabber/secret`
	if [ -n "$SECRET" ] ; then
        	echo "Updating component authentication secret in the config file..."
		perl -pi -e "s/>secret</>$SECRET</" /etc/jabber/jjigw.xml
	fi
fi

/sbin/chkconfig --add jjigw
if [ -r /var/lock/subsys/jjigw ]; then
	/etc/rc.d/init.d/jjigw restart >&2
else
	echo "Run \"/etc/rc.d/init.d/jjigw start\" to start Jabber IRC Gateway"
fi

%preun
if [ "$1" = "0" ]; then
	if [ -r /var/lock/subsys/jjigw]; then
		/etc/rc.d/init.d/jjigw stop >&2
	fi
	/sbin/chkconfig --del jjigw
fi

%files
%defattr(644,root,root,755)
%doc README TODO *.xml
%attr(755,root,root) %{_bindir}/*
%{_datadir}/*
%attr(640,root,jabber) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/jabber/*
%attr(754,root,root) /etc/rc.d/init.d/jjigw
%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/jjigw