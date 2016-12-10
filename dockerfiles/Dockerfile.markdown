FROM tinylab/cloud-ubuntu-dev_cn_input
MAINTAINER Wu Zhangjin <wuzhangjin@gmail.com>

ENV DEBIAN_FRONTEND noninteractive
ENV HOME /home/ubuntu/

# RUN sed -i -e "s%mirrors.linode.com%cn.archive.ubuntu.com%g" /etc/apt/sources.list

RUN apt-get -y update

# For Slides, Resume and Article
RUN apt-get install -y --force-yes --no-install-recommends \
	pandoc \
    && apt-get autoclean -y \
    && apt-get autoremove -y \
    && rm -rf /var/cache/apt/archives/*.deb

RUN apt-get install -y --force-yes --no-install-recommends \
	texlive-xetex \
    && apt-get autoclean -y \
    && apt-get autoremove -y \
    && rm -rf /var/cache/apt/archives/*.deb

# RUN apt-get install -y --force-yes --no-install-recommends \
#	texlive-latex-recommended \
#    && apt-get autoclean -y \
#    && apt-get autoremove -y \
#    && rm -rf /var/cache/apt/archives/*.deb

RUN apt-get install -y --force-yes --no-install-recommends \
	texlive-latex-extra \
    && apt-get autoclean -y \
    && apt-get autoremove -y \
    && rm -rf /var/cache/apt/archives/*.deb

RUN apt-get install -y --force-yes --no-install-recommends \
	texlive-fonts-recommended \
    && apt-get autoclean -y \
    && apt-get autoremove -y \
    && rm -rf /var/cache/apt/archives/*.deb

# RUN apt-get install -y --force-yes --no-install-recommends \
#	texlive-fonts-extra \
#    && apt-get autoclean -y \
#    && apt-get autoremove -y \
#    && rm -rf /var/cache/apt/archives/*.deb

RUN apt-get install -y --force-yes --no-install-recommends \
	lmodern \
    && apt-get autoclean -y \
    && apt-get autoremove -y \
    && rm -rf /var/cache/apt/archives/*.deb

RUN apt-get install -y --force-yes --no-install-recommends \
	latex-cjk-common latex-cjk-chinese \
    && apt-get autoclean -y \
    && apt-get autoremove -y \
    && rm -rf /var/cache/apt/archives/*.deb

RUN apt-get install -y --force-yes --no-install-recommends \
	latex-cjk-chinese-arphic-bkai00mp latex-cjk-chinese-arphic-bsmi00lp \
	latex-cjk-chinese-arphic-gbsn00lp latex-cjk-chinese-arphic-gkai00mp \
    && apt-get autoclean -y \
    && apt-get autoremove -y \
    && rm -rf /var/cache/apt/archives/*.deb

RUN apt-get install -y --force-yes --no-install-recommends \
	latex-beamer \
    && apt-get autoclean -y \
    && apt-get autoremove -y \
    && rm -rf /var/cache/apt/archives/*.deb

# For gitbook
RUN apt-get install -y --force-yes --no-install-recommends \
	calibre \
    && apt-get autoclean -y \
    && apt-get autoremove -y \
    && rm -rf /var/cache/apt/archives/*.deb

RUN apt-get install -y --force-yes --no-install-recommends \
	nodejs npm \
    && apt-get autoclean -y \
    && apt-get autoremove -y \
    && rm -rf /var/cache/apt/archives/*.deb

# RUN npm config set registry https://registry.npm.taobao.org/
# RUN npm config set registry http://npmreg.mirrors.ustc.edu.cn/

RUN export npm_config_cache=$(mktemp -d) \
    && npm install gitbook-cli -g \
    && npm cache clean \
    && rm -rf /tmp/* \
    && rm /usr/local/bin/gitbook \
    && sh -c 'echo "nodejs /usr/local/lib/node_modules/gitbook-cli/bin/gitbook.js \$@" > /usr/local/bin/gitbook' \
    && chmod +x /usr/local/bin/gitbook

RUN export npm_config_cache=$(mktemp -d) \
    && npm install gitbook-plugin-duoshuo -g \
    && npm install gitbook-plugin-disqus -g \
    && npm install gitbook-plugin-google_code_prettify -g \
    && npm install gitbook-plugin-collapsible-menu -g \
    && npm install gitbook-plugin-maxiang -g \
    && npm install gitbook-plugin-multipart -g \
    && npm cache clean \
    && rm -rf /tmp/*

# RUN export npm_config_cache=$(mktemp -d) \
#    && gitbook fetch latest \
#    && npm cache clean \
#    && rm -rf /tmp/*
# ...

RUN rm -rf /var/lib/apt/lists/*

# RUN sed -i -e "s%cn.archive.ubuntu.com%mirrors.linode.com%g" /etc/apt/sources.list

EXPOSE 5900 22

WORKDIR /

ENTRYPOINT ["/startup.sh"]
