from flask_restful import Resource, reqparse
from app.models.groups_model import Groups
from app.models.users_model import Users
from mongoengine import NotUniqueError, ValidationError, DoesNotExist
import requests
import json
from app.sessions_ids import sessions_ids


class GetByCoor(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('coordinates', required=True)
        args = parser.parse_args()  # parse arguments to dictionary

        loc_response = []

        url = "https://maps.googleapis.com/maps/api/geocode/json?latlng="+args.get('coordinates')+"&key=AIzaSyBu-btSrvUAGaR-GHHfdk0kjlwiO91XV8k&language=iw"
        payload={}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        locations_json = json.loads(response.text)
        for loc in locations_json["results"]:
            loc_response.append({"groupid": loc["place_id"], "groupname": loc["formatted_address"], "grouptype": loc["types"][0]})

        return loc_response, 200

class AddUser(Resource):
    def post(self):
        def add_group_to_user(username, groupid):
            user = Users.objects.get(username=username)
            user_groups = user.group_ids
            user_groups.append(groupid)
            Users.objects(username=username).update(group_ids=user_groups)
            
            response = {"message": "User added successfully.", "username": username, "groupid": groupid}
            return response, 200



        ##### TODO: Check if group exist by groupid, If exists add user to group

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

class GetGroups(Resource):
    def get(self):
        groups = Groups.objects()
        return json.loads(groups.to_json()), 200
