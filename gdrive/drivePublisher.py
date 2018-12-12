from apiclient import discovery
from apiclient.http import MediaFileUpload
from httplib2 import Http
from oauth2client import file, client, tools

class Gpublisher():                                                                                                     #Googe Drive API object
        def __init__(self):                                                                                             #setup Google Drive API
                print("initializing Google Drive...")

                scope = 'https://www.googleapis.com/auth/drive'                                                         #grant full auth
                store = file.Storage('gdrive/storage.json')                                                             #get storage
                credentials = store.get()                                                                               #get credentials
                if not credentials or credentials.invalid:
                        flow = client.flow_from_clientsecrets('gdrive/credentials.json', scope)
                        credentials = tools.run_flow(flow, store)
                self.gdrive = discovery.build('drive', 'v3', http=credentials.authorize(Http()))                        #Google Drive object

                print("done")

        def upload(self, imagePath, imageName="photo", folderID='16gFypOom7AEcIwuH50Bnt2TjLWx1JZPE'):                   #upload image from disk to MailBot folder in Google Drive
                fileMetadata = {
                        'name': [imageName],
                        'parents': [folderID]
                }
                media = MediaFileUpload(imagePath,
                                        mimetype='image/jpeg',
                                        resumable=True)
                file = self.gdrive.files().create(body=fileMetadata,
                                        media_body=media,
                                        fields='id').execute()
                return file.get('id')                                                                                   #return Google Drive file id

        def __del__(self):                                                                                              #close safely
            print("stopping Google Drive...")
            print("done")
