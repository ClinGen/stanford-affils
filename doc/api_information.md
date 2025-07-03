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

### URLS

TEST: `https://affils-test.clinicalgenome.org/api/`

PROD: `https://affils.clinicalgenome.org/api/`

Example: `https://affils-test.clinicalgenome.org/api/affiliations_list/` will
give you a JSON response of all affiliations
