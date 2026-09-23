# Tennessee Data Center Map

## Run locally

From the UTK project root:

```bash
cd "outputs/Data center/TN/Map"
python3 -m http.server 8000
```

Open `http://localhost:8000/tennessee_dcmap.html` in a browser. Stop the server with Ctrl+C. The map data is embedded in the HTML, but basemap tiles, JavaScript libraries, and the Tennessee boundary require an internet connection.

The default basemap is OpenFreeMap Positron. If a basemap request returns HTTP 403, use the layer menu at top right to try another basemap and inspect the failing request URL in the browser's Network tab. A 403 from a tile host is a remote-service response; the local Python server does not serve the tiles.

## Sources and Attribution

### Facility data

The facility records were compiled and deduplicated from:

- [PeeringDB Facility API](https://www.peeringdb.com/api/fac?state=TN&country=US) — operational interconnection and colocation facilities.
- [FracTracker Alliance Data Centers dataset](https://services.arcgis.com/jDGuO8tYggdCCnUJ/arcgis/rest/services/data_centers_v4_agol_all/FeatureServer/0) — facility locations, project status, capacity, and related attributes.
- [Compute Atlas Facilities API](https://www.compute-atlas.com/api/facilities?state=TN) — data centers, AI facilities, crypto-mining sites, and related projects.
- Additional public sources — official operator pages, government records, filings, news reports, and industry directories. Record-level links are available in each map popup.

### Geographic data

- Basemap tiles and styles: [OpenFreeMap](https://openfreemap.org/), [OpenMapTiles](https://openmaptiles.org/), and [OpenStreetMap contributors](https://www.openstreetmap.org/copyright).
- Optional standard basemap: [OpenStreetMap](https://www.openstreetmap.org/copyright).
- Tennessee state boundary: [U.S. Census Bureau TIGERweb](https://tigerweb.geo.census.gov/tigerwebmain/TIGERweb_main.html).

### Mapping software

The map interface uses [Leaflet 1.9.4](https://leafletjs.com/), [MapLibre GL JS](https://maplibre.org/maplibre-gl-js/docs/), and [MapLibre GL Leaflet](https://github.com/maplibre/maplibre-gl-leaflet).

### Recommended attribution

Use the following statement when publishing the map, a screenshot, or a derived figure:

> Facility data: PeeringDB, FracTracker Alliance, Compute Atlas, and record-level public sources. Map tiles: OpenFreeMap © OpenMapTiles; map data © OpenStreetMap contributors. Tennessee boundary: U.S. Census Bureau TIGERweb.

For a specific facility, also cite the evidence links shown in its popup and include the date on which the map was accessed.

## User Guide

### Map legend

#### Marker shape

| Shape | Meaning |
|---|---|
| Circle | Data center |
| Square | Interconnection facility |
| Diamond | Crypto-mining facility |
| Dashed circle | Unconfirmed candidate site |
| Circle with × | Cancelled record / negative sample, from either `Master` or `Candidate_Sites` |
| Square with Ⅱ | Jurisdiction data-center moratorium; its point is a government or town reference, not a facility site |

#### Marker color

| Color | Lifecycle status |
|---|---|
| Green | Operational |
| Amber | Under construction |
| Blue | Proposed |
| Purple | Expanding |
| Black | Unknown |

Candidate sites use a white marker with a dashed amber outline. Cancelled records use a pale red marker with an ×, regardless of facility type or capacity.

#### Marker size

| Size | Meaning |
|---|---|
| Small default marker | No published capacity value |
| Larger marker | Higher published capacity in MW |

Marker size uses a logarithmic scale, so it helps compare capacity ranges but is not directly proportional to MW. A missing capacity value means “not published,” not zero.

Hover over a marker for a short summary. Click it to view facility details, data-quality information, and evidence links.

### Control panel

- **Visible facilities**: number of non-cancelled Master markers currently shown.
- **With published MW**: visible confirmed facilities with a reported capacity.
- **Candidate sites**: number of non-cancelled candidate markers currently shown.
- **Cancelled / negative**: number of visible cancelled markers from both source sheets.
- **Policy moratoriums**: number of visible `Moratoriums` records. All 11 records in the current workbook have reference-point coordinates.
- **Search**: searches visible facilities and candidate records by name, operator, city, county, or ID. Reset filters if a known record does not appear.
- **Map layers**: independently show or hide facilities, unconfirmed candidates, cancelled records, and policy moratoriums.
- **Crypto included**: shows or hides crypto-mining facilities.
- **Verification class**: filters confirmed, review-required, or candidate records.
- **Source confidence**: filters records by high, medium, or low confidence.
- **QA state**: filters records with coordinate or status conflicts.
- **Lifecycle**: click a status button to show or hide that status.
- **Operator**: displays facilities for one operator.
- **Published capacity**: filters facilities by reported MW or missing capacity.
- **Reset filters**: restores all records and fits the map to the visible Tennessee locations.

Use the arrow in the control panel to collapse or expand it. The legend at bottom left can also be collapsed. Use the top-right layer menu to switch basemaps. Zoom controls are in the bottom-right corner.

## Interpretation Notes

- Candidate sites are separate from confirmed facilities and should not be included in confirmed-facility counts.
- Cancelled markers are historical negative examples, not active facilities or proposed sites. They are excluded from the facility and candidate counters.
- Moratorium records describe local policy. Their map points locate a jurisdiction reference, not the policy boundary or an affected facility. Eight records have no operator attributable to the policy; the other three link to existing facilities for context only. A linked facility's operator is not the operator of a jurisdiction-wide moratorium.
- Coordinates may represent an exact site, an address, an approximate location, or a city-level location. Check the popup before using a point for detailed spatial analysis.
- Published capacity may be incomplete. A missing value must not be treated as zero.
- Status, ownership, capacity, and location can change. Review the update date and evidence links before publication.
- The map is a collection of publicly identifiable records, not a guaranteed complete census of all Tennessee facilities.
