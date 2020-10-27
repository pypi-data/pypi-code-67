import ssl
import ftplib
import datetime
import os


class Ftpsbase(ftplib.FTP_TLS):
    """FTPS subclass that automatically wraps sockets in SSL to support implicit FTPS."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._sock = None

    @property
    def sock(self):
        """Return the socket."""
        return self._sock

    @sock.setter
    def sock(self, value):
        """When modifying the socket, ensure that it is ssl wrapped."""
        if value is not None and not isinstance(value, ssl.SSLSocket):
            value = self.context.wrap_socket(value)
        self._sock = value

    def get_file(self, path, dest_path=None):
        """Read and save data from file which is specified 'path' """
        saved_path = None
        filename = os.path.basename(path)
        if filename != path:
            saved_path = self.pwd()
            self.cwd(os.path.dirname(path))
        with open(dest_path if dest_path else filename, "wb") as f:

            def callback(data):
                f.write(data)

            self.retrbinary(f"RETR {filename}", callback)
        if filename != path:
            self.cwd(saved_path)

    def send_file(self, path, dest_path=None):
        saved_path = None
        if dest_path is not None:
            saved_path = self.pwd()
            self.cwd(os.path.dirname(dest_path))
        filename = os.path.basename(path)
        ftpCommand = f"STOR {filename}"
        file_byte = open(path, "rb")  # file to send
        self.storbinary(ftpCommand, file_byte)  # send the file
        file_byte.close()
        if dest_path is not None:
            self.cwd(saved_path)

    def list_directory(self, dirName):
        dirs = []
        self.dir(dirName, dirs.append)
        files = []
        for dirr in dirs:
            line = dirr.lstrip().split()
            datetmp = " ".join(line[5 : len(line) - 1])  # noqa: E203
            month, day, year = datetmp.split(" ")
            time = None
            now = datetime.datetime.now()
            if year.find(":") > -1:
                time = year
                year = now.year
            else:
                time = "00:00"
            files.append(
                {
                    "permission": line[0],
                    "links": line[1],
                    "owner": line[2],
                    "group": line[3],
                    "size": line[4],
                    "month": month,
                    "day": day,
                    "year": year,
                    "time": time,
                    "name": line[-1],
                }
            )
        return files

    def help(self):
        print(f"=== {type(self).__name__} === \n")
        print(".get_file(path) => get file from ftp path\n")
        print(".send_file(path, dest_path) => send file to ftp path\n")
        print(".list_directory(path) => do ls in ftp in path\n")
