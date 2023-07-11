getip() {
	__interface=$1
	ip=$(ifconfig  $__interface| grep -oE 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -oE '([0-9]*\.){3}[0-9]*')
}

getmac() {
	__interface=$1
	mac=$(ifconfig $__interface | grep -oE '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}')
}

getuuid() {
	getip eth0
	getmac eth0
	cpu=$(cat /proc/cpuinfo | grep 'model name' |head -n1| awk -F': ' '{ print $2 }')
	name=$(uname -a)
	uuid=$(echo -en "ip:$ip,mac:$mac,cpu:$cpu,name:$name" | md5sum | awk -F' ' '{ print $1 }' )
}

# $1: report title
# $2: report url
report() {
	title=$1
	url=$2
	getip eth0
	getmac eth0
	getuuid
	mem=`top -n 1|head -n10 | grep "Mem:"`
	cpu=`top -n 1|head -n10 | grep "CPU:"`
	load=`uptime`
	tm=`date`
	#TODO add private key report
	info="{\"title\":\"$title\",\"ip\":\"$ip\",\"mac\":\"$mac\",\"devid\":\"$uuid\",\"mem\":\"$mem\",\"cpu\":\"$cpu\",\"load\":\"$load\",\"date\":\"$tm\"}"
	ret=`wget -q -U "$info" $url -O -`
	#TODO process ret
}

while true
do
	report "somedevice" "http://192.168.1.11:5050/v1/report"
	sleep 10
done

