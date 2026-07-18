#!/bin/bash

echo "**RHEL**"

#System Information
#hostname
echo "fact: hostname"
hostname

#ip
echo "fact: ip_address"
ip -4 -o addr show scope global | awk '{split($4,a,"/"); print a[1]}'|grep -v '[#]'

#mac address
echo "fact: ifconfig_mac_addresses"
ifconfig -a |  grep -o -E '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}'

#uname -a (all)
echo "fact: uname_all"
uname -a

#What type of virtualization a system is running
echo "fact: virt_what_type"
virt-what;echo $?

#name of package that provides ‘redhat-release’
echo "fact: redhat_release_name"
rpm -q --queryformat "%{NAME}\n" --whatprovides redhat-release

#release of package that provides ‘redhat-release’
echo "fact: redhat_release_release"
rpm -q --queryformat "%{RELEASE}\n" --whatprovides redhat-release

#version of package that provides ‘redhat-release’
echo "fact: redhat_release_version"
rpm -q --queryformat "%{VERSION}\n" --whatprovides redhat-release

# number of cores per socket
echo "fact: cpu_core_per_socket"
cat /proc/cpuinfo 2>/dev/null | grep '^cpu cores\s*.' | sed -n -e 's/^.*cpu cores\s*.\s*//p' | uniq

# number of processors
echo "fact: cpu_count"
cat /proc/cpuinfo 2>/dev/null | grep '^processor\s*.' | wc -l

# cpu family
echo "fact: cpu_cpu_family"
cat /proc/cpuinfo 2>/dev/null | grep '^cpu family\s*.' | sed -n -e 's/^.*cpu family\s*.\s*//p' | uniq

# Whether cpu is hyperthreaded
echo "fact: cpu_hyperthreading"
cat /proc/cpuinfo 2>/dev/null | grep '^siblings\s*.' | sed -n -e 's/^.*siblings\s*.\s*//p' | uniq

# cpu model name
echo "fact: cpu_model_name"
cat /proc/cpuinfo 2>/dev/null | grep '^model name\s*.' | sed -n -e 's/^.*model name\s*.\s*//p' |uniq

# cpu model version
echo "fact: cpu_model_ver"
cat /proc/cpuinfo 2>/dev/null | grep '^model\s*.' | sed -n -e 's/^.*model\s*.\s*//p' | sort | uniq

# cpu siblings
echo "fact: cpu_siblings"
cat /proc/cpuinfo 2>/dev/null | grep '^siblings\s*.' | sed -n -e 's/^.*siblings\s*.\s*//p' |uniq

# cpu vendor name
echo "fact: cpu_vendor_id"
cat /proc/cpuinfo 2>/dev/null | grep '^vendor_id\s*' | sed -n -e 's/^.*vendor_id\s*.\s*//p' |uniq

# /root/anaconda-ks.cfg modified time *needs root*
echo "fact: date_anaconda_log"
ls --full-time /root/anaconda-ks.cfg 2>/dev/null | grep -o '[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}'

# date
echo "fact: date_date"
date

# uses tune2fs -l on the / filesystem dev found using mount *might need root*
echo "fact: date_filesystem_create"
fs_date=$(tune2fs -l $(mount | egrep '/ type' | grep -o '/dev.* on' | sed -e 's/\on//g') 2>/dev/null | grep 'Filesystem created' | sed 's/Filesystem created:\s*//g'); if [[ $fs_date ]]; then date +'%F' -d "$fs_date"; else echo "" ; fi

# /etc/machine-id modified time’
echo "fact: date_machine_id"
if [ -f /etc/machine-id ] ; then ls --full-time /etc/machine-id 2>/dev/null | grep -o '[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}' ; fi

# dates from yum history
echo "fact: date_yum_history"
yum history 2>/dev/null  | tail -n 2 | grep -o '[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}'

# date on etc
echo "fact: etc_date"
ls -lact --full-time /etc |awk 'END {print $6}'

