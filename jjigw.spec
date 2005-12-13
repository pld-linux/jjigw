Summary:	IRC Conference module for Jabber
Summary(pl):	Modu³ konferencyjny IRC systemu Jabber
Name:		jjigw
Version:	0.2.1
Release:	0.2
License:	GPL
Group:		Applications/Communications
Source0:	http://www.jabberstudio.org/files/jjigw/%{name}-%{version}.tar.gz
# Source0-md5:	b8b25ebed5aedb28365a528211bdd75e
Source1:	%{name}.xml
Source2:	%{name}.init
Source3:	%{name}.sysconfig
URL:		http://www.jabberstudio.org/projects/jjigw/
Requires(post):	perl-base
Requires(post):	textutils
Requires(post,preun):	/sbin/chkconfig
Requires:	python-libxml2
Requires:	python-pyxmpp
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
JJIGW is a Jabber-to-IRC gateway compatible with the Multi User Chat
protocol, it allows you to join IRC channels and communicate with IRC
users via your Jabber client.

%description -l pl
JJIGW to bramka Jabber-IRC kompatybilna z protoko³em Multi User Chat.
Pozwala przy³±czaæ siê do kana³ów IRC i komunikowaæ z u¿ytkownikami
IRC-a poprzez klienta Jabbera.

%prep
%setup -q

%build
%{__make} \
	prefix=%{_prefix}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/{jabber,rc.d/init.d,sysconfig},%{_bindir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	prefix=%{_prefix}

perl -pi -e 's#%{_prefix}%{_sysconfdir}#%{_sysconfdir}/jabber#g' $RPM_BUILD_ROOT%{_bindir}/*

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/jabber
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/jjigw
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/jjigw

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
%attr(640,root,jabber) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/jabber/*
%attr(754,root,root) /etc/rc.d/init.d/jjigw
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/jjigw
