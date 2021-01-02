from flask_restful import Resource, reqparse
from app.models.groups_model import Groups
from app.models.users_model import Users
from mongoengine import NotUniqueError, ValidationError, DoesNotExist
import requests
import json
from app.sessions_ids import sessions_ids

class GetGroupByCoor(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('coordinates', required=True)
        parser.add_argument('session_id', required=True)
        args = parser.parse_args()  # parse arguments to dictionary

        loc_response = []

        url = "https://maps.googleapis.com/maps/api/geocode/json?latlng="+args.get('coordinates')+"&key=AIzaSyBu-btSrvUAGaR-GHHfdk0kjlwiO91XV8k&language=iw"
        payload={}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        locations_json = json.loads(response.text)
        for loc in locations_json["results"]:
            try:
                group = Groups.objects.get(groupid=loc["place_id"])
                users = group.users

            except:
                users = []
                
            if sessions_ids[args.get('session_id')] in users:
                continue
            loc_response.append({"groupid": loc["place_id"], "groupname": loc["formatted_address"], "grouptype": loc["types"][0], "users": users})

        return loc_response, 200


class AddUserToGroup(Resource):
    def post(self):
        def add_group_to_user(username, groupid):
            user = Users.objects.get(username=username)
            user_groups = user.group_ids
            user_groups.append(groupid)
            Users.objects(username=username).update(group_ids=user_groups)
            
            response = {"message": "User added successfully.", "username": username, "groupid": groupid}
            return response, 200

        parser = reqparse.RequestParser()
        parser.add_argument('groupname', required=True)
        parser.add_argument('grouptype', required=True)
        parser.add_argument('groupid', required=True)
        parser.add_argument('session_id', required=True)
        args = parser.parse_args()  # parse arguments to dictionary

        try:
            group = Groups.objects.get(groupid=args.get('groupid'))
            group_users = group.users
            if sessions_ids[args.get('session_id')] in group_users:
                return {"message": "User already in group."}, 500
            group_users.append(sessions_ids[args.get('session_id')])
            print(group_users)
            Groups.objects(groupid=args.get('groupid')).update(users=group_users)
            print("added")
            
        except DoesNotExist:
            # If new group
            g = Groups(
                groupname=args.get('groupname'),
                grouptype=args.get('grouptype'),
                groupid=args.get('groupid'),
                users=[sessions_ids[args.get('session_id')]],
            )
            try:
                g.save()
            except ValidationError:
                return {"message": "Bad input."}, 500
            except NotUniqueError as e:
                print(e)
                return {"message": "User already exists."}, 500
            else:
                return add_group_to_user(sessions_ids[args.get('session_id')], args.get('groupid'))

        except ValidationError:
            return {"message": "Bad input."}, 500
        except NotUniqueError as e:
            print(e)
            return {"message": "User already exists."}, 500
        else:
            return add_group_to_user(sessions_ids[args.get('session_id')], args.get('groupid'))


class GetAllGroups(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('session_id', required=True)
        _ = parser.parse_args()  # parse arguments to dictionary
        groups = Groups.objects()
        return json.loads(groups.to_json()), 200

class SearchGroup(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('address', required=True)
        parser.add_argument('session_id', required=True)
        args = parser.parse_args()  # parse arguments to dictionary

        results_json = []

        url = "https://maps.googleapis.com/maps/api/geocode/json?address="+args.get('address')+"&key=AIzaSyBu-btSrvUAGaR-GHHfdk0kjlwiO91XV8k&language=iw"
        payload={}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        search_results = json.loads(response.text)
        for result in search_results["results"]:
            try:
                group = Groups.objects.get(groupid=result["place_id"])
                users = group.users

            except:
                users = []
            results_json.append({"groupname": result["formatted_address"], "groupid": result["place_id"], "grouptype": result["types"][0], "user": users})

            address_componets = {}
            sub_address = []

            for components in result["address_components"]:
                address_componets[components["types"][0]] = components["long_name"]

            if "street_number" in address_componets.keys():
                sub_address.append("{0}, {1}, {2}".format(address_componets["route"], address_componets["locality"], address_componets["country"]))
            if "route" in address_componets.keys():
                sub_address.append("{0}, {1}".format(address_componets["locality"], address_componets["country"]))
            if "locality" in address_componets.keys():
                print("found country")
                sub_address.append("{0}".format(address_componets["country"]))
            
            [sub_address.append(val) for key, val in address_componets.items() if "administrative_area" in key]

            for sub_addr in sub_address:
                print(sub_address)
                url = "https://maps.googleapis.com/maps/api/geocode/json?address="+sub_addr+"&key=AIzaSyBu-btSrvUAGaR-GHHfdk0kjlwiO91XV8k&language=iw"

                response_sub = requests.request("GET", url, headers=headers, data=payload)

                search_results_sub = json.loads(response_sub.text)
                for result_sub in search_results_sub["results"]:
                    try:
                        group = Groups.objects.get(groupid=result_sub["place_id"])
                        users = group.users

                    except:
                        users = []
                    results_json.append({"groupname": result_sub["formatted_address"], "groupid": result_sub["place_id"], "grouptype": result_sub["types"][0], "user": users})

        return {"message": "Found {0} Groups.".format(len(results_json)),"results":results_json}, 200