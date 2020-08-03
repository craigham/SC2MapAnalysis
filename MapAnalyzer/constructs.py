from typing import Optional, TYPE_CHECKING

import numpy as np
from sc2.game_info import Ramp as sc2Ramp
from sc2.position import Point2

from .Polygon import Polygon

if TYPE_CHECKING:  # pragma: no cover
    from .MapData import MapData
    from .sc2pathlibp.choke import Choke


class PathLibChoke:
    # noinspection PyProtectedMember
    def __init__(self, pathlib_choke: "Choke", pk: int):
        self.id = pk
        self.pixels = set(pathlib_choke.pixels)
        self.main_line = pathlib_choke.pixels
        self.pathlib_choke = pathlib_choke

    def __repr__(self) -> str:
        return f"[{self.id}]PathLibChoke; {len(self.pixels)}"


class ChokeArea(Polygon):
    """
    ChokeArea DocString
    """

    def __init__(
            self, array: np.ndarray, map_data: "MapData", pathlibchoke: Optional[PathLibChoke] = None
    ) -> None:
        super().__init__(map_data=map_data, array=array)
        self.main_line = None
        self.id = 'Unregistered'
        self.md_pl_choke = None
        if pathlibchoke:
            self.main_line = pathlibchoke.main_line
            self.id = pathlibchoke.id
            self.md_pl_choke = pathlibchoke
        self.is_choke = True

    def calc_areas(self) -> None:
        if self.main_line:
            points = [min(self.points), max(self.points)]
            areas = self.areas
            for point in points:
                point = int(point[0]), int(point[1])
                new_areas = self.map_data.where_all(point)
                if self in new_areas:
                    new_areas.pop(new_areas.index(self))
                areas.extend(new_areas)
            self.areas = list(set(areas))

    def __repr__(self) -> str:  # pragma: no cover
        return f"<[{self.id}]ChokeArea[size={self.area}]> of  {self.areas}"


class MDRamp(ChokeArea):
    """
    MDRamp DocString
    """

    def __init__(self, map_data: "MapData", array: np.ndarray, ramp: sc2Ramp) -> None:
        super().__init__(map_data=map_data, array=array)
        self.is_ramp = True
        self.ramp = ramp

    def calc_areas(self) -> None:
        return

    @property
    def top_center(self) -> Point2:
        # warning when sc2 fails to provide a top_center, and fallback to  .center
        if self.ramp.top_center is not None:
            return self.ramp.top_center
        else:
            self.map_data.logger.debug(f"No top_center found for {self}, falling back to `center`")

    @property
    def bottom_center(self) -> Point2:
        # warning when sc2 fails to provide a bottom_center, and fallback to  .center
        if self.ramp.bottom_center is not None:
            return self.ramp.bottom_center
        else:
            self.map_data.logger.debug(f"No bottom_center found for {self}, falling back to `center`")

    def __repr__(self):  # pragma: no cover
        return f"<MDRamp[size={self.area}]: {self.areas}>"

    def __str__(self):
        return f"R[{self.area}]"


class VisionBlockerArea(ChokeArea):
    """
    VisionBlockerArea DocString
    """

    def __init__(self, map_data: "MapData", array: np.ndarray) -> None:
        super().__init__(map_data=map_data, array=array)
        self.is_vision_blocker = True

    def __repr__(self):  # pragma: no cover
        return f"<VisionBlockerArea[size={self.area}]: {self.areas}>"
