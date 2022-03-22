#!/usr/bin/env python3

from fabric.api import *

from common import manager_fsim_dir, set_fabric_firesim_pem

def build_default_workloads():
    """ Builds workloads that will be run on F1 instances as part of CI """

    with prefix('cd {} && source ./env.sh'.format(manager_fsim_dir)), \
         prefix('cd deploy/workloads'):

        # avoid logging excessive amounts to prevent GH-A masking secrets (which slows down log output)
        with settings(warn_only=True):
            rc = run("marshal -v build br-base.json &> br-base.full.log").return_code
            print(f"marshal exit code was '{rc}'")
            run("cat br-base.full.log")
            if rc != 0:
                raise Exception("Building br-base.json failed to run")

        run("make linux-poweroff")
        run("make allpaper")

if __name__ == "__main__":
    set_fabric_firesim_pem()
    execute(build_default_workloads, hosts=["localhost"])
