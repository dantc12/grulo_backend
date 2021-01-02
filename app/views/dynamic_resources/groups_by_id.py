from flask_restful import Resource, reqparse
from mongoengine import DoesNotExist
from app.sessions_ids import sessions_ids
from app.models.users_model import Users
import json
import requests
from app.models.groups_model import Groups
from mongoengine import NotUniqueError, ValidationError, DoesNotExist


class GroupById(Resource):
    def get(self, groupid):
        parser = reqparse.RequestParser()
        parser.add_argument('session_id', required=True)
        _ = parser.parse_args()

        try:
            g = Groups.objects.get(groupid=groupid)
        except DoesNotExist:
            return {"message": "Group doesn't exist."}, 500
        else:
            response = {"message": "Found group successfully."}
            response.update(g.json())
            return response, 200

class AddUserToGroupById(Resource):
    def post(self, groupid):
        def add_group_to_user(username, groupid):
            user = Users.objects.get(username=username)
            user_groups = user.group_ids
            user_groups.append(groupid)
            Users.objects(username=username).update(group_ids=user_groups)
            
            response = {"message": "User added successfully.", "username": username, "groupid": groupid}
            return response, 200

        parser = reqparse.RequestParser()
        parser.add_argument('session_id', required=True)
        args = parser.parse_args() 

        try:
            group = Groups.objects.get(groupid=groupid)
            group_users = group.users
            if sessions_ids[args.get('session_id')] in group_users:
                return {"message": "User already in group."}, 500
            group_users.append(sessions_ids[args.get('session_id')])
            Groups.objects(groupid=groupid).update(users=group_users)
            
        except DoesNotExist:
            url = "https://maps.googleapis.com/maps/api/geocode/json?place_id="+groupid+"&key=AIzaSyBu-btSrvUAGaR-GHHfdk0kjlwiO91XV8k&language=iw"
            payload={}
            headers = {}

            response = requests.request("GET", url, headers=headers, data=payload)

            response_json = json.loads(response.text)
            groupname = response_json["results"][0]["formatted_address"]
            grouptype = response_json["results"][0]["types"][0]

            # If new group
            g = Groups(
                groupname=groupname,
                grouptype=grouptype,
                groupid=groupid,
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
                return add_group_to_user(sessions_ids[args.get('session_id')], groupid)

        except ValidationError:
            return {"message": "Bad input."}, 500
        except NotUniqueError as e:
            print(e)
            return {"message": "User already exists."}, 500
        else:
            return add_group_to_user(sessions_ids[args.get('session_id')], groupid)