# bios vendor name
echo "fact: dmi_bios_vendor"
/usr/sbin/dmidecode -s bios-vendor 2>/dev/null

#number of installed packages
echo "fact: installed_packages"
rpm -qa | wc -l

# check to see if any red hat rpms are installed
echo "fact: redhat_packages_gpg_is_redhat"
if [ $(rpm -qa --qf "%{DSAHEADER:pgpsig}|%{RSAHEADER:pgpsig}|%{SIGGPG:pgpsig}|%{SIGPGP:pgpsig}\n" | grep 'Key ID 199e2f91fd431d51\|Key ID 5326810137017186\|Key ID 219180cddb42a60e\|Key ID 7514f77d8366b0d9\|Key ID 45689c882fa658e0' | wc -l) -gt 0 ]; then echo "Y"; else echo "N"; fi

# gather the number of all installed red hat packages filtered by gpg keys
echo "fact: redhat_packages_gpg_num_rh_packages"
rpm -qa --qf "%{DSAHEADER:pgpsig}|%{RSAHEADER:pgpsig}|%{SIGGPG:pgpsig}|%{SIGPGP:pgpsig}\n" 2> /dev/null | grep 'Key ID 199e2f91fd431d51\|Key ID 5326810137017186\|Key ID 45689c882fa658e0\|Key ID 219180cddb42a60e\|Key ID 7514f77d8366b0d9\|Key ID 45689c882fa658e0' | wc -l

# gather the last installed red hat package filtered by gpg keys
echo "fact: redhat_packages_gpg_last_installed"
rpm -qa --qf "%{INSTALLTIME} %{DSAHEADER:pgpsig}|%{RSAHEADER:pgpsig}|%{SIGGPG:pgpsig}|%{SIGPGP:pgpsig} |%{NAME}-%{VERSION} Installed:%{INSTALLTIME:date}\n" | grep 'Key ID 199e2f91fd431d51\|Key ID 5326810137017186\|Key ID 45689c882fa658e0\|Key ID 219180cddb42a60e\|Key ID 7514f77d8366b0d9\|Key ID 45689c882fa658e0' | sort -nr | head -n 1 | cut -d"|" -f2

# gather the last built red hat package filtered by gpg keys
echo "fact: redhat_packages_gpg_last_built"
rpm -qa --qf "%{BUILDTIME} %{DSAHEADER:pgpsig}|%{RSAHEADER:pgpsig}|%{SIGGPG:pgpsig}|%{SIGPGP:pgpsig} |%{NAME}-%{VERSION} Built:%{BUILDTIME:date}\n" | grep 'Key ID 199e2f91fd431d51\|Key ID 5326810137017186\|Key ID 45689c882fa658e0\|Key ID 219180cddb42a60e\|Key ID 7514f77d8366b0d9\|Key ID 45689c882fa658e0' | sort -nr | head -n 1 | cut -d"|" -f2

# gather redhat-packages.certs fact
echo "fact: redhat_packages_certs"
ls /etc/pki/product/ /etc/pki/product-default/ 2> /dev/null |grep '.pem' | sort -u

# gather enabled repositories
echo "fact: yum_enabled_repolist"
yum repolist enabled 2> /dev/null

#check cpu model name for QEMU
echo "fact: internal_cpu_model_name_kvm"
model_name=$(cat /proc/cpuinfo 2>/dev/null | grep '^model name\s*:' | sed -n -e 's/^.*model name\s*:\s//p'); if [[ $model_name == *QEMU ]]; then echo "Y"; else echo "N"; fi

#DMI system product name
echo "facts: internal_dmi_system_product_name"
/usr/sbin/dmidecode -t system 2>/dev/null | grep "Product Name"

#test if user has sudo 
echo "fact: internal_user_has_sudo_cmd"
echo "user has sudo" 2>/dev/null

