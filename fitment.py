#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'yangzhuo'

import os
import pymel.core as pm


fitment_label = 'dayu_command_label'
fitment_hotkey = 'dayu_command_hotkey'
fitment_description = 'dayu_command_description'
fitment_key_func_names = ['dayu_command', 'dayu_double']
fitment_default_icon = os.path.join(os.path.dirname(__file__), 'fitment_default.png')
fitment_icon_ext = '.png'
BUTTON_ICON_SIZE = 20
GLOBAL_MENU_DATA, GLOBAL_LAYOUT_DATA = {}, {}

display_folder = os.path.join(os.path.dirname(__file__), 'display')


def add_out_liner_mouse():
    mouse_folder = os.path.join(display_folder, 'outliner', 'mouse')
    add_mouse_menu(mouse_folder)


def add_views_mouse():
    mouse_folder = os.path.join(display_folder, 'views', 'mouse')
    add_mouse_menu(mouse_folder)


def add_hypershade_mouse():
    mouse_folder = os.path.join(display_folder, 'hypershade', 'mouse')
    add_mouse_menu(mouse_folder)


def scan_files(folder):
    for root, _, file_list in os.walk(folder):
        for f in file_list:
            if f.endswith('.py') and f != '__init__.py':
                yield os.path.join(root, f)


def scan_folder(folder):
    for root, folders, _ in os.walk(folder):
        for f in folders:
            yield os.path.join(root, f)


def add_mouse_menu(mouse_folder):
    _d = pm.menuItem(divider=True)
    menu_parent = '|'.join(_d.name().split('|')[:-1])
    py_files = list(scan_files(mouse_folder))

    for py_file in py_files:
        file_parent = os.path.dirname(py_file)
        sub_menu_path = file_parent.replace(mouse_folder, '').replace('\\', '/').strip('/').strip('|')
        if not sub_menu_path:
            sub_parent = menu_parent
        else:
            sub_parent = _create_submenu(sub_menu_path, folder_path=mouse_folder, root_menu=menu_parent)

        _create_command(py_file, sub_parent)

    pm.setParent(menu_parent, menu=True)


def _create_submenu(menu_path, folder_path, root_menu):
    items = menu_path.split('/')
    menu = root_menu
    for item in items:
        _menu = _find_menu(menu, item)
        folder_path = os.path.join(folder_path, item)
        if _menu:
            menu = _menu
        else:
            menu = pm.menuItem(label=item, parent=menu, subMenu=True, tearOff=True, image='')

    return menu


def _filter_menu(menu, parent, menu_name):
    result = menu.parent().startswith(parent) and pm.menu(menu, q=True, label=True) == menu_name
    if not result:
        result = menu.startswith(parent) and menu.endswith('|' + menu_name)
    return result


def _find_menu(parent, menu_name):
    key = '{}_{}'.format(str(parent), menu_name)
    menu = GLOBAL_MENU_DATA.get(key)
    if menu is None:
        menu = next((m for m in pm.lsUI(menus=True, long=True) if _filter_menu(m, parent, menu_name)), None)
        GLOBAL_MENU_DATA.setdefault(key, menu)

    return menu


def _create_command(py_file, parent):
    command_data = parse(py_file)
    command = command_data.get('command', '')

    description = command_data.get('description')

    if not command:
        return

    return pm.menuItem(label=command_data['label'], ann=description, image=command_data['icon'], c=command,
                       parent=parent)


def add_menus(folder, parent):
    for sub_folder in list(scan_folder(folder)):
        menu = _find_menu(parent, os.path.basename(sub_folder))
        if os.path.basename(sub_folder).startswith('.'):  # .idea folder
            continue
        if not menu:
            menu = pm.menu(parent=parent, label=os.path.basename(sub_folder), tearOff=True)

        menu.deleteAllItems()
        py_files = list(scan_files(sub_folder))

        for py_file in py_files:

            file_parent = os.path.dirname(py_file)
            sub_menu_path = file_parent.replace(sub_folder, '').replace('\\', '/').strip('/').strip('|')
            if not sub_menu_path:
                sub_parent = menu
            else:
                sub_parent = _create_submenu(sub_menu_path, folder_path=sub_folder, root_menu=menu)

            _create_command(py_file, sub_parent)


