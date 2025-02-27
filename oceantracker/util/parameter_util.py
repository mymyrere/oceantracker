
from oceantracker import common_info_default_param_dict_templates as common_info
from oceantracker.util.module_importing_util  import import_module_from_string
from oceantracker.util.parameter_checking import merge_params_with_defaults

def make_class_instance_from_params(name, params,msg_logger, class_role_name=None,
                                     crumbs='', merge_params=True):
    # make a class instance  dynamically,  get instance of class from string eg oceantracker.solver.Solver
    # assumes class_name param exists
    # add class sequence number, used for in class list

    # work out class name
    if 'class_name' not in params or params['class_name'] is None:
        if class_role_name is not None and class_role_name in common_info.default_class_names:
            params['class_name'] = common_info.default_class_names[class_role_name]

        else:
            msg_logger.msg('params for ' + crumbs + ' must contain class_name ' + str(class_role_name),
                            fatal_error=True, hint= 'given params are = ' + str(params), exit_now=True)

    i = import_module_from_string(params['class_name'], msg_logger,crumbs = crumbs + ' > importing module')
    i.info['name'] = name
    i.info['class_role'] = class_role_name

    if merge_params:
        i.params  = merge_params_with_defaults(params, i.default_params, msg_logger, crumbs=crumbs)

    # attach the current message loger
    i.msg_logger = msg_logger
    return i