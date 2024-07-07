#~ /usr/bin/env python3
import os
import os.path

def select_one(prompt, types):
    'Prompt & return Sqlite types for PyDAO, or False.'
    for ss, value in enumerate(types):
        print(f'{ss+1}.) {types[ss]}') 
    ans = input(prompt)
    if not ans:
        return False
    which = int(ans)
    if which >= 1 and which <= len(types):
        return types[which-1]
    return False


def get_bool(prompt):
    'Prompt & return True if input starts with "Y" or "y"'
    ans = input(prompt)
    if ans and ans[0] in 'Yy':
        return True
    return False


def get_int(prompt):
    'Prompt & return an integer, else False. Caveat zero based.'
    ans = input(prompt)
    if ans:
        try:
            return int(ans.strip())
        except: pass
    return False


def project_overwrite(adict, afqn):
    'Always returns a three-tuple.'
    with open(afqn, 'w') as fh:
        payl = str(adict)
        if fh.write(payl) == len(payl):
            return True, adict, afqn
    return False, adict, afqn


def mk_projectfn(project_name):
    'Check for BASE file name in the pwd. No-name Exception = "Done"'
    if not project_name:
        raise Exception("Done.")
    return f'./{project_name}.dict'


def project_exists(fqproject_name):
    'Check for BASE file name in the pwd. No-name Exception = "Done"'
    if not fqproject_name:
        raise Exception("Done.")
    return os.path.exists(fqproject_name)

    
def create(*args, **kwargs):
    'Create a GenTUI Project.'
    if get_bool("Create a NEW GenTUI Project? y/N: "):
        project = {}; key=None; value=None
        project_name = mk_projectfn(input("Enter project name: "))
        if project_exists(project_name):
            print("Error: File exists. Use Update?")
            return False, None
        print("Enter Tag. Tap Enter when done ...")
        while True:
            key = input("Field name: ")
            if key:
                value = select_one(
                    "Select field type: ",
                    ['INTEGER','REAL','TEXT']
                    )
                if value:
                    project[key] = value
            if not key or not value:
                if not project:
                    return False, None
                return project_overwrite(project, project_name)
    return False, None


def is_safe(astr)->bool:
    "Caveat 'tre basic ..."
    if astr:
        astr = astr.strip()
        if astr:
            return astr[0] == '{'
    return False


def read(*args, **kwargs):
    'Read existing GenTUI Project.'
    names = []
    for fname in os.listdir('./'):
        if fname.endswith('.dict'):
            names.append(fname)
    if not names:
        return False, None
    zfile = select_one("Which project #? ", names)
    if not zfile:
        return False, None
    fname = f'./{zfile}'
    with open(fname) as fh:
        astr = fh.read()
        if is_safe(astr):
            proj = eval(astr)
            if proj and isinstance(proj, dict):
                return True, proj, fname # 3 param true
    return False, None


def update(*args, **kwargs):
    'Update a GenTUI Project.'
    changed = False
    sel = read(args, kwargs)
    if sel and sel[0]:
        while True:
            show_project(sel[1])
            print("1.) Add Field")
            print("2.) Change Field")
            which = get_int("Which #? ([enter] if done): ")
            if not which:
                if changed:
                    if get_bool("Project definition changed - save? y/N: "):
                        if project_overwrite(sel[1], sel[2]):
                            print(f"Project {sel[2]} updated.")
                            return sel
                        else:
                            raise Exception(f"Error: Unable to save {sel[2]}!")
                return sel
            if which == 1:
                key = input("New field name: ")
                if key:
                    value = select_one(
                        "Select field type: ",
                        ['INTEGER','REAL','TEXT']
                        )
                    if value:
                        sel[1][key] = value
                        changed = True
                continue
            elif which == 2:    # safe coding is no accident.
                key = select_one("Select field: ", list(sel[1]))
                if key:
                    if get_bool(f"Rename {key}? y/N: "):
                        nkey = input(f"New name for {key}: ")
                        if not nkey:
                            if get_bool(f"Delete {key}? "):
                                del sel[1][key]
                                print(f"Removed {key}.")
                                if project_overwrite(sel[1], sel[2]):
                                    print(f"Project {sel[2]} updated.")
                                    return sel
                                else:
                                    raise Exception(f"Error: Unable to save {sel[2]}!")
                        else:
                            value = sel[1][key]
                            del sel[1][key]
                            sel[1][nkey] = value
                            print(f"Renamed {key} to {nkey}.")
                            key = nkey
                            changed = True
                    if get_bool(f"Change {key} type? y/N: "):
                        value = select_one(
                            "Select field type: ",
                            ['INTEGER','REAL','TEXT']
                            )
                        if value:
                            sel[1][key] = value
                            print(f"Changed {key} type to {value}")
                            changed = True
    return False, None


def delete(*args, **kwargs):
    'Delete a GenTUI Project.'
    sel = read(args, kwargs)
    if sel and sel[0]:
        if get_bool(
            f"Delete Project {sel[2]}? \There's no undo, dude! y/N: "\
            ):
                os.remove(sel[2])
                if not os.path.exists(sel[2]):
                    print(f"Deleted {sel[2]}")
                    return sel
                else:
                    print(f"Error: Unable to remove {sel[2]}.")
    return False, None


def my_quit(*args, **kwargs):
    'Quit GenTUI.'
    print('Bye!')
    quit()


def show_project(project):
    if project:
        max_ = len(max(project))
        print('*' * 10)
        for col in project:
            print(col.ljust(max_ + 1), end= '')
            print(project[col])
        print('*' * 10,end='')
    print()
    

def mainloop(*args, **kwargs):
    options = {
        'c':create,
        'r':read,
        'u':update,
        'd':delete,
        'q':my_quit
        }
    project = None
    while True:
        try:
            show_project(project)
            for op in options:
                print(f'{op}.) {options[op].__doc__}')
            sel = input("Which: ")
            if sel in options:
                resp = options[sel](args, kwargs)
                if resp[0]:
                    project = resp[1]
        except Exception as ex:
            print(f'Error: {ex}')
            

if __name__ == '__main__':
    mainloop()