def _find_button_layout(parent, layout_name):
    key = '{}_{}'.format(str(parent), layout_name)
    layout = GLOBAL_LAYOUT_DATA.get(key)
    if layout is None:
        layout = next((lay for lay in pm.lsUI(long=True, type='flowLayout') if lay.parent().startswith(parent) and pm.flowLayout(lay, q=True, ann=True) == layout_name), None)

    return layout


def _create_button(py_file, parent):
    if os.path.isfile(py_file):
        command_data = parse(py_file)
        command = command_data.get('command', '')

        description = command_data.get('description', '')
        if not command:
            return
        return pm.iconTextButton(label=command_data['label'], ann=description, image=command_data['icon'], c=command,
                                 parent=parent, w=BUTTON_ICON_SIZE, h=BUTTON_ICON_SIZE)
    else:
        # sub menu
        folder = py_file
        folder_name = os.path.basename(folder)
        btn = pm.iconTextButton(label=folder_name, ann=folder_name, image=get_icon_path(folder),
                                parent=parent, w=BUTTON_ICON_SIZE, h=BUTTON_ICON_SIZE)
        menu = pm.popupMenu(folder_name, p=btn, button=True)
        return menu


def _create_button_menu(menu_path, folder_path, root_layout):
    items = menu_path.split('/')
    menu = root_layout

    for item in items:
        _menu = _find_menu(menu, item)
        folder_path = r'{}'.format(os.path.join(folder_path, item))
        if _menu:
            menu = _menu
        else:
            menu = _create_button(folder_path, menu)
    return menu


def add_buttons(folder, parent):
    layout = _find_button_layout(parent=parent, layout_name=os.path.basename(folder))
    if not layout:
        layout = pm.flowLayout(parent=parent, ann=os.path.basename(folder))

    child_array = pm.flowLayout(layout, q=True, childArray=True)
    if child_array:
        pm.deleteUI(child_array)

    py_files = list(scan_files(folder))

    for py_file in py_files:
        file_parent = os.path.dirname(py_file)
        sub_menu_path = file_parent.replace(folder, '').replace('\\', '/').strip('/').strip('|')
        if not sub_menu_path:
            _create_button(py_file, layout)
        else:
            sub_parent = _create_button_menu(sub_menu_path, folder_path=folder, root_layout=layout)
            _create_command(py_file, sub_parent)


def _get_view_planes():
    return [p for p in pm.lsUI(long=False, p=True) if 'modelPanel' in p]


def _get_view_bar():
    return [lay.parent() for lay in pm.lsUI(long=True, controlLayouts=True)
            if lay.parent() and lay.parent().name().endswith('modelEditorIconBar')]


def parse(py_file):
    """
    :param py_file:
    :return: {label: '',
              description: '',
              hotkey: '',
              command: '',
              icon: ''}
    """
    data = {}

    execfile(py_file)

    with open(py_file, 'r') as f:
        py_string = f.read()

    data['label'] = locals().get(fitment_label, os.path.basename(py_file))
    data['description'] = locals().get(fitment_description, data['label'])
    data['hotkey'] = locals().get(fitment_hotkey, '')

    for func_name in fitment_key_func_names:
        func = locals().get(func_name, None)
        if func:
            data[func_name.split('_')[-1]] = '{}\n{}()'.format(py_string, func_name)

    data['icon'] = get_icon_path(py_file)

    return data


def get_icon_path(path):
    if os.path.exists(path):
        pass
    return fitment_default_icon


def fitment():

    # main window menu
    main_menu_folder = os.path.join(display_folder, 'main_menu', 'menu')
    if os.path.exists(main_menu_folder):
        add_menus(folder=main_menu_folder, parent='MayaWindow')

    # out liner menu
    out_liner_folder = os.path.join(display_folder, 'outliner', 'menu')
    if os.path.exists(out_liner_folder):
        add_menus(folder=out_liner_folder, parent='Outliner|ToggledOutlinerLayout|outlinerPanel1')

    # view button
    view_button_folder = os.path.join(display_folder, 'views', 'tools')
    if os.path.exists(view_button_folder):
        for bar in _get_view_bar():
            add_buttons(folder=view_button_folder, parent=bar)

    # view menu
    view_menu_folder = os.path.join(display_folder, 'views', 'menu')
    if os.path.isdir(view_menu_folder):
        for view in _get_view_planes():
            try:
                add_menus(folder=view_menu_folder, parent=view)
            except Exception as e:
                print 'Error: %s' % e

