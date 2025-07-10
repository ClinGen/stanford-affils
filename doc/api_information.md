## API Key Information

- We are utilizing
  [Django REST Framework API Key](https://florimondmanca.github.io/djangorestframework-api-key/)
  package to support the use of API keys.

### API KEY

- If you are in need of an API Key, please reach out to one of the website
  administrators or your admin user to obtain an API Key.
- Upon creating an API key from the admin, the full API key is shown only once
  in a success message banner. After creation, only the prefix of the API key is
  shown in the admin site, mostly for identification purposes. If you lose the
  full API key, you'll need to regenerate a new one.

### Authorization header

By default, clients must pass their API key via the Authorization header. It
must be formatted as follows: `X-Api-Key <API_KEY>` where \<API_KEY> refers to
the full generated API key

### Endpoints

#### Affiliations

GET `affiliations_list/`

- Get all affiliations in JSON format

GET `affiliation_detail/?affil_id={affiliation_id}`

- Get a specific affiliation in JSON format

POST `affiliation/create/`

- Creates a new Affiliation. This endpoint generates and returns a `201 Created`
  status, unique `affiliation_id` and a corresponding `expert_panel_id` upon
  success.
- Returns a `400 Bad Request` on failure with error message of missing or
  invalid fields.

PATCH `affiliation/<int:affiliation_id>/update/`

- Updates an existing Affiliation. This endpoint generates and returns a
  `200 OK` and full changed affiliation on success.

- Returns a `400 Bad Request` on failure with error message of missing or
  invalid fields.

- Returns a `404 Not Found` on failure with error message.

## POST api/affiliation/create Endpoint Details:

#### Request Example:

The required fields and accepted values are listed below in Required Field
Details and Accepted Values sections below.

```
{
  "full_name": "POST Affiliation",
  "clinical_domain_working_group": 2,
  "type": "VCEP",
  "status": "APPLYING",
  "members": "Jane Smith, John Doe",
  "coordinators": [{
    "coordinator_name": "John Doe",
    "coordinator_email": "email@email.com"
  }],
  "approvers": [{
    "approver_name": "John Doe"
  }],
  "clinvar_submitter_ids": [{
    "clinvar_submitter_id": "1245"
  }]
}
```

#### Successful Response:

Returns `201 Created` with:

- `affiliation_id`: *integer* – Generated affiliation ID (example: 10000)
- `expert_panel_id`: *integer* – Associated expert panel ID (example: 40000)

#### Unsuccessful Responses:

Returns `400 Bad Request` with a JSON object detailing which fields failed
validation.

Example:

```
{
    "error": "Validation Failed",
    "details": {
        "status": [
            "This field is required."
        ]
    }
}
```

#### Required Field Details:

`full_name`: *string* - Full name of the affiliation.
`clinical_domain_working_group`: *integer* - ID of the Clinical Domain Working
Group. `type`: *string* - The type of affiliation. Must be one of the accepted
values below. `status`: *string* - The current status of the affiliation. Must
be one of the accepted values below.

### Optional Fields

The following fields are optional but may be included:

- `members`: *string* – Comma-separated names of members.
- `coordinators`: *list of objects* – Each object must contain
  `coordinator_name` and `coordinator_email`.
- `approvers`: *list of objects* – Each object must contain `approver_name`.
- `clinvar_submitter_ids`: *list of objects* – Each object must contain
  `clinvar_submitter_id`.

#### Accepted Values:

The `clinical_domain_working_group` value is an integer ID referring to a CDWG.
You can find these IDs on the CDWG page of the affiliations site (a dedicated
endpoint is in progress).

Acceptable `type` values:

- VCEP
- GCEP
- SC_VCEP
- INDEPENDENT_CURATION

Acceptable `status` values:

- APPLYING
- ACTIVE
- INACTIVE
- RETIRED
- ARCHIVED

## PATCH affiliation/<int:affiliation_id>/update/ Endpoint Details:

The affiliation_id in the URL is the only required field. In request, only the
values that need to be updated should be included.

#### Successful Response:

Returns `200 OK` with:

- `affiliation_id`: *integer* – Generated affiliation ID (example: 10000)
- `expert_panel_id`: *integer* – Associated expert panel ID (example: 40000)
- `full_name`: *string* - Full name of the affiliation.
- `short_name`: *string* – Short or abbreviation of affiliation.
- `clinical_domain_working_group`: *integer* - ID of the Clinical Domain Working
  Group.
- `type`: *string* - The type of affiliation. Must be one of the accepted values
  below.
- `status`: *string* - The current status of the affiliation. Must be one of the
  accepted values below.
- `members`: *string* – Comma-separated names of members.
- `coordinators`: *list of objects* – Each object must contain
  `coordinator_name` and `coordinator_email`.
- `approvers`: *list of objects* – Each object must contain `approver_name`.
- `clinvar_submitter_ids`: *list of objects* – Each object must contain
  `clinvar_submitter_id`.
- `is_deleted`: *boolean* – True or False if affiliation is tombstoned.

#### Unsuccessful Responses:

Returns `400 Bad Request` with a JSON object detailing which fields failed
validation.

Example:

```
{
    "error": "Request Failed",
    "details": {
        "detail": "No Affiliation matches the given query."
    }
}
```

#### Clinical Domain Working Groups Endpoint Details

A Clinical Domain Working Group (CDWG) is a group associated with specific
clinical domains. This API allows clients to list, retrieve, create, and update
CDWGs.

GET `cdwg_list/`

- Get all CDWG's in JSON format

GET `cdwg_detail/id/<int:id>/`

- Get a specific CDWG by ID in JSON format

GET `cdwg_detail/name/<str:name>/`

- Get a specific CDWG by name in JSON format

POST `cdwg/create/`

- Creates a new CDWG. This endpoint generates and returns a `201 Created`
  status, unique `name` and a corresponding `id` upon success.
- Checks if a CDWG with the provided `name` already exists.
- Returns a `400 Bad Request` on failure with error message of missing or
  invalid fields.

PATCH `cdwg/id/<int:id>/update/`

- Updates an existing CDWG. This endpoint generates and returns a `200 OK` and
  full changed CDWG on success.

- Returns a `400 Bad Request` on failure with error message of missing or
  invalid fields.

## GET api/cdwg_list Endpoint Details:

### Return Values

```
[
  {
    "id": 1,
    "name": "Cardiology"
  },
  {
    "id": 2,
    "name": "Oncology"
  }
]
```

## GET api/cdwg_detail/id/<int:id>/ and cdwg_detail/name/<str:name>/ Endpoint Details:

### Return Values

Example: GET /api/cdwg_detail/id/2/

```
[
  {
    "id": 1,
    "name": "Cardiology"
  },
]
```

## POST api/cdwg/create Endpoint Details:

#### Request Example:

The required fields and accepted values are listed below in Required Field
Details and Accepted Values sections below.

```
{
  "name": "POST CDWG",
}
```

#### Successful Response:

Returns `201 Created` with:

- `name`: *string* – Provided CDWG name.
- `id`: *integer* – Generated CDWG ID.

#### Unsuccessful Responses:

Returns `400 Bad Request` with a JSON object detailing which fields failed
validation.

Example:

```
{
    "error": "Validation Failed",
    "details": {
        "name": [
            "This field is required."
        ]
    }
}
```

#### Required Field Details:

`name`: *string* - Provided name of the CDWG.

## PATCH cdwg/id/<int:id>/update/ Endpoint Details:

The id in the URL is the only required field. In request, only the values that
need to be updated should be included.

#### Request Example:

PATCH /api/cdwg/id/2/update/

```
{
  "name": "Updated CDWG Name",
}
```

#### Response Example:

```
{
  "id": 2,
  "name": "Updated CDWG Name"
}
```

#### Successful Response:

Returns `200 OK` with:

- `name`: *string* – Provided CDWG name.
- `id`: *integer* – Generated CDWG ID.

#### Unsuccessful Responses:

Returns `400 Bad Request` with a JSON object detailing which fields failed
validation.

Example:

```
{
    "error": "Request Failed",
    "details": {
        "detail": "No Affiliation matches the given query."
    }
}
```


### URLS

TEST: `https://affils-test.clinicalgenome.org/api/`

PROD: `https://affils.clinicalgenome.org/api/`

Example: `https://affils-test.clinicalgenome.org/api/affiliations_list/` will
give you a JSON response of all affiliations
