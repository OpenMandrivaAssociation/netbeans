# Prevent brp-java-repack-jars from being run.
%define __jar_repack %{nil}

%define __alternatives %{_sbindir}/alternatives

%define nb_              netbeans
%define nb_org           %{nb_}.org
%define nb_ver_major     6.8
%define nb_ver           %{nb_ver_major}
%define nb_alt_priority  680
%define nb_release_time  200907230233
%define nb_home          %{_datadir}/%{nb_}
%define nb_dir           %{nb_home}/%{nb_ver}

%define nb_platform_ver  11
%define nb_platform      platform%{nb_platform_ver}
%define nb_platform_dir  %{nb_home}/%{nb_platform}
%define nb_platform_pkg  %{nb_}-platform
%define nb_platform_vpkg  %{nb_}-%{nb_platform}

%define nb_harness       harness
%define nb_harness_dir   %{nb_home}/%{nb_harness}
%define nb_harness_pkg   %{nb_platform_pkg}-%{nb_harness}

%define nb_ide_ver       12
%define nb_ide_          ide
%define nb_ide           %{nb_ide_}%{nb_ide_ver}
%define nb_ide_dir       %{nb_home}/%{nb_ide}
%define nb_ide_pkg       %{nb_}-%{nb_ide_}
%define nb_ide_vpkg      %{nb_}-%{nb_ide}

%define nb_java_ver      3
%define nb_java_         java
%define nb_java          %{nb_java_}%{nb_java_ver}
%define nb_java_dir      %{nb_home}/%{nb_java}
%define nb_java_pkg      %{nb_}-%{nb_java_}
%define nb_java_vpkg     %{nb_}-%{nb_java}

%define nb_apisupport_ver  1
%define nb_apisupport_     apisupport
%define nb_apisupport      %{nb_apisupport_}%{nb_apisupport_ver}
%define nb_apisupport_dir  %{nb_home}/%{nb_apisupport}
%define nb_apisupport_pkg  %{nb_}-%{nb_apisupport_}
%define nb_apisupport_vpkg %{nb_}-%{nb_apisupport}

%define nb_nb         nb%{nb_ver_major}
%define nb_nb_dir     %{nb_dir}/%{nb_nb}
%define nb_bin_dir    %{nb_dir}/bin
%define nb_etc_dir    %{nb_dir}/etc
%define nb_nb_config_dir %{nb_nb_dir}/config

# See http://wiki.netbeans.org/NBDistroIDs
%define nb_distro_id NBMDV

%define nb_javadoc_site  http://bits.netbeans.org/%{nb_ver}/javadoc

# Prevents use of autoupdate on the specified directory.
# %1 the directory being prevented for autoupdate.
%define noautoupdate()    echo > %1/.noautoupdate

%define cluster base

%define nb_icon         %{nb_nb_dir}/netbeans.png
%define nb_launcher     %{nb_bin_dir}/netbeans
%define nb_desktop      %{name}-ide-%{version}.desktop

%define compiler_opt    -Dbuild.compiler.deprecation=false -Dbuild.compiler.debug=false
%define jdk_opt         -Dpermit.jdk6.builds=true
%define verify_opt      -Dverify.checkout=false
%define ant_nb_opt %{ant} -v %{jdk_opt} %{compiler_opt} %{verify_opt}
%define build_nb_dir nbbuild/netbeans

# Layout defined by ant-1.7.0-1jpp.4.fc9.rpm
%define ant_bin_dir /usr/bin
%define ant_etc_dir %{_datadir}/ant/etc
%define ant_lib_dir %{_datadir}/java
%define ant_lib_dir2 %{_datadir}/java/ant

# Used xml resolver
%define xml_resolver netbeans-resolver
%define xml_resolver_ver 6.7.1
%define xml_resolver_jar %{xml_resolver}-%{xml_resolver_ver}.jar

