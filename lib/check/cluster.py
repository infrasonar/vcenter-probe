from libprobe.asset import Asset
from libprobe.exceptions import IgnoreCheckException
from pyVmomi import vim  # type: ignore
from ..vmwarequery import vmwarequery


def on_cluster_summary(obj):
    # vim.ClusterComputeResource.Summary
    return {
        'currentBalance': obj.currentBalance,  # int
        'currentEVCModeKey': obj.currentEVCModeKey,  # str
        'currentFailoverLevel': obj.currentFailoverLevel,  # int
        'numVmotions': obj.numVmotions,  # int
        'targetBalance': obj.targetBalance,  # int
    }


def on_about_info(obj):
    # vim.AboutInfo
    return {
        'apiType': obj.apiType,  # str
        'apiVersion': obj.apiVersion,  # str
        'build': obj.build,  # str
        'fullName': obj.fullName,  # str
        'instanceUuid': obj.instanceUuid,  # str
        'licenseProductName': obj.licenseProductName,  # str
        'licenseProductVersion': obj.licenseProductVersion,  # str
        'localeBuild': obj.localeBuild,  # str
        'localeVersion': obj.localeVersion,  # str
        # 'name': obj.name,  # str
        'osType': obj.osType,  # str
        'patchLevel': obj.patchLevel,  # str
        'productLineId': obj.productLineId,  # int
        'vendor': obj.vendor,  # str
        'version': obj.version,  # str
    }


def on_config_summary(obj):
    # vim.host.Summary.ConfigSummary
    return {
        'faultToleranceEnabled': obj.faultToleranceEnabled,  # bool
        # 'name': obj.name,  # str
        'port': obj.port,  # int
        'sslThumbprint': obj.sslThumbprint,  # int/null
        'vmotionEnabled': obj.vmotionEnabled,  # int
    }


def on_host_summary(obj):
    # vim.host.Summary
    return {
        'currentEVCGraphicsModeKey': obj.currentEVCGraphicsModeKey,  # str
        'currentEVCModeKey': obj.currentEVCModeKey,  # str
        'managementServerIp': obj.managementServerIp,  # str
        'maxEVCModeKey': obj.maxEVCModeKey,  # str
        'overallStatus': obj.overallStatus,  # str
        'rebootRequired': obj.rebootRequired,  # bool
    }


async def check_cluster(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:
    clusters_ = await vmwarequery(
        asset,
        asset_config,
        check_config,
        vim.ClusterComputeResource,
        ['summary', 'host'],
    )
    if len(clusters_) == 0:
        raise IgnoreCheckException

    hosts_ = await vmwarequery(
        asset,
        asset_config,
        check_config,
        vim.HostSystem,
        ['name', 'summary'],
    )
    clusters_lookup = {
        c.obj: {p.name: p.val for p in c.propSet} for c in clusters_}
    hosts_lookup = {
        h.obj: {p.name: p.val for p in h.propSet} for h in hosts_}
    summary = []
    hosts = []

    for moref, cluster in clusters_lookup.items():
        cluster_name = f'{moref.parent.parent.name}-{moref.name}'
        cluster_dct = on_cluster_summary(cluster['summary'])
        cluster_dct['name'] = cluster_name
        summary.append(cluster_dct)

        for host_moref in cluster['host']:
            host = hosts_lookup.get(host_moref)
            if host is None:
                continue

            host_dct = {
                **on_host_summary(host['summary']),
                **on_config_summary(host['summary'].config),
                **on_about_info(host['summary'].config.product),
                'productName': host['summary'].config.product.name,
                'clusterName': cluster_name,
                'name': host['name'],
            }
            hosts.append(host_dct)

    return {
        'cluster': summary,
        'hosts': hosts
    }
