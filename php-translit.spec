%define modname translit
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A33_%{modname}.ini

Summary:	Transliterates non-latin character sets to latin
Name:		php-%{modname}
Version:	0.6.1
Release:	%mkrel 5
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


%changelog
* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.6.1-3mdv2011.0
+ Revision: 696377
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.6.1-2
+ Revision: 695322
- rebuilt for php-5.3.7

* Thu Jun 16 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.6.1-1
+ Revision: 685500
- 0.6.1
- drop old pre 5.3 hack

* Thu May 05 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.6.0-21
+ Revision: 667753
- mass rebuild

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.6.0-20
+ Revision: 646561
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.6.0-19mdv2011.0
+ Revision: 629749
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.6.0-18mdv2011.0
+ Revision: 628055
- ensure it's built without automake1.7

* Tue Nov 23 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.6.0-17mdv2011.0
+ Revision: 600187
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.6.0-16mdv2011.0
+ Revision: 588726
- rebuild

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.6.0-15mdv2010.1
+ Revision: 514707
- rebuilt for php-5.3.2

* Mon Feb 22 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.6.0-14mdv2010.1
+ Revision: 509472
- rebuild
- rebuild

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.6.0-12mdv2010.1
+ Revision: 485268
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.6.0-11mdv2010.1
+ Revision: 468095
- rebuilt against php-5.3.1

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.6.0-10mdv2010.0
+ Revision: 451225
- rebuild

* Sun Jul 19 2009 RaphaÃ«l Gertz <rapsys@mandriva.org> 1:0.6.0-9mdv2010.0
+ Revision: 397627
- Rebuild

* Wed May 13 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.6.0-8mdv2010.0
+ Revision: 375366
- rebuilt against php-5.3.0RC2

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.6.0-7mdv2009.1
+ Revision: 346680
- rebuilt for php-5.2.9

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.6.0-6mdv2009.1
+ Revision: 341516
- rebuilt against php-5.2.9RC2

* Thu Jan 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.6.0-5mdv2009.1
+ Revision: 321959
- rebuild

* Fri Dec 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.6.0-4mdv2009.1
+ Revision: 310226
- rebuilt against php-5.2.7

* Tue Jul 15 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.6.0-3mdv2009.0
+ Revision: 235884
- rebuild

* Fri May 02 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.6.0-2mdv2009.0
+ Revision: 200120
- rebuilt against php-5.2.6

* Wed Apr 02 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.6.0-1mdv2008.1
+ Revision: 191581
- 0.6.0

* Mon Feb 04 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.5-19mdv2008.1
+ Revision: 161944
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Nov 11 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.5-18mdv2008.1
+ Revision: 107580
- restart apache if needed

* Sat Sep 01 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.5-17mdv2008.0
+ Revision: 77465
- rebuilt against php-5.2.4

* Thu Aug 16 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.5-16mdv2008.0
+ Revision: 64309
- use the new %%serverbuild macro

* Thu Jun 14 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.5-15mdv2008.0
+ Revision: 39392
- use distro conditional -fstack-protector

* Fri Jun 01 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.5-14mdv2008.0
+ Revision: 33786
- rebuilt against new upstream version (5.2.3)

* Thu May 03 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.5-13mdv2008.0
+ Revision: 21035
- rebuilt against new upstream version (5.2.2)


* Fri Feb 09 2007 Oden Eriksson <oeriksson@mandriva.com> 0.5-12mdv2007.0
+ Revision: 118558
- rebuilt against new upstream php version (5.2.1)

* Wed Nov 08 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.5-11mdv2007.0
+ Revision: 78349
- fix deps
- rebuilt for php-5.2.0

* Thu Nov 02 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.5-9mdv2007.1
+ Revision: 75379
- Import php-translit

* Mon Aug 28 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.5-9
- rebuilt for php-5.1.6

* Thu Jul 27 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.5-8mdk
- rebuild

* Sat May 06 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.5-7mdk
- rebuilt for php-5.1.4

* Fri May 05 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.5-6mdk
- rebuilt for php-5.1.3

* Thu Feb 02 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.5-5mdk
- new group (Development/PHP) and iurt rebuild

* Sun Jan 15 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.5-4mdk
- rebuilt against php-5.1.2

* Tue Nov 29 2005 Oden Eriksson <oeriksson@mandriva.com> 1:0.5-3mdk
- rebuilt against php-5.1.1

* Sat Nov 26 2005 Oden Eriksson <oeriksson@mandriva.com> 1:0.5-2mdk
- rebuilt against php-5.1.0

* Thu Nov 03 2005 Oden Eriksson <oeriksson@mandriva.com> 1:0.5-1mdk
- rebuilt against php-5.1.0RC4
- fix versioning

* Sun Oct 30 2005 Oden Eriksson <oeriksson@mandriva.com> 5.1.0_0.5-0.RC1.2mdk
- rebuilt to provide a -debug package too

* Mon Oct 03 2005 Oden Eriksson <oeriksson@mandriva.com> 5.1.0_0.5-0.RC1.1mdk
- rebuilt against php-5.1.0RC1

* Fri May 27 2005 Oden Eriksson <oeriksson@mandriva.com> 5.0.4_0.5-1mdk
- rename the package

* Sun Apr 17 2005 Oden Eriksson <oeriksson@mandriva.com> 5.0.4_0.5-1mdk
- 5.0.4

* Sun Mar 20 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 5.0.3_0.5-2mdk
- use the %%mkrel macro

* Thu Mar 03 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 5.0.3_0.5-1mdk
- initial Mandrakelinux package