# Used svn client adapter
%define svnclientadapter     netbeans-svnclientadapter
%define svnclientadapter_ver 6.7.1
%define svnclientadapter_jar libnb-svnClientAdapter.jar

%define javaparser_ver %{nb_ver}

# existing commons-logging-1.0.4.jar instead of required commons-logging-1.1.jar
%define commons_logging_ver 1.1

# existing ini4j-0.3.2.jar instead of required ini4j-0.4.1.jar
%define ini4j_ver 0.4.1

%define svnjavahl_ver 1.6.0

# Links the system JAR
# %1 - the sys jar name
# %2 - the symlink
%global lnSysJAR() if [ -f %{_javadir}/%{1} ] ; then  %__ln_s -f %{_javadir}/%{*} ; else echo "%{1} doesn't exist." ; exit 1 ; fi ; \

Name:           %{nb_}
Version:        %{nb_ver}
Release:        %mkrel 1
Summary:        Integrated Development Environment (IDE)
Group:          Development/Java
License:        GPLv2 with exceptions or CDDL
Vendor:         netbeans.org
URL:            http://www.netbeans.org

# The official zip is used: MD5: 1b085b82e04788beaf245859f818dcad
Source0: http://download.netbeans.org/netbeans/6.8/final/zip/netbeans-6.8-200912041610-src.zip

Source1: %{name}-ide.desktop-template
%define nb_desktop_template %{SOURCE1}

# Enables the Update Center (UC) for Fedora
Patch0: %{name}-%{version}~00-updatecenters.patch
# Removes actions against binary files
Patch1: %{name}-%{version}~10-ant-patch.patch
# Removes KenaiAction from the welcome page
Patch2: %{name}-%{version}~20-welcome.patch
# Removes windows components
Patch3: %{name}-%{version}~30-build-xml.patch
# Adapts IDE launcher for Fedora
# - unset DESKTOP_STARTUP_ID
# - set progdir
# - exec /etc/netbeans.conf
# - avoid interactive accepting license
# http://wiki.netbeans.org/Fedora10PackagingNBIDELauncher
# https://bugzilla.redhat.com/show_bug.cgi?id=464820
# https://bugzilla.redhat.com/show_bug.cgi?id=467546
Patch4: %{name}-%{version}~40-ide-launcher.patch 
# Avoids releasing binary files
Patch5: %{name}-%{version}~50-build-copy.patch 
# Avoids using svnkit
Patch6: %{name}-%{version}~60-nosvnkit.patch
# Sets up IDE configuration
Patch7: %{name}-%{version}~70-small-ide-cluster.patch
Patch8: %{name}-%{version}~71-cluster-properties.patch
# Disables the checkmoduleconfigs task
Patch9: %{name}-%{version}~80-check-modules.patch
# Avoids failonerror during copying license file.
# The file is moved to the top directory of the tarball.
Patch10: %{name}-%{version}~90-copy_license.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

BuildRequires: jpackage-utils
BuildRequires: java-rpmbuild >= 1.7.5
BuildRequires: java-devel >= 1.6.0
BuildRequires: ant >= 0:1.7.0
BuildRequires: ant-junit >= 0:1.7.0
BuildRequires: ant-nodeps >= 0:1.7.0
BuildRequires: ant-trax >= 0:1.7.0
BuildRequires: bytelist
BuildRequires: junit >= 3.8.2
BuildRequires: junit4 >= 4.5
BuildRequires: jvyamlb
BuildRequires: jzlib
BuildRequires: swing-layout >= 0:1.0
BuildRequires: javahelp2 >= 2.0.05
BuildRequires: lucene >= 2.4.0
BuildRequires: unzip
BuildRequires: desktop-file-utils
BuildRequires: netbeans-javaparser >= %{javaparser_ver}
BuildRequires: xerces-j2 >= 2.8.0
BuildRequires: appframework >= 1.0.3
BuildRequires: beansbinding >= 1.2.1
BuildRequires: freemarker >= 2.3.10
BuildRequires: jsch >= 0.1.39
BuildRequires: %{xml_resolver} >= %{xml_resolver_ver}
BuildRequires: ini4j >= 0.4.1
BuildRequires: netbeans-svnclientadapter >= %{svnclientadapter_ver}
BuildRequires: svn-javahl >= 1.5.0
BuildRequires: swingx
BuildRequires: jakarta-commons-logging >= 1.0.4
BuildRequires: jakarta-oro >= 2.0.8
BuildRequires: jakarta-commons-net >= 1.4.1
BuildRequires: %{nb_harness_pkg}   >= %{version}
BuildRequires: %{nb_platform_vpkg} >= %{version}
BuildRequires: java-rpmbuild >= 0:1.5.32

