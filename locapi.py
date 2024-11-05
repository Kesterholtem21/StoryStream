import requests

class LibraryOfCongressAPI:

    def query(keyword, format_type="json", results_per_page=50, sort_by="date", filters=[]):
        # base api query url
        BASE_URL = "https://www.loc.gov/books/"


        # initial parameters
        params = {
            "q": keyword,
            "fo": format_type,
            "c": results_per_page,
            "sb": sort_by
        }

        # add filters
        queryFilters = ""
        for index, (key, value) in enumerate(filters):
            if index > 0:
                queryFilters += "|"
            queryFilters += f"{key}:{value}"
        
        if queryFilters:
            params["fa"] = queryFilters

        try:
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()  # check for successful response
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None
