#!/usr/bin/env python

from ecs_api import ECSApi
from textwrap import wrap
import traceback
import logging
import json
import sys

USAGE_HELP = "Usage: ecs <subcommand> [args]\n\n" \
             "Control, list, and manipulate ECS instances.\n"

SUBCOMMAND_HELP = {
    'create': ('<ConfigFile>|spec',
               'Create an ECS instance based on <ConfigFile>.'),
    'delete': ('<ServerID> [<ServerID>] [<ServerID>...]',
               'Delete EVS instances.'),
    'help': ('', 'Display this message.'),
    'list': ('', 'List all ECS instances.'),
    'info': ('<InstanceName>', 'Get information about an/all ECS instance(s).'),
    'start': ('<ServerID> [<ServerID>] [<ServerID>...]',
              'Start ECS instances.'),
    'restart': ('<ServerID> [<ServerID>] [<ServerID>...]',
                'Restart ECS instances.'),
    'stop': ('<ServerID> [<ServerID>] [<ServerID>...]',
             'Stop ECS instances.'),
    'resize': ('<ServerID> <FlavorRef>', 'Modify the specifications of the ECS.'),
    'rename': ('<ServerID> <NewName>', 'Modify the name of the ECS.'),
    'flavors': ('', 'Getting list of flavors.'),
    'images': ('', 'Getting list of images.'),
    'vpcs': ('', 'Getting list of VPCs.'),
    'subnets': ('<VPCID>', 'Getting list of subnets.'),
    'eips': ('', 'Getting list of elastic IP addresses.'),
    'security-groups': ('', 'Getting list of security groups.'),
    'availability-zones': ('', 'Getting list of availability zones.'),
    'keypair-list': ('', 'Get information about ECS ssh-keypair.'),
    'projects': ('', 'Getting list of projects accessible to users.'),
    'project-info': ('<ProjectName>', 'Query information about project.'),
    'task-status': ('<JobID>', 'Get the execution status of task.'),
    'block-attach': ('<ServerID> <VolumeID> <DevicePATH>',
                     'Attach a disk to an ECS.'),
    'block-detach': ('<ServerID> <VolumeID>',
                     'Detach an EVS disk from an ECS.'),
    'block-list': ('<ServerID>',
                   'List virtual block devices attached to an ECS.'),
    'network-attach': ('<ServerID> <count>, <subnet_id>, <security_group_id>',
                       'Add one or multiple NICs to an ECS.'),
    'network-detach': ('<ServerID> <nic_ids>',
                       'Delete one or multiple NICs from an ECS.'),
    'network-list': ('<ServerID>',
                     'List virtual network interfaces attached to an ECS.'),
    'evs-create': ('<name>, <size>, <vol_type>, [<count>]',
                   'Create one or multiple Elastic Volume Service (EVS) disks.'),
    'evs-delete': ('<VolumeID>', 'Delete an EVS disk.'),
    'evs-list': ('', 'List all EVS disks.'),
}

SUBCOMMAND_OPTIONS = {
    'list': (
        ('-l', '--long', 'Output all VM details'),
        ('', '--label', 'Include security labels'),
    ),
}


def ecs_delete(args):
    arg_check(args, 1)
    j_content = ECSApi().delete_ecss(args)
    if "job_id" not in j_content:
        print("Error")
    else:
        print(json.dumps(j_content, indent=4, sort_keys=True))


def ecs_restart(args):
    arg_check(args, 1)
    j_content = ECSApi().restart_ecss(args)
    if "job_id" not in j_content:
        print("Error")
    else:
        print(json.dumps(j_content, indent=4, sort_keys=True))


def ecs_rename(args):
    arg_check(args, 2, 2)
    j_content = ECSApi().modify_ecs_info(args[0], args[1])
    if 'server' not in j_content:
        print("No server")
    else:
        print(json.dumps(j_content['server'], indent=4, sort_keys=True))


def ecs_stop(args):
    arg_check(args, 1)
    j_content = ECSApi().stop_ecss(args)
    if "job_id" not in j_content:
        print("Error")
    else:
        print(json.dumps(j_content, indent=4, sort_keys=True))


def ecs_start(args):
    arg_check(args, 1)
    j_content = ECSApi().start_ecss(args)
    if "job_id" not in j_content:
        print("Error")
    else:
        print(json.dumps(j_content, indent=4, sort_keys=True))


