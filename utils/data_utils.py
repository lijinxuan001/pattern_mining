import re
"""
00:00:58.2822343|ExecutedCommand|LibGalleryABB
00:01:02.3917263|ExecutingCommand|LibGalleryABB|Activated
00:01:02.9541861|ImportedMechanism|IRB7600_150_350
00:01:02.9541861|ExecutedCommand|LibGalleryABB
00:01:10.0793071|ExecutingCommand|LibGalleryABB|Activated
00:01:10.1886793|ImportingCADFile|RSGFX|124713
00:01:10.3918098|ImportingCADFile|RSGFX|77844
"""

# make it fater
def normalize_from_rule(event_type, *args):
    if event_type == "ExecutingCommand":
        return "ExecutingCommand:" + args[0]
    elif event_type == "ExecutedCommand":
        return "ExecutedCommand:" + args[0]
    elif event_type == "ControllerConnectionState":
        return "ControllerConnectionState"
    elif event_type == "AddinLoaded" or event_type == "AddinAdded" or event_type == "AddinLoading":
        return "Addin:" + args[0]
    elif event_type == "NetworkAdapterChange":
        return "NetworkAdapterChange"
    elif event_type == "ImportedMechanism":
        return "ImportedMechanism"
    elif event_type == "ActiveWindowChanged":
        return "ActiveWindowChanged:" + args[1]
    elif event_type == "RibbonTabChanged":
        return "RibbonTabChanged"
    elif event_type == "InstallDistributionPackage":
        return "InstallDistributionPackage"
    elif event_type in ["StartedVC", "StartingVC", "VCAffinity"]:
        return "VirtualControllerEvent"
    elif event_type == "Error":
        return "Error"
    elif event_type == "SystemEvent":
        return "SystemEvent"
    elif event_type == "UserLogMessage":
        return "UserLogMessage"
    elif event_type == "UIThreadWatchdog":
        return "UIThreadWatchdog"
    elif event_type == "ApiInfo":
        return "ApiInfo"
    elif event_type == "ControllerState":
        return "ControllerState"
    elif event_type == "StudioAppFramework":
        return "StudioAppFramework"
    elif event_type == "RobApiSubscribeError":
        return "RobApiSubscribeError"
    elif event_type == "Exception":
        return "Exception"
    elif event_type == "VR":
        return "VR"
    elif event_type == "PaintApplicator":
        return "PaintApplicator"
    elif event_type == "ExportGeometry":
        return "ExportGeometry"
    elif event_type == "ImportingCADFile":
        return "ImportingCADFile"
    elif event_type == "StationLoaded":
        return "StationLoaded"
    elif event_type == "ActivatedPP":
        return "ActivatedPP"
    else:
        return event_type

# Parse, normalize and format output
def normalize_events(events):
    event_sequence = []

    for line in events.strip().split("\n"):
        parts = line.split("|")
        if len(parts) >= 3:
            timestamp, event_type, args = parts[0], parts[1], parts[2:]       
            event_sequence.append(normalize_from_rule(event_type, *args))

    return event_sequence

def parse_log_file(events):
    """ parse log file, return event sequence """
    event_sequence = []

    for line in events.strip().split("\n"):
        parts = line.split("|")

        if len(parts) >= 3:
            timestamp, event_type, details = parts[0], parts[1], parts[2]
            # delete GUID and *.sab
            # AddedController, {29482355-91EB-4976-A615-0901346C9494}
            # Error, PIM: Could not load stream Streams/fcd2a5adad94440e945437b369b280e5.GeoDataStream.sab
            details = re.sub('/[^ ]+\\.sab', '',details)
            details = re.sub(r'\{[A-Za-z0-9-]+\}', '', details)
            # Use regex to find and remove numeric strings longer than 6 characters
            details = re.sub(r'\b\d{3,}\b', '', details)
            # Use regex to find and remove file path
            details = re.sub(r"[A-Za-z]:\\[^ ]+", '', details)
            if event_type == 'Exception':
                details = ""
            event_sequence.append(event_type)

    return event_sequence