Requires: jpackage-utils
Requires: java >= 1.6.0
Requires: %{nb_apisupport_vpkg} >= %{version}
Requires: %{nb_harness_pkg}     >= %{version}
Requires: %{nb_ide_vpkg}        >= %{version}
Requires: %{nb_java_vpkg}       >= %{version}
Requires: %{nb_platform_vpkg}   >= %{version}
Requires: lucene >= 2.4.0
Requires: junit >= 3.8.2
Requires: junit4 >= 4.5

%description
NetBeans IDE is an Integrated Development Environment (IDE) for Java/JavaFX, 
C/C++, Ruby, UML, etc. The NetBeans IDE is oriented on wide audience of 
developers from beginners up to experts. A developer can find useful set of 
the development tools that are embedded in the IDE or can be integrated with. 
The NetBeans IDE is the modular system and it can be configured according to 
user needs. Please, visit http://www.netbeans.org/ for more information about 
this open-source project.


%package %{nb_apisupport_}

Summary: Common NetBeans Platform Development Related Libraries for NetBeans
Group: Development/Java
Requires: jpackage-utils
Requires: java >= 1.6.0
Requires: %{nb_ide_vpkg}      >= %{version}
Requires: %{nb_java_vpkg}     >= %{version}
Requires: %{nb_platform_vpkg} >= %{version}
Requires: %{nb_harness_pkg}   >= %{version}

Provides: %{nb_apisupport_vpkg} = %{version}-%{release}

%description %{nb_apisupport_}
The NetBeans appisupport cluster, version %{nb_apisupport_ver}.
Common libraries for development of NetBeans Platform modular extensions.


%package %{nb_ide_}

Summary: Integrated Development Environment (IDE) Libraries for NetBeans
Group: Development/Java
Requires: jpackage-utils
Requires: java >= 1.6.0
Requires: jsch
Requires: %{xml_resolver} >= %{xml_resolver_ver}
Requires: ini4j
Requires: freemarker >= 2.3.8
Requires: xerces-j2 >= 2.7.1
Requires: netbeans-svnclientadapter >= %{svnclientadapter_ver}
Requires: svn-javahl >= 1.5.0
Requires: jakarta-commons-logging >= 1.0.4
Requires: jakarta-oro >= 2.0.8
Requires: jakarta-commons-net >= 1.4.1
Requires: bytelist
Requires: jvyamlb
Requires: jzlib
Requires: swingx
# A requirement for the owner of the /usr/share/netbeans directory
Requires: %{nb_platform_vpkg} >= %{version}

Provides: %{nb_ide_vpkg} = %{version}-%{release}

%description %{nb_ide_}
The NetBeans ide cluster, version %{nb_ide_ver}.
Common languages independent libraries for use in the IDE.


%package %{nb_java_}

