from libprobe.asset import Asset
from pyVmomi import vim  # type: ignore
from ..utils import datetime_to_timestamp
from ..vmwarequery import vmwarequery


async def check_alarms(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:
    result = await vmwarequery(
        asset,
        asset_config,
        check_config,
        vim.HostSystem,
        ['triggeredAlarmState'],
    )

    alarms = [
        {
            'name': str(alarm.key),
            'entityName': alarm.entity.name,
            'alarmInfo': alarm.alarm.info.name,
            'alarmDesc': alarm.alarm.info.description,
            'acknowledged': alarm.acknowledged,
            'acknowledgedByUser': alarm.acknowledgedByUser,
            'acknowledgedTime': datetime_to_timestamp(alarm.acknowledgedTime),
            'eventKey': alarm.eventKey,
            'overallStatus': alarm.overallStatus,
            'time': datetime_to_timestamp(alarm.time),
        }
        for item in result
        for prop in item.propSet
        for alarm in prop.val
    ]

    return {
        'alarms': alarms
    }
