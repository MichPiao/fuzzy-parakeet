class FileOperator:
    def openfile(self, default: str, count: int, mode: str):
        name = str(default)
        print(name)
        while count:
            fname = input(f'File name ({mode}):   ')
            if len(fname) < 1:
                return open(name, mode=mode)
            try:
                return open(fname, mode=mode)
            except FileNotFoundError:
                count -= 1
                print(f'File cannot be opened: {fname} ({count} counts left)')
        else:
            print('Out of counts.')
            quit()
