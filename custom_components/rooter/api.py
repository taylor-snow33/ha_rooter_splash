"""API Client for ROOTer stats."""
import logging
import aiohttp
import async_timeout
from bs4 import BeautifulSoup

_LOGGER = logging.getLogger(__name__)

class RooterApiClient:
    """ROOTer API Client."""

    def __init__(self, session: aiohttp.ClientSession, host: str, verify_ssl: bool = False) -> None:
        """Initialize."""
        self._session = session
        self._host = host.rstrip("/")
        self._verify_ssl = verify_ssl

    async def async_get_data(self) -> dict:
        """Fetch and parse data from the splash page."""
        url = f"https://{self._host}/splash.html"
        try:
            async with async_timeout.timeout(10):
                async with self._session.get(url, ssl=self._verify_ssl) as response:
                    response.raise_for_status()
                    html = await response.text()
                    return self._parse_html(html)
        except Exception as e:
            _LOGGER.error("Error fetching ROOTer data: %s", e)
            raise

    def _parse_html(self, html: str) -> dict:
        """Parse HTML content."""
        soup = BeautifulSoup(html, "html.parser")
        data = {}

        tables = soup.find_all("table", class_="center")
        
        def clean(elem):
            if elem:
                # Content is wrapped in a div. Due to malformed HTML, 
                # cells might be nested. We target the first div.
                div = elem.find("div")
                if div:
                    return div.get_text(" ", strip=True)
                # Fallback if no div found (though the HTML suggests div usage)
                return elem.get_text(" ", strip=True)
            return None

        # Helper to get cells by class from a specific table index
        def get_cells(table_idx, class_name):
            if len(tables) > table_idx:
                table = tables[table_idx]
                # If HTML is badly nested, finding all cells with class might work best
                return table.find_all("td", class_=class_name)
            return []

        # Table 1: Modem Metrics (class 'tmsCell')
        # Structure: Strength, CSQ, RSSI, RSCP(RSRP), ECIO(RSRQ), SINR
        cells = get_cells(0, "tmsCell")
        if len(cells) >= 6:
            data["signal_strength"] = clean(cells[0]).replace("%", "").split()[0]
            data["csq"] = clean(cells[1]).split()[0]
            data["rssi"] = clean(cells[2]).split()[0]
            
            # RSRP is in cell 3: "-93 Poor (3G)..." -> "-93"
            data["rsrp"] = clean(cells[3]).split()[0]
            
            # RSRQ is in cell 4: "-13"
            data["rsrq"] = clean(cells[4]).split()[0]
            
            data["sinr"] = clean(cells[5]).split()[0]

        # Table 2: Network (class 'ttmsCell')
        # Mode, MCC, MNC, RNC/eNB ID, LAC, Channel, PCI, Bands, SIM Status
        cells = get_cells(1, "ttmsCell")
        if len(cells) >= 8:
            data["mode"] = clean(cells[0])
            data["mcc"] = clean(cells[1])
            data["mnc"] = clean(cells[2])
            
            enb_full = clean(cells[3])
            # "B7545 (750917)"
            if "(" in enb_full:
                data["cell_id"] = enb_full.split("(")[1].replace(")", "")
            else:
                data["cell_id"] = enb_full
                
            data["lac"] = clean(cells[4])
            data["channel"] = clean(cells[5])
            # PCI at 6, Bands at 7
            data["bands"] = clean(cells[7])

        # Table 3: Device (class 'ttmsCell')
        # Router, Modem, Provider, Protocol, Port, Temp, Ext IP, Interface
        cells = get_cells(2, "ttmsCell")
        if len(cells) >= 6:
            data["router_model"] = clean(cells[0])
            data["modem_model"] = clean(cells[1])
            data["provider"] = clean(cells[2])
            data["protocol"] = clean(cells[3])
            # Port at 4, Temp at 5
            data["temperature"] = clean(cells[5]).replace("°C", "")
            
        return data
