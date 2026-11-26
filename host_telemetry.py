"""Local host telemetry; no remote execution or credential collection."""
import platform
import socket
import time
from datetime import datetime, timezone
import psutil

def snapshot(user_id, team_id, expected_team, administrators, metrics=psutil):
    if not expected_team or team_id != expected_team or not user_id or user_id == '*' or user_id not in administrators:
        raise PermissionError('Host intelligence requires administrator authorization')
    memory = metrics.virtual_memory()
    disks = []
    for partition in metrics.disk_partitions(all=False):
        try:
            usage = metrics.disk_usage(partition.mountpoint)
            disks.append({'mount':partition.mountpoint,'total':usage.total,'used':usage.used,'percent':usage.percent})
        except OSError:
            disks.append({'mount':partition.mountpoint,'unavailable':True})
    interfaces = [{'name':name,'up':stats.isup,'speed_mbps':stats.speed}
                  for name,stats in metrics.net_if_stats().items()]
    processes = []
    for process in metrics.process_iter(['pid','name']):
        try:
            processes.append({'pid':process.info['pid'],'name':process.info['name']})
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
        if len(processes) >= 100:
            break
    return {'host':socket.gethostname(),'os':platform.system(),'version':platform.release(),
            'captured_at':datetime.now(timezone.utc).isoformat(),
            'cpu_percent':metrics.cpu_percent(interval=0.2),'logical_cpus':metrics.cpu_count(),
            'memory':{'total':memory.total,'available':memory.available,'percent':memory.percent},
            'uptime_seconds':max(0,int(time.time()-metrics.boot_time())),
            'disks':disks,'interfaces':interfaces,'processes':processes,
            'process_limit':100}
