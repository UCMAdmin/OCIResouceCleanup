import oci
import time
from datetime import datetime as dt
TODAY=dt.today()

WaitRefresh = 15


def DeleteBootVolumes(config, Compartments):
    properlyTaggedItems = []
    improperlyTaggedItems = []
    object = oci.core.BlockstorageClient(config)
    identity = oci.identity.IdentityClient(config)

    print ("Getting all Blockstorage objects")
    for compartment in Compartments:
        ads = identity.list_availability_domains(compartment_id=compartment.id).data
        for ad in ads:
            items = oci.pagination.list_call_get_all_results(object.list_boot_volumes, availability_domain=ad.name, compartment_id=compartment.id).data
            for item in items:
                if item.lifecycle_state != "TERMINATED":
                    try:
                        date_in_string=item.defined_tags["ExpirationTag"]["ExpirationDate(dd/mm/yyyy)"]
                        date_in_date=dt.strptime(date_in_string, "%d/%m/%Y")
                        if date_in_date<TODAY:
                            properlyTaggedItems.append(item)
                            print("- {} - {}".format(item.display_name, item.lifecycle_state))
                    except:
                        improperlyTaggedItems.append(item)
    itemsPresent = True

    while itemsPresent:
        count = 0
        for item in properlyTaggedItems:
            try:
                itemstatus = object.get_boot_volume(boot_volume_id=item.id).data
                if itemstatus.lifecycle_state != "TERMINATED":
                    if itemstatus.lifecycle_state != "TERMINATING":
                        try:
                            print("Deleting: {}".format(itemstatus.display_name))
                            object.delete_boot_volume(boot_volume_id=itemstatus.id)
                        except:
                            print("error trying to delete: {}".format(itemstatus.display_name))
                    else:
                        print("{} = {}".format(itemstatus.display_name, itemstatus.lifecycle_state))
                    count = count + 1
            except:
                print("error deleting {}, probably already deleted".format(item.display_name))
        if count > 0:
            print("Waiting for all Objects to be deleted...")
            time.sleep(WaitRefresh)
        else:
            itemsPresent = False
    print("All expired Objects deleted!")
    if improperlyTaggedItems:
        print("\n--Check the following improperly tagged resources--\n")
        for item in improperlyTaggedItems:
            print("{} = {}".format(item.display_name, item.lifecycle_state))    

def DeleteBlockVolumesBackups(config, Compartments):
    properlyTaggedItems = []
    improperlyTaggedItems = []
    object = oci.core.BlockstorageClient(config)
    identity = oci.identity.IdentityClient(config)

    print ("Getting all Block Volumes Backup objects")
    for compartment in Compartments:
        items = oci.pagination.list_call_get_all_results(object.list_volume_backups, compartment_id=compartment.id).data
        for item in items:
            if (item.lifecycle_state != "TERMINATED"):
                try:
                    date_in_string=item.defined_tags["ExpirationTag"]["ExpirationDate(dd/mm/yyyy)"]
                    date_in_date=dt.strptime(date_in_string, "%d/%m/%Y")
                    if date_in_date<TODAY:
                        properlyTaggedItems.append(item)
                        print("- {} - {}".format(item.display_name, item.lifecycle_state))
                except:
                    improperlyTaggedItems.append(item)

    itemsPresent = True

    while itemsPresent:
        count = 0
        for item in properlyTaggedItems:
            try:
                itemstatus = object.get_volume_backup(volume_backup_id=item.id).data
                if itemstatus.lifecycle_state != "TERMINATED":
                    if itemstatus.lifecycle_state != "TERMINATING":
                        try:
                            print("Deleting: {}".format(itemstatus.display_name))
                            object.delete_volume_backup(volume_backup_id=itemstatus.id)
                        except:
                            print("error trying to delete: {}".format(itemstatus.display_name))
                    else:
                        print("{} = {}".format(itemstatus.display_name, itemstatus.lifecycle_state))
                    count = count + 1
            except:
                print("error deleting {}, probably already deleted".format(item.display_name))
        if count > 0:
            print("Waiting for all Objects to be deleted...")
            time.sleep(WaitRefresh)
        else:
            itemsPresent = False
    print ("All expired Objects deleted!")
    if improperlyTaggedItems:
        print("\n--Check the following improperly tagged resources--\n")
        for item in improperlyTaggedItems:
            print("{} = {}".format(item.display_name, item.lifecycle_state))


