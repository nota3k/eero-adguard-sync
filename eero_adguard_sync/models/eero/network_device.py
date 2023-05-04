from dataclasses import dataclass, field

from eero_adguard_sync.models.eero.client_device import EeroClientDevice


@dataclass
class EeroNetworkDevice:
    mac_address: str
    ip_address: str
    model: str
    location: str
    gateway: bool = False
    ipv6_addresses: list[dict] = field(default_factory=list)

    @property
    def ips(self) -> list[str]:
        ipv6_addresses = [i["address"] for i in self.ipv6_addresses if i.get("address")]
        return [self.ip_address, *ipv6_addresses]

    @property
    def nickname(self) -> str:
        return f"{self.location} {self.model}"

    @property
    def hostname(self) -> str:
        return (f"{self.location} {self.model}").replace(' ', '-').lower()

    def as_client_device(self) -> EeroClientDevice:
        return EeroClientDevice(
            ips=self.ips,
            nickname=self.nickname,
            mac=self.mac_address,
            hostname=self.hostname,
            device_type="generic",
        )
