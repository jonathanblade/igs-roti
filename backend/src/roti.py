import numpy as np
import matplotlib.pyplot as plt

from base64 import b64encode
from datetime import date
from fastapi import UploadFile
from itertools import groupby
from unlzw import unlzw
from tempfile import NamedTemporaryFile
from typing import List, Tuple

plt.rcParams["font.size"] = 16
plt.rcParams["figure.figsize"] = (8, 8)
plt.rcParams["figure.dpi"] = 300
plt.rcParams["savefig.bbox"] = "tight"

START_ROTIMAP = "START OF ROTIPOLARMAP"
END_ROTIMAP = "END OF ROTIPOLARMAP"
FILE_ENCODING = "cp1252"

MLT = np.linspace(0, 24, 180)


class ROTIMap:
    def __init__(self):
        self.MLAT = []
        self.ROTI = []
        self.DATE = None

    async def read_from_file(self, file: UploadFile) -> None:
        bytes_obj = await file.read()
        if file.filename.endswith(".Z"):
            bytes_obj = unlzw(bytes_obj)
        self.read_rotimap(bytes_obj)

    def find_rotimap(self, lines: List[bytes]) -> Tuple[int, int]:
        start_rotimap = None
        end_rotimap = None
        for i, line in enumerate(lines):
            if bytes(START_ROTIMAP, FILE_ENCODING) in line:
                start_rotimap = i
            if bytes(END_ROTIMAP, FILE_ENCODING) in line:
                end_rotimap = i
        if not start_rotimap:
            raise Exception(f"'{START_ROTIMAP}' not found")
        if not end_rotimap:
            raise Exception(f"'{END_ROTIMAP}' not found")
        return (start_rotimap, end_rotimap)

    def read_rotimap(self, bytes_obj: bytes) -> None:
        lines = bytes_obj.splitlines()
        start_rotimap, end_rotimap = self.find_rotimap(lines)
        self.read_rotimap_date(lines[start_rotimap + 1])
        for _, group in groupby(
            lines[start_rotimap + 2 : end_rotimap],
            key=lambda line: len(self.parse_line(line)) == 3,
        ):
            line = b"".join(list(group))
            parsed_line = self.parse_line(line)
            if len(parsed_line) == 3:
                self.MLAT.append(parsed_line[0])
            else:
                self.ROTI.append(parsed_line)

    def read_rotimap_date(self, line: bytes) -> None:
        parsed_line = self.parse_line(line)
        year = int(parsed_line[0])
        month = int(parsed_line[1])
        day = int(parsed_line[2])
        self.DATE = date(year, month, day)

    def parse_line(self, line: bytes, encoding: str = FILE_ENCODING) -> List[float]:
        return list(map(float, line.strip().decode(encoding).split()))

    def plot(self) -> str:
        fig = plt.figure()
        ax = fig.add_subplot(projection="polar")

        ax.set_title(self.DATE.strftime("%d %B %Y"))
        ax.set_xticklabels(["06", "", "12", "", "18", "", "00 MLT", ""])
        ax.set_rgrids([90, 80, 70, 60, 50], angle=45)
        ax.set_rlim(bottom=90, top=50)

        theta, r = np.meshgrid(MLT, self.MLAT)
        cax = ax.contourf(
            theta,
            r,
            self.ROTI,
            levels=np.linspace(0, 1, 51),
            cmap="jet",
            vmin=0,
            vmax=1,
        )
        cbar = fig.colorbar(
            cax, ticks=np.linspace(0, 1, 6), orientation="horizontal", pad=0.1
        )
        cbar.set_label("ROTI, TECU/min")

        with NamedTemporaryFile(suffix=".png") as f:
            fig.savefig(f, format="png")
            f.seek(0)
            return f"data:image/png;base64,{b64encode(f.read()).decode('ascii')}"
