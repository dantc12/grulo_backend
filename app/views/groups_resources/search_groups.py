from app.utils import get_google_groups_by_addr, check_if_logged_in


def get_group_by_address(session_id: str, address: str):
    message, return_code = check_if_logged_in(session_id)
    if return_code == 400:
        return message, return_code

    google_groups = get_google_groups_by_addr(address)

    results = []

    for google_group in google_groups:
        results.append({
            "group_name": google_group["formatted_address"],
            "group_id": google_group["place_id"],
            "group_type": google_group["types"][0]})

        address_components = {}
        sub_address = []

        for components in google_group["address_components"]:
            address_components[components["types"][0]] = components["long_name"]
        if "street_number" in address_components.keys():
            sub_address.append("{0}, {1}, {2}".format(address_components["route"],
                                                      address_components["locality"],
                                                      address_components["country"]))
        if "route" in address_components.keys():
            sub_address.append("{0}, {1}".format(address_components["locality"], address_components["country"]))
        if "locality" in address_components.keys():
            sub_address.append("{0}".format(address_components["country"]))

        # [sub_address.append(val) for key, val in address_components.items() if "administrative_area" in key]
        for sub_address in sub_address:
            search_results_sub = get_google_groups_by_addr(sub_address)
            for result_sub in search_results_sub:
                results.append({
                    "group_name": result_sub["formatted_address"],
                    "group_id": result_sub["place_id"],
                    "group_type": result_sub["types"][0]})

    return results, 200
