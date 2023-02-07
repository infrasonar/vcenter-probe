from libprobe.asset import Asset
from ..vmwarequery import vmwarequery_content


async def check_system(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:
    content = await vmwarequery_content(
        asset,
        asset_config,
        check_config,
    )
    about = content.about

    system = [
        # vim.AboutInfo
        {
            'apiType': about.apiType,
            'apiVersion': about.apiVersion,
            'build': about.build,
            'fullName': about.fullName,
            'instanceUuid': about.instanceUuid,
            'licenseProductName': about.licenseProductName,
            'licenseProductVersion': about.licenseProductVersion,
            'localeBuild': about.localeBuild,
            'localeVersion': about.localeVersion,
            'name': about.name,  # str
            'osType': about.osType,
            'productLineId': about.productLineId,
            'version': about.version,  # str
        }
    ]

    return {
        'system': system
    }
