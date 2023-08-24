import logging
from libprobe.asset import Asset
from pyVmomi import vim  # type: ignore
from ..vmwarequery import vmwarequery


async def check_host_vms(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:

    stores_ = await vmwarequery(
        asset,
        asset_config,
        check_config,
        vim.Datastore,
        ['name', 'summary.capacity'],
    )

    vms_ = await vmwarequery(
        asset,
        asset_config,
        check_config,
        vim.VirtualMachine,
        ['name', 'config', 'guest', 'runtime'],
    )

    stores_lookup = {
        store.obj: {p.name: p.val for p in store.propSet} for store in stores_}
    vms_retrieved = {
        vm.obj: {p.name: p.val for p in vm.propSet} for vm in vms_}

    guests = []
    running_guest_count = 0
    for moref, vm in vms_retrieved.items():
        if 'config' not in vm:
            logging.info(
                f'Skipping VM {vm} because it is missing config data'
            )
            continue
        if vm['config'].template:
            continue

        guests.append({
            'name': vm['config'].instanceUuid,
            'instanceName': vm['name'],
            'powerState': vm['runtime'].powerState,
            'currentHypervisor':
                # vm.runtime.host is empty when vm is off
                vm['runtime'].host and vm['runtime'].host.name,
        })

        if vm['guest'].guestState == 'running':
            running_guest_count += 1

        for device in vm['config'].hardware.device:
            if isinstance(device, vim.vm.device.VirtualDisk):
                datastore = stores_lookup[device.backing.datastore]
                if 'virtualCapacity' not in datastore:
                    datastore['virtualCapacity'] = 0
                datastore['virtualCapacity'] += device.capacityInBytes

    guest_count = [{
        'name': 'guestCount',
        'guestCount': len(guests),
        'runningGuestCount': running_guest_count
    }]
    virtual_storage = [{
        'name': ds['name'],
        'virtualCapacity': ds['virtualCapacity'],
        'actualCapacity': ds['summary.capacity']
    } for ds in stores_lookup.values()]

    return {
        'guests': guests,
        'guestCount': guest_count,
        'virtualStorage': virtual_storage,
    }