def ecs_resize(args):
    arg_check(args, 2, 2)
    j_content = ECSApi().resize_ecs(args[0], args[1])
    if "job_id" not in j_content:
        print("Error")
    else:
        print(json.dumps(j_content, indent=4, sort_keys=True))


def ecs_list(args):
    j_content = ECSApi().query_ecs()
    if len(j_content['servers']) == 0:
        print("No servers")
    else:
        print '%-36s\t%s' % ("ID", "Name")
        for server in j_content['servers']:
            print '%-36s\t%s' % (server["id"].encode('ascii', 'ignore'), server["name"].encode('ascii', 'ignore'))


def ecs_info(args):
    j_content = ECSApi().query_ecs_detail()
    if len(j_content['servers']) == 0:
        print("No servers")
    else:
        for server in j_content['servers']:
            print(json.dumps(server, indent=4, sort_keys=True))


def ecs_flavors(args):
    j_content = ECSApi().list_flavors()
    if len(j_content['flavors']) == 0:
        print("No flavors")
    else:
        print '%-12s\t%-12s' % ("ID", "Name")
        for flavor in j_content['flavors']:
            print '%-12s\t%-12s' % (flavor['id'], flavor['name'])


def ecs_images(args):
    j_content = ECSApi().query_images()
    if len(j_content['images']) == 0:
        print("No images")
    else:
        print '%-36s\t%-36s\t%-36s\t%-20s' % ("ID", "Name", "OS Version", "Created_date")
        for image in j_content['images']:
            print '%-36s\t%-36s\t%-36s\t%-20s' % \
                  (image['id'], image['name'], image['__os_version'], image['created_at'])


def ecs_vpcs(args):
    j_content = ECSApi().query_vpcs()
    if len(j_content['vpcs']) == 0:
        print("No vpcs")
    else:
        print '%-36s\t%-20s\t%-10s' % ("ID", "Name", "CIDR")
        for vpc in j_content['vpcs']:
            print '%-36s\t%-20s\t%-10s' % (vpc['id'], vpc['name'], vpc['cidr'])


def ecs_subnets(args):
    arg_check(args, 1, 1)
    j_content = ECSApi().query_subnets(args[0])
    if len(j_content['subnets']) == 0:
        print("No subnets")
    else:
        print '%-36s\t%-20s\t%-10s' % ("ID", "Name", "CIDR")
        for subnet in j_content['subnets']:
            print '%-36s\t%-20s\t%-10s' % (subnet['id'], subnet['name'], subnet['cidr'])


def ecs_eips(args):
    j_content = ECSApi().query_eips()
    if len(j_content['publicips']) == 0:
        print("No publicips")
    else:
        print '%-36s\t%-15s\t%-10s' % ("ID", "Public IP Address", "Status")
        for publicip in j_content['publicips']:
            print '%-36s\t%-15s\t%-10s' % (publicip['id'], publicip['public_ip_address'], publicip['status'])


def ecs_security_groups(args):
    j_content = ECSApi().query_security_groups()
    if len(j_content['security_groups']) == 0:
        print("No security_groups")
    else:
        for security_group in j_content['security_groups']:
            print(json.dumps(security_group, indent=4, sort_keys=True))


def ecs_availability_zones(args):
    j_content = ECSApi().query_availability_zones()
    if len(j_content['availabilityZoneInfo']) == 0:
        print("No availability zones")
    else:
        for availabilityzone in j_content['availabilityZoneInfo']:
            print(availabilityzone['zoneName'])


def ecs_keypair_list(args):
    j_content = ECSApi().query_ssh_keypairs()
    if len(j_content['keypairs']) == 0:
        print("No keypairs")
    else:
        for keypair in j_content['keypairs']:
            print(keypair["keypair"]["name"])


def ecs_projects(args):
    j_content = ECSApi().query_projects()
    if len(j_content['projects']) == 0:
        print("No projects")
    else:
        for project in j_content['projects']:
            print(json.dumps(project, indent=4, sort_keys=True))


def ecs_project_info(args):
    arg_check(args, 1, 1)
    j_content = ECSApi().query_project_info(args[0])
    if len(j_content['projects']) == 0:
        print("No projects")
    else:
        print '%-32s\t%s' % ("ID", "Name")
        for project in j_content['projects']:
            print '%-32s\t%s' % (project['id'], project['name'])


