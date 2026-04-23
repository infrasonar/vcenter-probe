from libprobe.asset import Asset
from libprobe.check import Check
from ..vmwarequery import vmwarequery_content


class CheckSystem(Check):
    key = 'system'
    unchanged_eol = 14400

    @staticmethod
    async def run(asset: Asset, local_config: dict, config: dict) -> dict:

        content = await vmwarequery_content(
            asset,
            local_config,
            config,
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