def DeleteBootVolumesBackups(config, Compartments):
    properlyTaggedItems = []
    improperlyTaggedItems = []
    object = oci.core.BlockstorageClient(config)
    identity = oci.identity.IdentityClient(config)

    print ("Getting all Boot Volumes Backup objects")
    for compartment in Compartments:
        items = oci.pagination.list_call_get_all_results(object.list_boot_volume_backups, compartment_id=compartment.id).data
        for item in items:
            if (item.lifecycle_state != "TERMINATED"):
                try:
                    date_in_string=item.defined_tags["ExpirationTag"]["ExpirationDate(dd/mm/yyyy)"]
                    date_in_date=dt.strptime(date_in_string, "%d/%m/%Y")
                    if date_in_date<TODAY:
                        properlyTaggedItems.append(item)
                        print("- {} - {}".format(item.display_name, item.lifecycle_state))
                except:
                    improperlyTaggedItems.append(item)

    itemsPresent = True

    while itemsPresent:
        count = 0
        for item in properlyTaggedItems:
            try:
                itemstatus = object.get_boot_volume_backup(boot_volume_backup_id=item.id).data
                if itemstatus.lifecycle_state != "TERMINATED":
                    if itemstatus.lifecycle_state != "TERMINATING":
                        try:
                            print("Deleting: {}".format(itemstatus.display_name))
                            object.delete_boot_volume_backup(boot_volume_backup_id=itemstatus.id)
                        except:
                            print("error trying to delete: {}".format(itemstatus.display_name))
                    else:
                        print("{} = {}".format(itemstatus.display_name, itemstatus.lifecycle_state))
                    count = count + 1
            except:
                print("error deleting {}, probably already deleted".format(item.display_name))
        if count > 0:
            print("Waiting for all Objects to be deleted...")
            time.sleep(WaitRefresh)
        else:
            itemsPresent = False
    print ("All expired Objects deleted!")
    if improperlyTaggedItems:
        print("\n--Check the following improperly tagged resources--\n")
        for item in improperlyTaggedItems:
            print("{} = {}".format(item.display_name, item.lifecycle_state))
    
    
def DeleteVolumeGroups(config, Compartments):
    properlyTaggedItems = []
    improperlyTaggedItems = []
    object = oci.core.BlockstorageClient(config)
    identity = oci.identity.IdentityClient(config)

    print ("Getting all Block Volume Groups objects")
    for compartment in Compartments:
        ads = identity.list_availability_domains(compartment_id=compartment.id).data
        for ad in ads:
            items = oci.pagination.list_call_get_all_results(object.list_volume_groups, availability_domain=ad.name, compartment_id=compartment.id).data
            for item in items:
                if (item.lifecycle_state != "TERMINATED"):
                    try:
                        date_in_string=item.defined_tags["ExpirationTag"]["ExpirationDate(dd/mm/yyyy)"]
                        date_in_date=dt.strptime(date_in_string, "%d/%m/%Y")
                        if date_in_date<TODAY:
                            properlyTaggedItems.append(item)
                            print("- {} - {}".format(item.display_name, item.lifecycle_state))
                    except:
                        improperlyTaggedItems.append(item)

    itemsPresent = True

    while itemsPresent:
        count = 0
        for item in properlyTaggedItems:
            try:
                itemstatus = object.get_volume_group(volume_group_id=item.id).data
                if itemstatus.lifecycle_state != "TERMINATED":
                    if itemstatus.lifecycle_state != "TERMINATING":
                        try:
                            print("Deleting: {}".format(itemstatus.display_name))
                            object.delete_volume_group(volume_group_id=itemstatus.id)
                        except:
                            print("error trying to delete: {}".format(itemstatus.display_name))
                    else:
                        print("{} = {}".format(itemstatus.display_name, itemstatus.lifecycle_state))
                    count = count + 1
            except:
                print("error deleting {}, probably already deleted".format(item.display_name))
        if count > 0:
            print("Waiting for all Objects to be deleted...")
            time.sleep(WaitRefresh)
        else:
            itemsPresent = False
    print ("All expired Objects deleted!")
    if improperlyTaggedItems:
        print("\n--Check the following improperly tagged resources--\n")
        for item in improperlyTaggedItems:
            print("{} = {}".format(item.display_name, item.lifecycle_state))

def DeleteVolumeGroupBackups(config, Compartments):
    properlyTaggedItems = []
    improperlyTaggedItems = []
    object = oci.core.BlockstorageClient(config)
    identity = oci.identity.IdentityClient(config)

    print ("Getting all Block Volume Group Backups objects")
    for compartment in Compartments:
        items = oci.pagination.list_call_get_all_results(object.list_volume_group_backups, compartment_id=compartment.id).data
        for item in items:
            if (item.lifecycle_state != "TERMINATED"):
                try:
                    date_in_string=item.defined_tags["ExpirationTag"]["ExpirationDate(dd/mm/yyyy)"]
                    date_in_date=dt.strptime(date_in_string, "%d/%m/%Y")
                    if date_in_date<TODAY:
                        properlyTaggedItems.append(item)
                        print("- {} - {}".format(item.display_name, item.lifecycle_state))
                except:
                    improperlyTaggedItems.append(item)

    itemsPresent = True

    while itemsPresent:
        count = 0
        for item in properlyTaggedItems:
            try:
                itemstatus = object.get_volume_group_backup(volume_group_backup_id=item.id).data
                if itemstatus.lifecycle_state != "TERMINATED":
                    if itemstatus.lifecycle_state != "TERMINATING":
                        try:
                            print("Deleting: {}".format(itemstatus.display_name))
                            object.delete_volume_group_backup(volume_group_backup_id=itemstatus.id)
                        except:
                            print("error trying to delete: {}".format(itemstatus.display_name))
                    else:
                        print("{} = {}".format(itemstatus.display_name, itemstatus.lifecycle_state))
                    count = count + 1
            except:
                print("error deleting {}, probably already deleted".format(item.display_name))
        if count > 0:
            print("Waiting for all Objects to be deleted...")
            time.sleep(WaitRefresh)
        else:
            itemsPresent = False
    print ("All expired Objects deleted!")
    if improperlyTaggedItems:
        print("\n--Check the following improperly tagged resources--\n")
        for item in improperlyTaggedItems:
            print("{} = {}".format(item.display_name, item.lifecycle_state))