#subman facts
echo "fact: subman"
ls /etc/rhsm/facts 2>/dev/null | grep .facts | wc -l

#subman fact check
echo "fact: subman check"
rhsmcheck="ls /etc/rhsm/facts 2>/dev/null | grep .facts | wc -l"
output=$(eval "$rhsmcheck")
result=$?
if [ $result -gt 0 ]; then
	echo "pass"

#consumed SKUs from subscription manager *Command may be broken*
echo "fact: subman_consumed"
subscription-manager list --consumed 2>/dev/null | grep -e '^SKU' -e '^Subscription Name' | sed -n -e 's/SKU\s*.\s*//p' -e 's/Subscription Name\s*.\s*//p' | paste -d ' ' - - | tr '\n' ';'

#consumed cores per socket from subscription manager
echo "fact: subman_cpu_core_per_socket"
subscription-manager facts --list | grep '^cpu.core(s)_per_socket.' | sed -n -e 's/^.*cpu.core(s)_per_socket.\s*//p'

#consumed cpu's from subscription manager
echo "fact: subman_cpu_cpu"
subscription-manager facts --list | grep '^cpu.cpu(s).' | sed -n -e 's/^.*cpu.cpu(s).\s*//p'

#consumed cpu per socket from subscription manager
echo "fact: subman_cpu_cpu_socket"
subscription-manager facts --list | grep '^cpu.cpu_socket(s).' | sed -n -e 's/^.*cpu.cpu_socket(s).\s*//p'

#if subscription is active or not 
echo "fact: subman_overall_status"
LANG=C subscription-manager status | grep -e 'Overall Status:'| cut -d ":" -f2

#Virtual host type from subscription manager
echo "fact: subman_virt_host_type"
subscription-manager facts --list | grep '^virt.host_type.' | sed -n -e 's/^.*virt.host_type.\s*//p'

#Whether is a virtual guest from subscription manager
echo "fact: subman_virt_is_guest"
subscription-manager facts --list | grep '^virt.is_guest.' | sed -n -e 's/^.*virt.is_guest.\s*//p'

#Virtual host uuid from subscription manager
echo "fact: subman_virt_uuid"
subscription-manager facts --list 2>/dev/null | grep '^virt.uuid.' | sed -n -e 's/^.*virt.uuid.\s*//p'

else
	echo "fail"
fi

#JBOSS
echo "**JBOSS**"

#use find to look for jboss-modules.jar
echo "fact: find_modules.jar"
find / -xdev -type f -name jboss-modules.jar 2> /dev/null | xargs -n 1 --no-run-if-empty dirname | sort -u

#check for jboss packages
echo "fact: jboss_packages"
rpm -qa --qf "%{NAME}|%{VERSION}|%{RELEASE}|%{INSTALLTIME}|%{VENDOR}|%{BUILDTIME}|%{BUILDHOST}|%{SOURCERPM}|%{LICENSE}|%{PACKAGER}|%{INSTALLTIME:date}|%{BUILDTIME:date}\n" | grep -iE '(eap7)|(jbossas)' | sort

#gather jboss.eap.processes count
echo "fact: jboss_processes"
pgrep -af jboss | grep -v jbossfinder | wc -l

#gather jboss.eap.processes 
echo "fact: jboss_processes_list"
ps -A -o comm -o args e --columns 10000 | grep -i jboss | grep -v grep | grep -v "^jbossfinder"

#Identifies if JBoss version 4 or 5 is present
echo "fact: jboss_version45"
FOUND=""; for jar in `find / -xdev -name 'run.jar' 2>/dev/null`; do VERSION=$(java -jar ${jar} --version 2> /dev/null | grep build  | sed 's/.*[CS]V[NS]Tag.//g' | sed 's/\sdate.*//g'); inode=$(stat -c '%i' "${jar}"); fs=$(df  -T "${jar}" | tail -1 | sed 's/ .*//'); ctime=$(stat ${jar} | grep 'Change' | grep -oP '[1-2][0-9]{3}-[0-1][0-9]-[0-3][0-9]'); if [ ! -z "${VERSION}" ]; then if [ ! -z "$FOUND" ]; then FOUND="$FOUND; $VERSION**${ctime}"; else FOUND=${VERSION}'**'${ctime}; fi; fi; done; echo ${FOUND};

