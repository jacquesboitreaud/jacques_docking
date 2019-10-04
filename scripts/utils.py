import os.path as osp

def add_suffix(path, suffix):
    pre, su = osp.split(path)
    return osp.join(pre, su.split('.')[0] + suffix)
def add_suffix_kill_prefix(path, suffix):
    return osp.split(path)[1].split('.')[0] + suffix

def add_suffix_new_path(path, new_path, suffix):
    _, su = osp.split(path)
    return osp.join(new_path, su.split('.')[0] + suffix)