Summary: Common Java Related Libraries for NetBeans
Group: Development/Java
Requires: jpackage-utils
Requires: java >= 1.6.0
Requires: java-devel >= 0:1.6.0
Requires: netbeans-javaparser >= %{javaparser_ver}
Requires: appframework >= 1.0.3
Requires: beansbinding >= 1.2.1
Requires: ant >= 1.7.0
Requires: ant-junit >= 1.7.0
Requires: ant-nodeps >= 1.7.0
Requires: ant-trax >= 1.7.0
Requires: %{nb_ide_vpkg} >= %{version}
# A requirement for the owner of the /usr/share/netbeans directory
Requires: %{nb_platform_vpkg} >= %{version}

Provides: %{nb_java_vpkg} = %{version}-%{release}

%description %{nb_java_}
The NetBeans java cluster, version %{nb_java_ver}.
Common libraries for the NetBeans Java IDE.

%prep
%setup -q -c

find . -type f \( -iname "*.jar" -o -iname "*.zip" \) -print0 | xargs -t -0 %{__rm} -f
find . -type f \( -iname "binaries-list" \) | xargs -t %{__rm} -f
find . -type f \( -iname "*.ser" \) -print0 | xargs -t -0 %{__rm} -f

# Generate stub jar file, so there is something in jsr223  module.
%{__mkdir_p} libs.jsr223/src/javax/script
echo "As of Java 6, JSR 223 is included in the JRE." > libs.jsr223/src/javax/script/readme.txt
%{__mkdir_p} libs.jsr223/external
jar cf libs.jsr223/external/jsr223-api.jar libs.jsr223/src/javax/script/readme.txt

# Generate stub jar file, so there is something in swingapp module.
%{__mkdir_p} swingapp/src/javax/swing
echo "As of Java 6, SwingWorker is included in the JRE." > swingapp/src/javax/swing/SwingWorker-readme.txt
%{__mkdir_p} swingapp/external
jar cf swingapp/external/swing-worker-1.1.jar swingapp/src/javax/swing/SwingWorker-readme.txt

# To build the netbeans modules the installed jars will be used instead of pre-packaged ones
# - javahelp2.jar is required for the build target "bootstrap" for "JavaHelp indexing".
#   see also classpath in the jhindexer task in nbbuild/templates/projectized.xml (334)
%{__mkdir_p} apisupport.harness/external
%lnSysJAR javahelp2.jar apisupport.harness/external/jsearch-2.0_05.jar
%lnSysJAR javahelp2.jar javahelp/external/jh-2.0_05.jar
# - links ant libs
%{__ln_s} -f %{_javadir} o.apache.tools.ant.module/external/lib

%patch0 -p1 -b .sav
%patch1 -p1 -b .sav
%patch2 -p1 -b .sav
%patch3 -p1 -b .sav
%patch4 -p1 -b .sav
%patch5 -p1 -b .sav
%patch6 -p1 -b .sav
%patch7 -p1 -b .sav
%patch8 -p1 -b .sav
%patch9 -p1 -b .sav
%patch10 -p1 -b .sav

%build

%{__mkdir_p} %{build_nb_dir}
%{__ln_s} -f %{nb_platform_dir} %{build_nb_dir}/%{nb_platform}
%{__ln_s} -f %{nb_harness_dir} %{build_nb_dir}/%{nb_harness}

IDE_EXT_DIR=%{build_nb_dir}/%{nb_ide}/modules/ext
%{__mkdir_p} ${IDE_EXT_DIR}
%lnSysJAR jsch.jar ${IDE_EXT_DIR}/jsch-0.1.41.jar
%lnSysJAR %{xml_resolver_jar} ${IDE_EXT_DIR}/resolver-1.2.jar
%lnSysJAR ini4j.jar  ${IDE_EXT_DIR}/ini4j-%{ini4j_ver}.jar

