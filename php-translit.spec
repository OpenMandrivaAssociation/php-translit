%define modname translit
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A33_%{modname}.ini

Summary:	Transliterates non-latin character sets to latin
Name:		php-%{modname}
Version:	0.6.0
Release:	%mkrel 19
Group:		Development/PHP
License:	PHP License
URL:		http://derickrethans.nl/translit.php
Source0:	http://pecl.php.net/get/translit-%{version}.tgz
BuildRequires:	php-devel >= 3:5.2.0
Epoch:		1
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This extension allows you to transliterate text in non-latin characters (such
as Chinese, Cyrillic, Greek etc) to latin characters. Besides the
transliteration the extension also contains filters to upper- and lowercase
latin, cyrillic and greek, and perform special forms of transliteration such as
converting ligatures such as the Norwegian "æ" to "ae" and normalizing
punctuation and spacing.

%prep

%setup -q -n translit-%{version}
[ "../package.xml" != "/" ] && mv ../package.xml .

# work around...
mkdir -p ext/iconv
echo "#" > ext/iconv/php_iconv.h
echo "#" > ext/iconv/php_have_bsd_iconv.h
echo "#" > ext/iconv/php_have_libiconv.h
echo "#define HAVE_GLIBC_ICONV 1" > ext/iconv/php_have_glibc_iconv.h
echo "#define HAVE_ICONV 1" > ext/iconv/php_have_iconv.h
echo "#define ICONV_SUPPORTS_ERRNO 1" > ext/iconv/php_iconv_supports_errno.h
echo "#define PHP_ICONV_H_PATH <%{_includedir}/iconv.h>" > ext/iconv/php_php_iconv_h_path.h
echo "#define PHP_ICONV_IMPL \"glibc\"" > ext/iconv/php_php_iconv_impl.h

%build
%serverbuild

phpize
%configure2_5x \
    --enable-%{modname}=shared,%{_prefix}

%make
mv modules/*.so .

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}


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

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc package.xml
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}
