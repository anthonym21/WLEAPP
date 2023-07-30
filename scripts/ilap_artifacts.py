# To add a new artifact module, import it here as shown below:
#     from scripts.artifacts.fruitninja import get_fruitninja
# Also add the grep search for that module using the same name
# to the 'tosearch' data structure.

import traceback

from scripts.artifacts.activitiesCache import get_activitiesCache
from scripts.artifacts.betterDiscord import get_betterDiscord
from scripts.artifacts.box import get_box
from scripts.artifacts.dropbox import get_dropbox
from scripts.artifacts.facebookMessenger import get_facebookMessenger
from scripts.artifacts.googleDrive import get_googleDrive
from scripts.artifacts.pfirewall import get_pfirewall
from scripts.artifacts.setupapiDev import get_setupapiDev
from scripts.artifacts.windowsAlarms import get_windowsAlarms
from scripts.artifacts.windowsCortana import get_windowsCortana
from scripts.artifacts.windowsEdge import get_windowsEdge
from scripts.artifacts.windowsNotification import get_windowsNotification
from scripts.artifacts.windowsPhotos import get_windowsPhotos
from scripts.artifacts.windowsStickyNotes import get_windowsStickyNotes
from scripts.artifacts.windowsYourPhone import get_windowsYourPhone

from scripts.ilapfuncs import *

# GREP searches for each module
# Format is Key='modulename', Value=Tuple('Module Pretty Name', 'regex_term')
#   regex_term can be a string or a list/tuple of strings
# Here modulename must match the get_xxxxxx function name for that module. 
# For example: If modulename='profit', function name must be get_profit(..)
# Don't forget to import the module above!!!!

tosearch = {
    'activitiesCache':('ActivitiesCache', ('*/AppData/Local/ConnectedDevicesPlatform/L.*/ActivitiesCache.db')),
    'betterDiscord':('Better Discord', ('*/AppData/Roaming/BetterDiscord/plugins/MessageLoggerV2Data.config.json')),
    'box':('Box', ('*/AppData/Local/Box/Box/Data/*.db')),
    'dropbox':('Dropbox', ('*/AppData/Local/Packages/*.DROPBOX_*/LocalState/users/*/*.sqlite', '*/AppData/Local/Dropbox/instance1/sync_history.db')),
    'facebookMessenger':('Facebook Messenger', ('*/AppData/Local/Packages/FACEBOOK.*_*/LocalState/msys_*.db')),
    'googleDrive':('Google Drive', ('*/AppData/Local/Google/DriveFS/*/metadata_sqlite_db')),
    'pfirewall':('Firewall', ('*/pfirewall.log')),
    'setupapiDev':('setupapi.dev.log', ('*/Windows/INF/setupapi.dev.log')),
    'windowsAlarms':('Windows Alarms', ('*/AppData/Local/Packages/Microsoft.WindowsAlarms_*/LocalState/Alarms/Alarms.json', '*/AppData/Local/Packages/Microsoft.WindowsAlarms_*/Settings/settings.dat')),
    'windowsCortana':('Windows Cortana', ('*/AppData/Local/Packages/Microsoft.Windows.Cortana_*/LocalState/DeviceSearchCache/AppCache*.txt')),
    'windowsEdge':('Windows Edge', ('*/AppData/Local/Microsoft/Windows/WebCache/WebCacheV01.dat')),
    'windowsNotification':('Windows Notification', ('*/Appdata/Local/Microsoft/Windows/Notifications/wpndatabase.db')),
    'windowsPhotos':('Windows Photos', ('*/AppData/Local/Packages/Microsoft.Windows.Photos_*/LocalState/MediaDb.v1.sqlite')),
    'windowsStickyNotes':('Windows StickyNotes', ('*/AppData/Local/Packages/Microsoft.MicrosoftStickyNotes_*/LocalState/plum.sqlite')),
    'windowsYourPhone':('Windows YourPhone', ('*/AppData/Local/Packages/Microsoft.YourPhone_*/LocalCache/Indexed/*/System/Database/*'))
}
slash = '\\' if is_platform_windows() else '/'

def process_artifact(files_found, artifact_func, artifact_name, seeker, report_folder_base, wrap_text):
    ''' Perform the common setup for each artifact, ie, 
        1. Create the report folder for it
        2. Fetch the method (function) and call it
        3. Wrap processing function in a try..except block

        Args:
            files_found: list of files that matched regex

            artifact_func: method to call

            artifact_name: Pretty name of artifact

            seeker: FileSeeker object to pass to method
            
            wrap_text: whether the text data will be wrapped or not using textwrap.  Useful for tools that want to parse the data.
    '''
    logfunc(f'{artifact_name} [{artifact_func}] artifact executing')
    report_folder = os.path.join(report_folder_base, artifact_name) + slash
    try:
        if not os.path.isdir(report_folder):
            os.makedirs(report_folder)
    except Exception as ex:
        logfunc(
            f'Error creating {artifact_name} report directory at path {report_folder}'
        )
        logfunc(f'Reading {artifact_name} artifact failed!')
        logfunc(f'Error was {str(ex)}')
        return
    try:
        method = globals()[f'get_{artifact_func}']
        method(files_found, report_folder, seeker, wrap_text)
    except Exception as ex:
        logfunc(f'Reading {artifact_name} artifact had errors!')
        logfunc(f'Error was {str(ex)}')
        logfunc(f'Exception Traceback: {traceback.format_exc()}')
        return

    logfunc(f'{artifact_name} [{artifact_func}] artifact completed')
    