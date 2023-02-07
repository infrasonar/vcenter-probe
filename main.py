from libprobe.probe import Probe
from lib.check.alarms import check_alarms
from lib.check.config_issues import check_config_issues
from lib.check.cluster import check_cluster
from lib.check.datastore import check_datastore
from lib.check.host_vms import check_host_vms
from lib.check.licenses import check_licenses
from lib.check.system import check_system
from lib.version import __version__ as version


if __name__ == '__main__':
    checks = {
        'alarms': check_alarms,
        'cluster': check_cluster,  # optional
        'configIssues': check_config_issues,
        'datastore': check_datastore,
        'hostVMs': check_host_vms,
        'licenses': check_licenses,
        'system': check_system,
    }

    probe = Probe("vcenter", version, checks)

    probe.start()
