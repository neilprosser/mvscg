import commands
import httplib
import json
import sys
import time
import urllib

if len(sys.argv) != 5:
    sys.stderr.write('Not enough arguments\n')
    sys.exit(1)

environment = sys.argv[1].lower()
service_name = sys.argv[2].lower()
prefix = "%s.%s" % (environment, service_name)

host = sys.argv[3]
port = sys.argv[4]

timestamp_millis = int(round(time.time() * 1000))
timestamp = timestamp_millis / 1000
connection = httplib.HTTPConnection(host, port, timeout = 1)

def tidy_up():
    connection.close()

try:
    connection.request('GET', '/exhibitor/v1/explorer/node-data?key=%2Flive%2Fservices%2Fsolr%2Fclusterstate.json')
except:
    sys.stderr.write('Unable to connect when obtaining cluster state\n')
    sys.exit(1)

zookeeper_response = connection.getresponse()
zookeeper_content = zookeeper_response.read()
zookeeper_json = json.loads(zookeeper_content)
state_json = json.loads(zookeeper_json['str'])

shards = state_json['items']['shards']

for shard_name in shards:
    shard = shards[shard_name]
    replicas = shard['replicas']
    for replica_host in replicas:
        host = replica_host.split('.', 1)[0]
        replica = replicas[replica_host]
        state = replica['state'].replace(' ', '_')
        print "%s.%s.%s.state.active %d %d" % (prefix, host, shard_name, 1 if state == 'active' else 0, timestamp)
        print "%s.%s.%s.state.recovering %d %d" % (prefix, host, shard_name, 1 if state == 'recovering' else 0, timestamp)
        print "%s.%s.%s.state.down %d %d" % (prefix, host, shard_name, 1 if state == 'down' else 0, timestamp)
        print "%s.%s.%s.state.recovery_failed %d %d" % (prefix, host, shard_name, 1 if state == 'recovery_failed' else 0, timestamp)
        print "%s.%s.%s.state.gone %d %d" % (prefix, host, shard_name, 1 if state == 'gone' else 0, timestamp)
        if replica.has_key('leader'):
            print "%s.%s.%s.state.leader 1  %d" % (prefix, host, shard_name, timestamp)
        else:
            print "%s.%s.%s.state.leader 0 %d" % (prefix, host, shard_name, timestamp)

tidy_up()