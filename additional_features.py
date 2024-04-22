import tkinter
import tkinter.ttk

tkinter_umlauts = ['odiaeresis', 'adiaeresis', 'udiaeresis', 'Odiaeresis', 'Adiaeresis', 'Udiaeresis', 'ssharp']


def set_completion_list(entry, completion_list):
    entry._completion_list = sorted(completion_list, key=str.lower)
    entry._hits = []
    entry._hit_index = 0
    entry.position = 0
    entry.bind('<KeyRelease>', lambda event: handle_keyrelease(event, entry))


def autocomplete(entry, delta=0):
    if delta:
        entry.delete(entry.position, tkinter.END)
    else:
        entry.position = len(entry.get())
    _hits = []
    for element in entry._completion_list:
        if element.lower().startswith(entry.get().lower()):
            _hits.append(element)
    if _hits != entry._hits:
        entry._hit_index = 0
        entry._hits = _hits
    if _hits == entry._hits and entry._hits:
        entry._hit_index = (entry._hit_index + delta) % len(entry._hits)
    if entry._hits:
        entry.delete(0, tkinter.END)
        entry.insert(0, entry._hits[entry._hit_index])
        entry.select_range(entry.position, tkinter.END)


def handle_keyrelease(event, entry):
    if event.keysym == "BackSpace":
        entry.delete(entry.index(tkinter.INSERT), tkinter.END)
        entry.position = entry.index(tkinter.END)
    if event.keysym == "Left":
        if entry.position < entry.index(tkinter.END):
            entry.delete(entry.position, tkinter.END)
        else:
            entry.position = entry.position - 1
            entry.delete(entry.position, tkinter.END)
    if event.keysym == "Right":
        entry.position = entry.index(tkinter.END)
    if event.keysym == "Down":
        autocomplete(entry, 1)
    if event.keysym == "Up":
        autocomplete(entry, -1)
    if len(event.keysym) == 1 or event.keysym in tkinter_umlauts:
        autocomplete(entry)


class MyEntry(tkinter.Entry):
    def set_completion_list(self, completion_list):
        set_completion_list(self, completion_list)

    def autocomplete(self, delta=0):
        autocomplete(self, delta)

    def handle_keyrelease(self, event):
        handle_keyrelease(event, self)


class MyCombobox(tkinter.ttk.Combobox):

    def set_completion_list(self, completion_list):
        set_completion_list(self, completion_list)
        self['values'] = self._completion_list

    def autocomplete(self, delta=0):
        autocomplete(self, delta)

    def handle_keyrelease(self, event):
        handle_keyrelease(event, self)
