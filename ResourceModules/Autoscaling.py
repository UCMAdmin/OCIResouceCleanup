import oci
import time
from datetime import datetime as dt
TODAY=dt.today()

WaitRefresh = 15

def DeleteAutoScalingConfigurations(config, Compartments):
    properlyTaggedItems = []
    improperlyTaggedItems = []
    object = oci.autoscaling.AutoScalingClient(config)

    print ("\nGetting all Autoscaling configurations")
    for Compartment in Compartments:
        items = oci.pagination.list_call_get_all_results(object.list_auto_scaling_configurations, compartment_id=Compartment.id).data
        for item in items:
            try:
                date_in_string=item.defined_tags["ExpirationTag"]["ExpirationDate(dd/mm/yyyy)"]
                date_in_date=dt.strptime(date_in_string, "%d/%m/%Y")
                if date_in_date<TODAY:                
                    properlyTaggedItems.append(item)
                    print("- {}".format(item.display_name))
            except:
                improperlyTaggedItems.append(item)

    for item in properlyTaggedItems:
        print("deleting - {}".format(item.display_name))
        object.delete_auto_scaling_configuration(auto_scaling_configuration_id=item.id)

    print ("All expired Objects deleted!")
    if improperlyTaggedItems:
        print("\n--Check the following improperly tagged resources--\n")
        for item in improperlyTaggedItems:
            print("{}".format(item.display_name))