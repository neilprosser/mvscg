#!/bin/bash
#
# Use me like this:
# /path/to/me.sh | nc -w 20 {graphite_host} {graphite_port}
#
#script=`readlink -f $0`
#path=`dirname $script`
#environment="<%= @esd_env %>"
#service_name="<%= @service_name %>"
#host="localhost"
#port="<%= @port %>"

#python $path/mvsg.py $environment $service_name $host $port

python /Users/neil/development/mvscg/mvscg.py live alternativesolr neil-beast.mobile.lnx.nokia.com 80