def task_status(args):
    arg_check(args, 1, 1)
    j_content = ECSApi().query_task_status(args[0])
    print(json.dumps(j_content, indent=4, sort_keys=True))


def ecs_block_attach(args):
    arg_check(args, 3, 3)
    j_content = ECSApi().attach_volume(*args)
    if "job_id" not in j_content:
        print("Error")
    else:
        print(json.dumps(j_content, indent=4, sort_keys=True))


def ecs_block_detach(args):
    arg_check(args, 2, 2)
    ECSApi().detach_volume(*args)


def ecs_block_list(args):
    arg_check(args, 1, 1)
    j_content = ECSApi().query_volumes(args[0])
    if len(j_content['volumeAttachments']) == 0:
        print("No volumes")
    else:
        print '%-3s\t%-36s\t%-15s' % ("No.", "ID", "Device")
        for i, volume in enumerate(j_content['volumeAttachments']):
            print '%3s\t%-36s\t%-15s' % \
                  (str(i), volume["id"], volume["device"])


def ecs_network_attach(args):
    arg_check(args, 4, 4)
    j_content = ECSApi().add_nics(*args)
    if "job_id" not in j_content:
        print("Error")
    else:
        print(json.dumps(j_content, indent=4, sort_keys=True))


def ecs_network_detach(args):
    arg_check(args, 2)
    j_content = ECSApi().delete_nics(args[0], args[1:])
    if "job_id" not in j_content:
        print("Error")
    else:
        print(json.dumps(j_content, indent=4, sort_keys=True))


def ecs_network_list(args):
    arg_check(args, 1, 1)
    j_content = ECSApi().query_nics(args[0])
    if len(j_content['interfaceAttachments']) == 0:
        print("No NICs")
    else:
        print '%-3s\t%-36s\t%-15s\t%-10s' % ("No.", "ID", "IP Address", "State")
        for i, nic in enumerate(j_content['interfaceAttachments']):
            print '%3s\t%-36s\t%-15s\t%-10s' % \
                  (str(i), nic["port_id"], nic["fixed_ips"][0]["ip_address"], nic["port_state"])


def ecs_evs_create(args):
    arg_check(args, 3, 4)
    j_content = ECSApi().create_evss(*args)
    if "job_id" not in j_content:
        print("Error")
    else:
        print(json.dumps(j_content, indent=4, sort_keys=True))


def ecs_evs_delete(args):
    arg_check(args, 1, 1)
    j_content = ECSApi().delete_evs(args[0])
    print(json.dumps(j_content, indent=4, sort_keys=True))


def ecs_evs_list(args):
    j_content = ECSApi().query_evss()
    if len(j_content['volumes']) == 0:
        print("No EVSs")
    else:
        print '%-36s\t%-40s\t%-5s\t%-10s\t%-10s\t%-10s' % ("ID", "Name", "Size", "Type", "AZ", "Status")
        for volume in j_content['volumes']:
            print '%-36s\t%-40s\t%-5s\t%-10s\t%-10s\t%-10s' % \
                  (volume["id"], volume["name"], volume["size"], volume["volume_type"], volume["availability_zone"],
                   volume["status"])


def ecs_importcommand(command, args):
    cmd = __import__(command, globals(), locals(), 'ecs_api')
    cmd.main([command] + args)


commands = {
    # domain commands
    "delete": ecs_delete,
    "restart": ecs_restart,
    "rename": ecs_rename,
    "stop": ecs_stop,
    "start": ecs_start,
    "resize": ecs_resize,
    "list": ecs_list,
    "info": ecs_info,
    # special
    "flavors": ecs_flavors,
    "images": ecs_images,
    "vpcs": ecs_vpcs,
    "subnets": ecs_subnets,
    "eips": ecs_eips,
    "security-groups": ecs_security_groups,
    "availability-zones": ecs_availability_zones,
    "keypair-list": ecs_keypair_list,
    "projects": ecs_projects,
    "project-info": ecs_project_info,
    "task-status": task_status,
    # block
    "block-attach": ecs_block_attach,
    "block-detach": ecs_block_detach,
    "block-list": ecs_block_list,
    # network
    "network-attach": ecs_network_attach,
    "network-detach": ecs_network_detach,
    "network-list": ecs_network_list,
    # EVS
    "evs-create": ecs_evs_create,
    "evs-delete": ecs_evs_delete,
    "evs-list": ecs_evs_list,
}

