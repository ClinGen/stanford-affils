# Reference

Reference guides contain code conventions, technical reference for APIs,
and technical reference for other aspects of the HCI’s machinery.
Reference material is information-oriented.

## Affiliations Service API

### Routes

- [`api/database_list/`](#apidatabase_list)
- [`api/database_list/<int:pk>/`](#apidatabase_listintpk)
- [`api/affiliations_list/`](#apiaffiliations_list)
- [`api/affiliation_detail/`](#apiaffiliation_detail)
- [`api/affiliation_detail/uuid/<str:uuid>/`](#apiaffiliation_detailuuidstruuid)
- [`api/affiliation/create/`](#apiaffiliationcreate)
- [`api/affiliation/update/affiliation_id/<int:affiliation_id>/`](#apiaffiliationupdateaffiliation_idintaffiliation_id)
- [`api/affiliation/update/expert_panel_id/<int:expert_panel_id>/`](#apiaffiliationupdateexpert_panel_idintexpert_panel_id)
- [`api/cdwg_list/`](#apicdwg_list)
- [`api/cdwg_detail/id/<int:id>/`](#apicdwg_detailidintid)
- [`api/cdwg_detail/name/<str:name>/`](#apicdwg_detailnamestrname)
- [`api/cdwg/create/`](#apicdwgcreate)
- [`api/cdwg/id/<int:id>/update/`](#apicdwgidintidupdate)

#### `api/database_list/`

Shows detailed information for each affiliation in the database in a list.

#### `api/database_list/<int:pk>/`

Shows detailed information for a specific affiliation in the database. 
Requires the primary key for the affiliation.

#### `api/affiliations_list/`

Shows basic information for all affiliations in a list.

#### `api/affiliation_detail/`

Shows basic information for a specific affiliation. Requires query parameter `affil_id`.

#### `api/affiliation_detail/uuid/<str:uuid>/`

Shows detailed information for a specific affiliation given the GPM UUID.

#### `api/affiliation/create/`

Creates a new affiliation. Returns unique `affiliation_id` and corresponding
`expert_panel_id` if successful. Returns error message with missing or invalid fields
otherwise.

#### `api/affiliation/update/affiliation_id/<int:affiliation_id>/`

Updates an affiliation by ID.

#### `api/affiliation/update/expert_panel_id/<int:expert_panel_id>/`

Updates an affiliation by ID.

#### `api/cdwg_list/`

Shows all clinical domain working groups in a list.

#### `api/cdwg_detail/id/<int:id>/`

Shows detailed information for a specific clinical domain working group given the ID.

#### `api/cdwg_detail/name/<str:name>/`

Shows detailed information for a specific clinical domain working group given the name.

#### `api/cdwg/create/`

Creates a new clinical domain working group.

#### `api/cdwg/id/<int:id>/update/`

Updates a clinical domain working group by ID.