#Identifies if JBoss version 6 or 7 is present
echo "fact: jboss_version67"
FOUND=""; for jar in `find / -xdev -name 'jboss-modules.jar' 2>/dev/null | grep -v '\.installation/patches'`; do VERSION=$(java -jar ${jar} -version 2> /dev/null | grep version | sed 's/.*version\s//g'); inode=$(stat -c '%i' "${jar}"); fs=$(df  -T "${jar}" | grep "/dev" | sed 's/ .*//'); ctime=$(stat ${jar} | grep 'Change' | grep -oP '[1-2][0-9]{3}-[0-1][0-9]-[0-3][0-9]'); if [ ! -z "${VERSION}" ]; then if [ ! -z "$FOUND" ]; then FOUND="$FOUND; $VERSION**$ctime"; else FOUND=${VERSION}'**'${ctime}; fi; fi; done; echo -n ${FOUND} | wc -l

#Check for version 2
echo "fact: jboss_version"
FOUND=""; for jar in `find /jboss /app /eap /opt /appserver -xdev -name 'jboss-modules.jar' 2>/dev/null | grep -v '\.installation/patches'`; do VERSION=$(java -jar ${jar} -version 2> /dev/null | grep version | sed 's/.*version\s//g'); inode=$(stat -c '%i' "${jar}"); fs=$(df  -T "${jar}" | grep "/dev" | sed 's/ .*//'); ctime=$(stat ${jar} | grep 'Change' | grep -oP '[1-2][0-9]{3}-[0-1][0-9]-[0-3][0-9]'); if [ ! -z "${VERSION}" ]; then if [ ! -z "$FOUND" ]; then FOUND="$FOUND; $VERSION**$ctime"; else FOUND=${VERSION}'**'${ctime}; fi; fi; done; echo ${FOUND}

# Identifies if JBoss version 8 is present
echo "fact: jboss_version8"
FOUND=""; for jar in `find / -xdev -name 'jboss-modules.jar' 2>/dev/null | grep -v '\.installation/patches'`; do VERSION=""; JBOSS_HOME=$(dirname "${jar}"); MF="${JBOSS_HOME}/modules/system/layers/base/org/jboss/as/product/eap/dir/META-INF/MANIFEST.MF"; if [ -f "${MF}" ]; then VERSION=$(grep -E '^JBoss-Product-Release-Version:' "${MF}" 2>/dev/null | head -n 1 | sed 's/^JBoss-Product-Release-Version:\s*//'); ctime=$(stat ${MF} | grep 'Change' | grep -oP '[1-2][0-9]{3}-[0-1][0-9]-[0-3][0-9]'); else VERSION=$(java -jar ${jar} -version 2> /dev/null | grep version | sed 's/.*version\s//g'); ctime=$(stat ${jar} | grep 'Change' | grep -oP '[1-2][0-9]{3}-[0-1][0-9]-[0-3][0-9]'); fi; inode=$(stat -c '%i' "${jar}"); fs=$(df -T "${jar}" | grep "/dev" | sed 's/ .*//'); if [ ! -z "${VERSION}" ]; then if echo "${VERSION}" | grep -qE '(^8(\.|$)|(^8\.)|([[:space:]]8\.)|(^8-)|(^8_)|(^8.*GA)|(^8.*redhat)|(^8.*Final))'; then FOUND="1"; break; fi; fi; done; if [ "$FOUND" = "1" ]; then echo 1; else echo 0; fi 


#Hyperthreading is enabled on physical server
#cat /sys/devices/system/cpu/smt/control

