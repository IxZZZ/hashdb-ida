# System packages/modules
import json
import requests

# HashDB
from ..exceptions import Exceptions
from ..types.algorithm import Algorithm


def fetch(api_url: str, timeout: int) -> dict:
    """
    Fetches all of the algorithms from the server.
    @param api_url: api url to use
    @param timeout: amount of seconds before we timeout
    @return: a json object (dict) fetched from the server
             containing data about each algorithm
    @raise Exceptions.Timeout: if a request timed out
    @raise Exceptions.ResponseCode: if an unexpected status code is encountered,
    @raise Exceptions.Json: if the response body isn't valid JSON.
    """
    # Perform the request
    url = f"{api_url}/hash"
    try:
        response = requests.get(url, timeout=timeout)
    except requests.Timeout:
        raise Exceptions.Timeout(f"Timed out when executing a request: {url}")

    # Check if the response code was 200 OK
    if not response.ok:
        raise Exceptions.ResponseCode(f"Unexpected response code from: {url}", response_code=response.status_code)

    # Convert and return the results
    try:
        return response.json()
    except json.JSONDecodeError:
        raise Exceptions.Json(f"Invalid response body from: {url}, body={response.text}")


def format_response(response_data: dict) -> list[Algorithm]:
    """
    Formats the raw json response into friendly structures.
    @param response_data: a json
    @return: a list of Algorithm instances
    @raise Exceptions.UnknownAlgorithmType: if an unknown algorithm type is encountered
    """
    # Parse the algorithms
    algorithms = []

    algorithm: dict
    # Iterate the algorithms
    for algorithm in response_data.get("algorithms", []):
        name: str = algorithm.get("algorithm")
        size: int = parse_algorithm_type(algorithm.get("type"))

        # Append an Algorithm instance
        algorithms.append(Algorithm(name=name, size=size))

    # Return the list of Algorithm instances
    return algorithms


def parse_algorithm_type(algorithm_type: str) -> int:
    """
    Converts an algorithm type into its equivalent
      size in bits.
    @param algorithm_type: type of the algorithm
    @return: size of the algorithm in bits
    @raise Exceptions.UnknownAlgorithmType: if the algorithm type is unknown
    """
    predetermined_sizes = {
        "unsigned_int":  32,
        "unsigned_long": 64
    }

    # Check if the algorithm type is a valid type
    if algorithm_type not in predetermined_sizes.keys():
        raise Exceptions.UnknownAlgorithmType(f"Unknown algorithm type encountered: {algorithm_type}",
                                              algorithm_type=algorithm_type)

    # Return the size of the algorithm
    return predetermined_sizes[algorithm_type]
