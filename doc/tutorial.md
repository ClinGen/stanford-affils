# Tutorials

Tutorials are lessons that take the reader by the hand through a series
of steps to accomplish something with the affiliations service. They 
are wholly learning-oriented, and specifically, they are oriented
towards learning how rather than learning what.

## Using the Affiliations Service API

The affiliations service provides an API for integration with other tools.
For detailed information on the affiliations service API, check out the
[reference guide](reference.md#affiliations-service-api).

If you need to integrate information from the affiliations service into your tool, first
check the API [routes](reference.md#routes) to see if the information you need requires
an API key. (You will probably need an API key, but there are a few routes that don't
require one.)

If you need an API key, email the maintainers of the affiliations service
(`affils@clinicalgenome.org`) to request an API key. When you receive your API key,
store it in your password manager. The maintainers will not be able to tell you what it
is if you lose it.

### Testing an API Key on the Command Line

(This tutorial assumes you're working on a Unix-like operating system.)

If you'd like to store your API key in an environment variable, open a terminal and
enter the following command:

```
export AFFILS_API_KEY="<insert your API key here>"
```

Then you can use [curl](https://curl.se/) to get some data from the API:

```
curl -H "X-Api-Key:$AFFILS_API_KEY" https://affils-test.clinicalgenome.org/api/affiliations_list/
```

To make the output easier to read, you can install [jq](https://jqlang.org/), and then
pipe the output to jq:

```
curl -H "X-Api-Key:$AFFILS_API_KEY" https://affils-test.clinicalgenome.org/api/affiliations_list/ | jq
```

If you prefer to use [wget](https://www.gnu.org/software/wget/), enter the following
command:

```
wget --header "X-Api-Key: $AFFILS_API_KEY" https://affils-test.clinicalgenome.org/api/affiliations_list/ -O-
```

If you prefer to use [HTTPie](https://httpie.io/), enter the following command:

```
http https://affils-test.clinicalgenome.org/api/affiliations_list/ "X-Api-Key:$AFFILS_API_KEY"
```
