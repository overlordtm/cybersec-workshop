# Old OpenSSH (7.4p1, Debian 9) for the version -> CVE exercise (e.g. CVE-2018-15473 user enumeration)
FROM debian:stretch-slim
RUN printf 'deb http://archive.debian.org/debian stretch main\n' > /etc/apt/sources.list \
 && apt-get -o Acquire::Check-Valid-Until=false update \
 && apt-get install -y --no-install-recommends openssh-server \
 && rm -rf /var/lib/apt/lists/* && mkdir -p /run/sshd \
 && useradd -m -s /bin/bash peter.horvat && echo 'peter.horvat:Poletje2019!' | chpasswd \
 && printf 'Banner /etc/issue.net\nPermitRootLogin no\n' >> /etc/ssh/sshd_config \
 && printf 'ACME oddaljeni dostop - samo za zaposlene.\n' > /etc/issue.net
CMD ["/usr/sbin/sshd", "-D", "-e"]
