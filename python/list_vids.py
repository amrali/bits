import os
import psutil as ps

def get_flash_proc():
    for p in ps.process_iter():
        if 'ppapi' in p.name:
            return p

def get_vid_fds(proc):
    base = '/proc/{}/fd/'.format(proc.pid)
    fds = os.listdir(base)
    for fd in fds:
        path = os.readlink(base + fd)
        if 'flash' in path.lower():
            yield fd

def get_fd_size(proc, fd):
    base = '/proc/{}/fdinfo/{}'.format(proc.pid, fd)
    with open(base, 'rb') as fdi:
        data = fdi.readline().replace('pos:\t', '')
    return int(data)

if __name__ == '__main__':
    base = '/proc/{}/fd/{}'
    p = get_flash_proc()
    fds = get_vid_fds(p)
    for fd in fds:
        size = get_fd_size(p, fd)
        print base.format(p.pid, fd), size, "({} MiB)".format(size / 1024.0**2)

