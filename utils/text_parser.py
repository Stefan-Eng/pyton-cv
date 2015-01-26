def parse(text):
    global_commands, lines = _get_lines_and_commands(text)

    return lines, global_commands

def _get_lines_and_commands(text):
    all_blocks = []
    current_block = []
    commands = []
    previous_was_break = False
    for line in text:
        if '#' in line:
            if line.startswith('#'):
                continue
            else:
                line = line.split('#')[0].strip()
        if line.startswith('/'):
            if _append_command(line):
                commands.append(line)
            else:
                all_blocks.append(current_block)
                current_block = []
                all_blocks.append([line])
                previous_was_break = False # Inline commands always define
                                           # new blocks.
            continue
        if line == "":
            if previous_was_break:
                all_blocks.append(current_block)
                previous_was_break = False
                current_block = []
            elif not previous_was_break:
                previous_was_break = True
                continue
        else: # line not empty, a comment or command.
            if previous_was_break:
                if len(current_block):
                    current_block[-1] += '!/'
                previous_was_break = False
            if line.endswith('//'):
                line = line.replace('//','')
                previous_was_break = True
            else:
                previous_was_break = False
            current_block.append(line)
    if current_block:
        all_blocks.append(current_block)
    fused_lines = [ ' '.join(text_block) for text_block in all_blocks]
    return _command_dictionary(commands), fused_lines

def _command_dictionary(commands):
    command_dict = {}
    for command in commands:
        variable, value = command.split('=')
        variable = variable.replace('/','').strip()
        value = value.strip()
        try:
            command_dict[variable] = int(value)
        except ValueError:
            command_dict[variable] = value
    return command_dict

def _append_command(command):
    line_dependent_commands = ['/line']
    if command in line_dependent_commands:
        return False
    return True
