%define modname translit
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A33_%{modname}.ini

Summary:	Transliterates non-latin character sets to latin
Name:		php-%{modname}
Epoch:		1
Version:	0.6.1
Release:	10
Group:		Development/PHP
License:	PHP License
Url:		http://derickrethans.nl/translit.php
Source0:	http://pecl.php.net/get/translit-%{version}.tgz
BuildRequires:	php-devel >= 3:5.2.0

%description
This extension allows you to transliterate text in non-latin characters (such
as Chinese, Cyrillic, Greek etc) to latin characters. Besides the
transliteration the extension also contains filters to upper- and lowercase
latin, cyrillic and greek, and perform special forms of transliteration such as
converting ligatures such as the Norwegian "æ" to "ae" and normalizing
punctuation and spacing.

%prep
%setup -qn translit-%{version}
[ "../package.xml" != "/" ] && mv ../package.xml .

%build
%serverbuild

phpize
%configure2_5x \
	--enable-%{modname}=shared,%{_prefix}

%make
mv modules/*.so .

%install
install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m755 %{soname} %{buildroot}%{_libdir}/php/extensions/

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}
EOF

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%files 
%doc package.xml
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}

