source /etc/skel/.bashrc

# For Chinese input support
dpkg -l | grep -q ibus-sunpinyin
if [ $? -eq 0 ]; then
	export LANG=en_US.UTF-8
	export LANGUAGE=en_US
	export LC_CTYPE=zh_CN.UTF-8
	export LC_NUMERIC=zh_CN.UTF-8
	export LC_TIME=zh_CN.UTF-8
	export LC_COLLATE=zh_CN.UTF-8
	export LC_MONETARY=zh_CN.UTF-8
	export LC_MESSAGES=zh_CN.UTF-8
	export LC_PAPER=zh_CN.UTF-8
	export LC_NAME=zh_CN.UTF-8
	export LC_ADDRESS=zh_CN.UTF-8
	export LC_TELEPHONE=zh_CN.UTF-8
	export LC_MEASUREMENT=zh_CN.UTF-8
	export LC_IDENTIFICATION=zh_CN.UTF-8
	export LC_ALL=
fi
