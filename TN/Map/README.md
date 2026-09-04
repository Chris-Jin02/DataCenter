# Tennessee Data Center Map

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
| Dashed circle | Candidate site, not a confirmed facility |

#### Marker color

| Color | Lifecycle status |
|---|---|
| Green | Operational |
| Amber | Under construction |
| Blue | Proposed |
| Purple | Expanding |
| Gray | Cancelled or inactive |
| Black | Unknown |

Candidate sites use a white marker with a dashed amber outline, regardless of lifecycle status.

#### Marker size

| Size | Meaning |
|---|---|
| Small default marker | No published capacity value |
| Larger marker | Higher published capacity in MW |

Marker size uses a logarithmic scale, so it helps compare capacity ranges but is not directly proportional to MW. A missing capacity value means “not published,” not zero.

Hover over a marker for a short summary. Click it to view facility details, data-quality information, and evidence links.

### Control panel

- **Visible facilities**: number of confirmed facility markers currently shown.
- **With published MW**: visible confirmed facilities with a reported capacity.
- **Candidate sites**: number of candidate markers currently shown.
- **Search**: searches visible records by facility name, operator, city, county, or facility ID. Reset filters if a known facility does not appear.
- **Crypto included**: shows or hides crypto-mining facilities.
- **Candidate sites included**: shows or hides the separate candidate layer.
- **Verification class**: filters confirmed, review-required, or candidate records.
- **Source confidence**: filters records by high, medium, or low confidence.
- **QA state**: filters records with coordinate or status conflicts.
- **Lifecycle**: click a status button to show or hide that status.
- **Operator**: displays facilities for one operator.
- **Published capacity**: filters facilities by reported MW or missing capacity.
- **Reset filters**: restores all records and fits the map to the visible Tennessee locations.

Use the arrow in the control panel to collapse or expand it. Use the top-right layer menu to switch between the available basemaps. Zoom controls are in the bottom-right corner.

## Interpretation Notes

- Candidate sites are separate from confirmed facilities and should not be included in confirmed-facility counts.
- Coordinates may represent an exact site, an address, an approximate location, or a city-level location. Check the popup before using a point for detailed spatial analysis.
- Published capacity may be incomplete. A missing value must not be treated as zero.
- Status, ownership, capacity, and location can change. Review the update date and evidence links before publication.
- The map is a collection of publicly identifiable records, not a guaranteed complete census of all Tennessee facilities.
