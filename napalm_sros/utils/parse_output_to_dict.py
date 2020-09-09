import os
import textfsm


def parse_with_textfsm(template, command_output):
    """
    :param template: TextFSM template to parse command
    :param command_output: Command output from a node
    :return: List of dicts. Dict per FSM row.
    """
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), template), "r") as template_file:
        fsm = textfsm.TextFSM(template_file)
        fsm_results = fsm.ParseText(command_output)
    output_list = []
    # print fsm.header
    for index, line in enumerate(fsm_results, 1):
        # print line
        textfsm_dict = {}
        for number, value in enumerate(line):
            textfsm_dict[fsm.header[number]] = value
        output_list.append(textfsm_dict)
    return output_list


def parse_with_textfsm_by_first_value(template, command_output):
    """
    :param template: TextFSM template to parse command
    :param command_output: Command output from a node
    :return: Dict per first(top) textFSM template value
    """
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), template), "r") as template_file:
        fsm = textfsm.TextFSM(template_file)
        fsm_results = fsm.ParseText(command_output)
    textfsm_dict = {}
    # print fsm.header
    for line in fsm_results:
        # print line
        textfsm_dict[line[0]] = {}
        for number, value in enumerate(line):
            if value != line[0]:
                textfsm_dict[line[0]].update({fsm.header[number]: value})
    return textfsm_dict


if __name__ == '__main__':
    pass
