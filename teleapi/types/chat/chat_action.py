from enum import Enum


class ChatAction(Enum):
    TYPING: str = "typing"
    CHOOSE_STICKER: str = "choose_sticker"
    FIND_LOCATION: str = "find_location"
    RECORD_VIDEO: str = "record_video"
    RECORD_VOICE: str = "record_voice"
    RECORD_VIDEO_NOTE: str = "record_video_note"
    UPLOAD_VIDEO_NOTE: str = "upload_video_note"
    UPLOAD_VOICE: str = "upload_voice"
    UPLOAD_PHOTO: str = "upload_photo"
    UPLOAD_DOCUMENT: str = "upload_document"
    UPLOAD_VIDEO: str = "upload_video"