# The freemarker 2.2 isn't compatible with 2.3. It means that future versions can be incompatible too.
# Therefore, we must use the freemarker-2.3.jar link instead of freemarker.jar
%lnSysJAR freemarker.jar  ${IDE_EXT_DIR}/freemarker-2.3.8.jar
%lnSysJAR %{svnclientadapter_jar} ${IDE_EXT_DIR}/svnClientAdapter-1.6.0.jar
%lnSysJAR svn-javahl.jar  ${IDE_EXT_DIR}/svnjavahl-%{svnjavahl_ver}.jar
%lnSysJAR xerces-j2.jar  ${IDE_EXT_DIR}/xerces-2.8.0.jar
%lnSysJAR lucene.jar  ${IDE_EXT_DIR}/lucene-core-2.4.1.jar
%lnSysJAR commons-logging.jar ${IDE_EXT_DIR}/commons-logging-%{commons_logging_ver}.jar
%lnSysJAR jakarta-oro.jar ${IDE_EXT_DIR}/jakarta-oro-2.0.8.jar
%lnSysJAR commons-net.jar ${IDE_EXT_DIR}/commons-net-1.4.1.jar
%lnSysJAR jzlib.jar ${IDE_EXT_DIR}/jzlib-1.0.7.jar
%lnSysJAR bytelist.jar ${IDE_EXT_DIR}/bytelist-0.1.jar
%lnSysJAR jvyamlb.jar ${IDE_EXT_DIR}/jvyamlb-0.2.3.jar
%lnSysJAR swingx.jar ${IDE_EXT_DIR}/swingx-0.9.5.jar

JAVA_EXT_DIR=%{build_nb_dir}/%{nb_java}/modules/ext
%{__mkdir_p} ${JAVA_EXT_DIR}
%lnSysJAR netbeans-javaparser-api-%{version}.jar ${JAVA_EXT_DIR}/javac-api-nb-7.0-b07.jar
%lnSysJAR netbeans-javaparser-impl-%{version}.jar ${JAVA_EXT_DIR}/javac-impl-nb-7.0-b07.jar
%lnSysJAR appframework.jar ${JAVA_EXT_DIR}/appframework-1.0.3.jar
%lnSysJAR beansbinding.jar ${JAVA_EXT_DIR}/beansbinding-1.2.1.jar
%lnSysJAR junit.jar ${JAVA_EXT_DIR}/junit-3.8.2.jar

%{ant_nb_opt} \
    -Do.n.core.dir=%{nb_platform_dir} \
    -Ddo-not-rebuild-clusters=true \
    -Dnb.cluster.platform-is-built=true \
    -Dnb.cluster.harness-is-built=true \
    -Dcore.dir=%{nb_platform_dir} \
    -Do.n.bootstrap.dir=%{nb_platform_dir} \
    -Dopenide.awt.dir=%{nb_platform_dir} \
    -Dlibs.beans-binding.classpath=%{_javadir}/beansbinding.jar \
    -Dlibs.swing-layout.classpath=%{_javadir}/swing-layout.jar \
    -Dcluster.config=basic \
    -f nbbuild/build.xml build-nozip

# Build desktop file
%{__cp} -p %{nb_desktop_template} %{nb_desktop}
sed --in-place "s|<nb_ver>|%{nb_ver}|g" %{nb_desktop}
sed --in-place "s|<nb_icon>|%{nb_icon}|g" %{nb_desktop}
sed --in-place "s|<nb_launcher>|%{nb_launcher}|g" %{nb_desktop}

# clean up links to ext jars for the ide module
pushd ${IDE_EXT_DIR}
  %{__rm} -f jsch-0.1.41.jar
  %{__rm} -f resolver-1.2.jar
  %{__rm} -f ini4j-%{ini4j_ver}.jar
  %{__rm} -f freemarker-2.3.8.jar
  %{__rm} -f svnClientAdapter-1.6.0.jar
  %{__rm} -f svnjavahl-%{svnjavahl_ver}.jar
  %{__rm} -f xerces-2.8.0.jar
  %{__rm} -f lucene-core-2.4.1.jar
  %{__rm} -f commons-logging-%{commons_logging_ver}.jar
  %{__rm} -f jakarta-oro-2.0.8.jar
popd

