"""
Usage:
    $SCHRODINGER/run set_map.py <input1> <input2>

Arguments:
    input1 (str): Must be either "ada" or "bolt"
    input2 (str): Must be either "NB" or "OB"

Description:
    This script sets the mapping based on the provided cluster type, which should
    be either "ada" or "bolt".
"""

import os
import sys
import subprocess

ADA = "ewr-ada-jobsrv-lv01.hpc.schrodinger.com:8030"
BOLT = "boltsub3.schrodinger.com:8030"

sdgr_path = os.environ["SCHRODINGER"]
remote_sdgr_path = f"/nfs/working/builds/"
local_sdgr_path = sdgr_path


def sdgr_version():
    version_txt = os.path.join(sdgr_path, "version.txt")

    with open(version_txt, "r") as file:
        data = file.read()
        split_data = data.split()
        version = split_data[2]
        build = split_data[4]

    return [version, build]


def create_cmd(cluster, sdgr_vers, sdgr_build, build_type):
    if cluster == "ada":
        cluster = ADA
    else:
        cluster = BOLT

    cmd = f"{sdgr_path}/jsc job-schrodinger-map set -launch-schrodinger {local_sdgr_path} -job-schrodinger {remote_sdgr_path}/{build_type}/{sdgr_vers}/build-{sdgr_build} {cluster}"

    return cmd

def print_mapping():
    cmd = f"{sdgr_path}/jsc job-schrodinger-map list"
    return cmd


if __name__ == "__main__":
    cluster = sys.argv[1]
    build_type = sys.argv[2]
    sdgr_vers = sdgr_version()[0].strip(",")
    sdgr_build = sdgr_version()[1]
    mapping_cmd = create_cmd(cluster, sdgr_vers, sdgr_build, build_type)
    print_map = print_mapping()

    try:
        result = subprocess.run(mapping_cmd,
                                shell=True,
                                check=True,
                                text=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        if result.stderr:
            print("Command error output:", result.stderr)
        elif result.returncode == 0:
            print("mapping succeeded")
            subprocess.run(print_map,shell=True)
            
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        print(f"stderr: {e.stderr}")
