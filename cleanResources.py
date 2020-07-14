import oci
import sys, getopt
from ResourceModules.IAM import *
from ResourceModules.Instances import *
from ResourceModules.Autoscaling import *
from ResourceModules.BlockStorage import *

########## Configuration ####################
# Specify your config file location
config_file_path = r"C:\Users\SQREDDY\.oci\conf_national02"

# Specify the DEFAULT compartment OCID that you want to delete, Leave Empty for no default
startcomp = "ocid1.compartment.oc1..aaaaaaaallv5ilbokc7lom5jynp5dxaf7kurhakrval3wzjpwsnff2ymx5kq"
#############################################

try:
    opts, args = getopt.getopt(sys.argv[1:], "c:", ["compid="])
except getopt.GetoptError:
    print ("cleanResources.py -c <compartmentID>")
    sys.exit(2)

for opt, arg in opts:
    print ("{} - {}".format(opt,arg))
    if opt == "-c":
        startcomp = arg

if startcomp =="":
    print ("No compartment specified")
    sys.exit(2)


config = oci.config.from_file(config_file_path)

# startcomp="ocid1.compartment.oc1..aaaaaaaallv5ilbokc7lom5jynp5dxaf7kurhakrval3wzjpwsnff2ymx5kq"

print ("\n--[ Login check and getting all compartments from root compartment ]--")
compartments = Login(config,startcomp)
#calling SubscribedRegions() function
regions=SubscribedRegions(config)
processCompartments=[]

print ("\n--[ Compartments to process ]--")

# Add all active compartments, but exclude the ManagementCompartmentForPaas (as this is locked compartment)
for compartment in compartments:
    if compartment.lifecycle_state== "ACTIVE" and compartment.name != "ManagedCompartmentForPaaS":
        processCompartments.append(compartment)
        print (compartment.name)

for region in regions:
    config["region"]=region

    print ("\n--[ Deleting Auto Scaling Configurations ]--")
    DeleteAutoScalingConfigurations(config, processCompartments)

    print ("\n--[ Deleting Compute Instances ]--")
    DeleteInstancePools(config,processCompartments)
    DeleteInstanceConfigs(config, processCompartments)
    DeleteInstances(config,processCompartments)
    DeleteImages(config, processCompartments)
    DeleteBootVolumes(config, processCompartments)
    DeleteBootVolumesBackups(config, processCompartments)
    DeleteDedicatedVMHosts(config, processCompartments)

    print ("\n--[ Deleting Block Volumes ]--")
    DeleteVolumeGroups(config, processCompartments)
    DeleteVolumeGroupBackups(config, processCompartments)
    DeleteVolumes(config, processCompartments)
    DeleteBlockVolumesBackups(config, processCompartments)