IMPORTED_COMMANDS = [
    'create',
]

for c in IMPORTED_COMMANDS:
    commands[c] = eval('lambda args: ecs_importcommand("%s", args)' % c)


def cmd_help(cmd):
    """Print help for a specific subcommand."""

    for fc in SUBCOMMAND_HELP.keys():
        if fc[:len(cmd)] == cmd:
            cmd = fc
            break

    try:
        args, desc = SUBCOMMAND_HELP[cmd]
    except KeyError:
        show_help()
        return

    print 'Usage: ecs %s %s' % (cmd, args)
    print
    print desc

    try:
        # If options help message is defined, print this.
        for shortopt, longopt, desc in SUBCOMMAND_OPTIONS[cmd]:
            if shortopt and longopt:
                optdesc = '%s, %s' % (shortopt, longopt)
            elif shortopt:
                optdesc = shortopt
            elif longopt:
                optdesc = longopt

            wrapped_desc = wrap(desc, 43)
            print '  %-30s %-43s' % (optdesc, wrapped_desc[0])
            for line in wrapped_desc[1:]:
                print ' ' * 33 + line
        print
    except KeyError:
        # if the command is an external module, we grab usage help
        # from the module itself.
        if cmd in IMPORTED_COMMANDS:
            try:
                cmd_module = __import__(cmd, globals(), locals(), 'ecs_api')
                cmd_usage = getattr(cmd_module, "help", None)
                if cmd_usage:
                    print cmd_usage()
            except ImportError:
                pass


def show_help():
    """Print out full help when ecs is called with ecs --help or ecs help"""

    print USAGE_HELP
    print 'ecs full list of subcommands:\n'

    for command in commands:
        try:
            args, desc = SUBCOMMAND_HELP[command]
        except KeyError:
            continue

        wrapped_desc = wrap(desc, 50)
        print ' %-20s %-50s' % (command, wrapped_desc[0])
        for line in wrapped_desc[1:]:
            print ' ' * 22 + line

    print


def usage(cmd=None):
    """ Print help usage information and exits """
    if cmd:
        cmd_help(cmd)
    else:
        show_help()
    sys.exit(1)


def arg_check(args, lo, hi=-1):
    n = len([i for i in args if i != '--'])

    if hi == -1:
        if n < lo:
            logging.error("'ecs %s' requires at least %d argument%s.\n" % (sys.argv[1], lo, lo == 1 and ' ' or 's'))
            usage(sys.argv[1])
    elif lo == hi:
        if n != lo:
            logging.error("'ecs %s' requires %d argument%s.\n" % (sys.argv[1], lo, lo == 1 and ' ' or 's'))
            usage(sys.argv[1])
    else:
        if n < lo or n > hi:
            logging.error("'ecs %s' requires between %d and %d arguments.\n" % (sys.argv[1], lo, hi))
            usage(sys.argv[1])


def ecs_lookup_cmd(cmd):
    if cmd in commands:
        return commands[cmd]
    elif cmd == 'help':
        show_help()
        sys.exit(0)
    else:
        # simulate getopt's prefix matching behaviour
        if len(cmd) > 1:
            same_prefix_cmds = [commands[c] for c in commands.keys()
                                if c[:len(cmd)] == cmd]
            # only execute if there is only 1 match
            if len(same_prefix_cmds) == 1:
                return same_prefix_cmds[0]

        logging.error('Sub Command %s not found!' % cmd)
        usage()


def main(argv=sys.argv):
    if len(argv) < 2:
        usage()

    logging.basicConfig(level=logging.ERROR, format='%(asctime)s %(levelname)s %(message)s')

    # intercept --debug(-d) and output debug log
    for debug_arg in ['--debug', '-d']:
        if debug_arg in argv[1:]:
            if debug_arg == argv[1]:
                logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')
                logging.debug("Running in debug mode")

    # intercept --help(-h) and output our own help
    for help_arg in ['--help', '-h']:
        if help_arg in argv[1:]:
            if help_arg == argv[1]:
                show_help()
            else:
                usage(argv[1])
            sys.exit(0)

    cmd = ecs_lookup_cmd(argv[1])

    # strip off prog name and subcmd
    args = argv[2:]
    if cmd:
        try:
            rc = cmd(args)
            if rc:
                usage()
        except Exception:
            logging.error(traceback.format_exc())
            sys.exit(1)


if __name__ == "__main__":
    main()
