import dataclasses
from dataclasses import dataclass, field
import datetime
from enum import Enum
from functools import cached_property
import json
from typing import Optional

from urllib.parse import urlencode

from core.geocode import normalize_address


class CommuteMode(Enum):
    DRIVING = "driving"
    WALKING = "walking"
    TRANSIT = "transit"


class Days(Enum):
    MON = "Monday"
    TUE = "Tuesday"
    WED = "Wednesday"
    THU = "Thursday"
    FRI = "Friday"
    SAT = "Saturday"
    SUN = "Sunday"


@dataclass
class CommuteWindow:
    days: list[Days]
    time: str


@dataclass
class CommutePreferences:
    modes: list[CommuteMode]
    arrival: CommuteWindow
    departure: CommuteWindow


@dataclass
class CommuteResult:
    duration: float
    cost: Optional[float] = None
    timestamp: str = field(
        default_factory=lambda: datetime.datetime.now().isoformat(),
        init=False,
        repr=False,
    )


@dataclass
class Address:
    address: str
    latitude: float = field(default=0, kw_only=True, repr=False)
    longitude: float = field(default=0, kw_only=True, repr=False)
    city: str = field(default="", kw_only=True, repr=False)
    state: str = field(default="", kw_only=True, repr=False)
    zipcode: str = field(default="", kw_only=True, repr=False)
    place_id: Optional[int] = field(default=None, kw_only=True, repr=False)
    search_url: Optional[str] = field(default=None, kw_only=True, repr=False)

    def __post_init__(self):
        self.address = self.address.strip()
        if not self.place_id:
            norm_address = normalize_address(self.address)
            self.__dict__.update(norm_address)
        if not self.search_url:
            self.search_url = self._search_url

    @cached_property
    def _search_url(self):
        """Generate a Google Maps URL for the address using urllib"""
        base_url = "https://www.google.com/maps/search/?api=1&"
        formatted_address = urlencode({"query": self.address})
        return base_url + formatted_address

    def __str__(self):
        return self.address


@dataclass
class FavoriteLocation:
    address: Address
    nickname: str
    commute_config: CommutePreferences

    def __str__(self):
        return self.nickname


@dataclass
class HomeConfig:
    address: Address
    listing_url: str
    price: float
    mortgage_rate: float = 0.065
    mortgage_term: int = 30
    hoa: float = 200.0
    insurance_rate: float = 0.005
    commute_results: dict[str, dict[str, CommuteResult]] = field(default_factory=dict)

    @cached_property
    def monthly_cost(self):
        # TODO: Calculate monthly cost
        return (
            self.price
            + self.price * self.mortgage_rate / 12
            + self.hoa
            + self.price * self.insurance_rate
        )


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)  # type: ignore
        if isinstance(o, Enum):
            return o.value
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        return super().default(o)