# clean up links to ext jars for the java module
pushd ${JAVA_EXT_DIR}
  %{__rm} -f javac-api-nb-7.0-b07.jar
  %{__rm} -f javac-impl-nb-7.0-b07.jar
  %{__rm} -f appframework-1.0.3.jar
  %{__rm} -f beansbinding-1.2.1.jar
  %{__rm} -f junit-4.5.jar
  %{__rm} -f junit-3.8.2.jar
popd

%install

# Installs the specified source(s) in the destination directory.
# $1 the destination directory.
# $2 the source(s), e.g. nbbuild/netbeans/platform8/* .
install_package() {
    DISTDIR=$1
    shift
    SOURCES=$*
    %{__mkdir_p} ${DISTDIR}
    %{__cp} -pr ${SOURCES} ${DISTDIR}
}

%{__rm} -rf %{buildroot}

# Install apisupport
install_package %{buildroot}%{nb_apisupport_dir} %{build_nb_dir}/%{nb_apisupport}/*
%noautoupdate %{buildroot}%{nb_apisupport_dir}

# Install ide
install_package %{buildroot}%{nb_ide_dir} %{build_nb_dir}/%{nb_ide}/*
%noautoupdate %{buildroot}%{nb_ide_dir}

# linking the ide to the external JARs
pushd %{buildroot}%{nb_ide_dir}/modules/ext
  %lnSysJAR jsch.jar jsch-0.1.41.jar
  %lnSysJAR %{xml_resolver_jar} resolver-1.2.jar
  %lnSysJAR ini4j.jar ini4j-%{ini4j_ver}.jar
# The freemarker 2.2 isn't compatible with 2.3. It means that future versions can be incompatible too.
# Therefore, we must use the freemarker-2.3.jar link instead of freemarker.jar
  %lnSysJAR freemarker.jar freemarker-2.3.8.jar
  %lnSysJAR %{svnclientadapter_jar} svnClientAdapter-1.6.0.jar
  %lnSysJAR svn-javahl.jar svnjavahl-%{svnjavahl_ver}.jar
  %lnSysJAR xerces-j2.jar xerces-2.8.0.jar
  %lnSysJAR lucene.jar lucene-core-2.4.1.jar
  %lnSysJAR commons-logging.jar commons-logging-%{commons_logging_ver}.jar
  %lnSysJAR jakarta-oro.jar jakarta-oro-2.0.8.jar
  %lnSysJAR jzlib.jar jzlib-1.0.7.jar
  %lnSysJAR bytelist.jar bytelist-0.1.jar
  %lnSysJAR jvyamlb.jar jvyamlb-0.2.3.jar
  %lnSysJAR swingx.jar swingx-0.2.3.jar
popd

# Install java
install_package %{buildroot}%{nb_java_dir} %{build_nb_dir}/%{nb_java}/*
# install java ant
install -d -m 755 %{buildroot}%{nb_java_dir}/ant/bin
install -d -m 755 %{buildroot}%{nb_java_dir}/ant/lib
%noautoupdate %{buildroot}%{nb_java_dir}

# linking the java to the external JARs
pushd %{buildroot}%{nb_java_dir}/modules/ext
  %lnSysJAR netbeans-javaparser-api.jar javac-api-nb-7.0-b07.jar
  %lnSysJAR netbeans-javaparser-impl.jar javac-impl-nb-7.0-b07.jar
  %lnSysJAR appframework.jar appframework-1.0.3.jar
  %lnSysJAR beansbinding.jar beansbinding-1.2.1.jar
  %lnSysJAR junit4.jar junit-4.5.jar
  %lnSysJAR junit.jar junit-3.8.2.jar
popd

# linking the Ant components
pushd %{buildroot}%{nb_java_dir}/ant
  %{__ln_s} -f %{ant_bin_dir}/ant bin/ant
  %{__ln_s} -f %{ant_bin_dir}/antRun bin/antRun
  %{__ln_s} -f %{ant_etc_dir} etc
# - jars
  pushd lib
    %{__ln_s} -f %{ant_lib_dir}/ant.jar ant.jar
    %{__ln_s} -f %{ant_lib_dir}/ant-launcher.jar ant-launcher.jar
    %{__ln_s} -f %{ant_lib_dir2}/ant-junit.jar ant-junit.jar
    %{__ln_s} -f %{ant_lib_dir2}/ant-nodeps.jar ant-nodeps.jar
    %{__ln_s} -f %{ant_lib_dir2}/ant-trax.jar ant-trax.jar
  popd
popd

# Install nb
install_package %{buildroot}%{nb_nb_dir} %{build_nb_dir}/%{nb_nb}/*
# install nb bin (launcher)
install_package %{buildroot}%{nb_bin_dir} %{build_nb_dir}/bin/*
# install nb etc (netbeans.conf, netbeans.clusters)
install_package %{buildroot}%{nb_etc_dir} %{build_nb_dir}/etc/*
# install nb htmls
%{__cp} -p %{build_nb_dir}/CREDITS.html %{buildroot}%{nb_dir}/
%{__cp} -p %{build_nb_dir}/README.html %{buildroot}%{nb_dir}/
%{__cp} -p %{build_nb_dir}/netbeans.css %{buildroot}%{nb_dir}/
# inistall nb/nbX.X config
echo -n "%{nb_distro_id}" > %{buildroot}%{nb_nb_config_dir}/productid
%noautoupdate %{buildroot}%{nb_nb_dir}

# Links to nbX.X components
pushd %{buildroot}%{nb_dir}
  %{__ln_s} ../%{nb_harness}    %{nb_harness}
  %{__ln_s} ../%{nb_apisupport} %{nb_apisupport}
  %{__ln_s} ../%{nb_ide}        %{nb_ide}
  %{__ln_s} ../%{nb_java}       %{nb_java}
  %{__ln_s} ../%{nb_platform}   %{nb_platform}
popd

# Install desktop file
desktop-file-validate  %{nb_desktop}
install -d -m 755 %{buildroot}%{_datadir}/applications/%{nb_org}
desktop-file-install --vendor="" \
    --dir=%{buildroot}%{_datadir}/applications/%{nb_org} \
    %{nb_desktop}

%clean
%{__rm} -rf %{buildroot}

%post
%{__alternatives} --install %{_bindir}/%{nb_} %{nb_} %{nb_launcher} %{nb_alt_priority}

%preun
if [ "$1" = "0" ]; then
    %{__alternatives} --remove %{nb_} %{nb_launcher}
fi

%files
%defattr(-,root,root,-)
%dir %{nb_dir}/
%{nb_dir}/
%docdir %{nb_nb_dir}/docs
%dir %{nb_bin_dir}/
%attr(755,root,root) %{nb_launcher}
%{nb_etc_dir}/
%doc %{nb_dir}/CREDITS.html
%doc %{nb_dir}/README.html
%doc %{nb_dir}/netbeans.css
%dir %{_datadir}/applications/%{nb_org}/
%{nb_nb_dir}/.noautoupdate
%{_datadir}/applications/%{nb_org}/%{nb_desktop}
%doc ide.branding/release-toplevel/LICENSE.txt

%files %{nb_apisupport_}
%defattr(-,root,root,-)
%{nb_apisupport_dir}/
%{nb_apisupport_dir}/.noautoupdate
%doc ide.branding/release-toplevel/LICENSE.txt

%files %{nb_ide_}
%defattr(-,root,root,-)
%{nb_ide_dir}/
%{nb_ide_dir}/.noautoupdate
%doc ide.branding/release-toplevel/LICENSE.txt

%files %{nb_java_}
%defattr(-,root,root,-)
%{nb_java_dir}/
%{nb_java_dir}/.noautoupdate
%doc ide.branding/release-toplevel/LICENSE.txt
