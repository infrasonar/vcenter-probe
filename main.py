from libprobe.probe import Probe
from lib.check.alarms import CheckAlarms
from lib.check.config_issues import CheckConfigIssues
from lib.check.cluster import CheckCluster
from lib.check.datastore import CheckDatastore
from lib.check.host_vms import CheckHostVMs
from lib.check.licenses import CheckLicenses
from lib.check.system import CheckSystem
from lib.version import __version__ as version


if __name__ == '__main__':
    checks = (
        CheckAlarms,
        CheckConfigIssues,
        CheckCluster,  # optional
        CheckDatastore,
        CheckHostVMs,
        CheckLicenses,
        CheckSystem,
    )

    probe = Probe("vcenter", version, checks)

    probe.start()
