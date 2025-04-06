from dataclasses import dataclass, field
from functools import cached_property
import pandas as pd


from core.datamodels import (
    Address,
    FavoriteLocation,
    HomeConfig,
)
from core.commute import simulate_commutes


@dataclass
class UserProfile:
    user_id: str
    name: str = ""
    down_payment: float = 0
    favorites: dict[str, FavoriteLocation] = field(default_factory=dict)
    homes: list[HomeConfig] = field(default_factory=list)

    def __post_init__(self):
        if not self.name:
            self.name = self.user_id
        self._simulate_commutes()

    def _simulate_commutes(self):
        for home in self.homes:
            for fav in self.favorites.values():
                if fav.nickname not in home.commute_results:
                    home.commute_results[fav.nickname] = simulate_commutes(
                        fav.address,
                        home,
                        fav.commute_config.modes,
                        [fav.commute_config.arrival, fav.commute_config.departure],
                    )

    def add_home(self, home: HomeConfig):
        for fav in self.favorites.values():
            home.commute_results[fav.nickname] = simulate_commutes(
                fav.address,
                home,
                fav.commute_config.modes,
                [fav.commute_config.arrival, fav.commute_config.departure],
            )

        self.homes.append(home)

    def add_favorite(self, location: FavoriteLocation):
        self.favorites[location.nickname] = location

    def remove_favorite(self, nickname: str):
        del self.favorites[nickname]

    def remove_home(self, address: Address):
        for home in self.homes:
            if home.address == address:
                self.homes.remove(home)

    @cached_property
    def map_favs(self) -> pd.DataFrame:
        favorites = [
            [k, v.address.longitude, v.address.latitude]
            for k, v in self.favorites.items()
        ]
        favorites_df = pd.DataFrame(
            favorites, columns=["name", "longitude", "latitude"]
        )
        return favorites_df

    @cached_property
    def map_homes(self) -> pd.DataFrame:
        homes = [
            [home.address.address, home.address.longitude, home.address.latitude]
            for home in self.homes
        ]
        homes_df = pd.DataFrame(homes, columns=["address", "longitude", "latitude"])
        return homes_df

    @cached_property
    def homes_df(self) -> pd.DataFrame:
        columns = ["address", "price", "monthly_cost"]
        for fav in self.favorites.values():
            for mode in fav.commute_config.modes:
                columns.append(fav.nickname + f"_{mode.value}_duration")
                columns.append(fav.nickname + f"_{mode.value}_cost")

        homes = []
        for home in self.homes:
            home_row = [home.address.address, home.price, home.monthly_cost]
            for fav in self.favorites.values():
                for mode in fav.commute_config.modes:
                    home_row.append(
                        home.commute_results[fav.nickname][mode.value].duration
                    )
                    home_row.append(home.commute_results[fav.nickname][mode.value].cost)
            homes.append(home_row)
        homes_df = pd.DataFrame(homes, columns=columns)
        return homes_df
