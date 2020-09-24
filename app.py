from flask import Flask, request, send_from_directory, Response
from flask_restful import Resource, Api
import shortuuid
import qrcode
from qrcode.image.pure import PymagingImage
from sqlitedict import SqliteDict


app = Flask(__name__)
api = Api(app)
mydict = SqliteDict('./my_db.sqlite', autocommit=True)


class CreateBookmark(Resource):
    def post(self):
        input = request.get_json()
        id = shortuuid.uuid(name=input['url'])
        if id in mydict.keys():
            return {'reason': "The given URL already existed in the system."}, 400
        mydict[id] = {
            'id': id,
            'name': input['name'],
            'url': input['url'],
            'description': input['description'],
            'count': 0
        }
        return {"id": id}, 201


class GetBookmarkByID(Resource):
    def get(self, BookmarkID):
        if BookmarkID in mydict.keys():
            bookmark = mydict.get(BookmarkID)
            bookmark['count'] += 1
            mydict[BookmarkID] = bookmark
            return mydict.get(BookmarkID)
        else:
            return {'reason': "404 Bookmark Not Found"}, 404


class GetQRCodeByID(Resource):
    def get(self, BookmarkID):
        if BookmarkID in mydict.keys():
            link = mydict.get(BookmarkID)['url']
            img = qrcode.make(link, image_factory=PymagingImage)
            # save file into directory
            with open('qrcode.PNG', 'wb') as f:
                img.save(f)
            return send_from_directory(app.root_path, 'qrcode.PNG', as_attachment=True)
        else:
            return {'reason': "404 Bookmark Not Found"}, 404


class DeleteBookmarkByID(Resource):
    def delete(self, BookmarkID):
        if BookmarkID in mydict.keys():
            del mydict[BookmarkID]
            return {}, 204
        else:
            return {'reason': "404 Not Found"}, 404


# Return the number of GET request made to each bookmark
# It should support conditional GET.
class GetStatsByID(Resource):
    def get(self, BookmarkID):
        # do not use this, does not account for null header
        # InputEtag = request.headers['ETag']

        # use this, account for optional header
        InputEtag = request.headers.get('ETag')
        if BookmarkID in mydict.keys():
            GetCount = str(mydict.get(BookmarkID)['count'])
            if InputEtag == GetCount:
                # print(InputEtag)
                return Response(status=304, headers={'ETag': GetCount})
            else:
                # print(InputEtag)
                # response object format: body, status code, headers
                return Response(response=GetCount, status=200, headers={'ETag': GetCount})
        else:
            return {'reason': "404 Bookmark Not Found"}, 404


api.add_resource(CreateBookmark, '/api/bookmarks')
api.add_resource(GetBookmarkByID, '/api/bookmarks/<string:BookmarkID>')
api.add_resource(DeleteBookmarkByID, '/api/bookmarks/<string:BookmarkID>')
api.add_resource(GetQRCodeByID, '/api/bookmarks/<string:BookmarkID>/qrcode')
api.add_resource(GetStatsByID, '/api/bookmarks/<string:BookmarkID>/stats')


if __name__ == '__main__':
    app.run(debug=True)
