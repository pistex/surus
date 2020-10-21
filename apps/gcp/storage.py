import io
import uuid
import PIL
from storages.backends.gcloud import GoogleCloudStorage, GoogleCloudFile
from storages.utils import setting, clean_name
from .initialization import gcp_initailize

gcp_initailize()

class StaticFile(GoogleCloudStorage):
    location = setting('GS_STATIC_FILE_LOCATION', '')

class MediaFile(GoogleCloudStorage):
    location = setting('GS_MEDIA_FILE_LOCATION', '')

    def _save(self, name, content):
        extention = name.split('.')[-1]
        name_without_extention = "".join(name.split('.')[:-1])
        path = ""
        if len(name_without_extention.split('/')) > 1:
            path = '/'.join(name_without_extention.split('/')[:-1]) + '/'
        name = "%s%s.%s" % (
            path,
            str(uuid.uuid4()).replace('-', ''),
            extention)
        cleaned_name = clean_name(name)
        name = self._normalize_name(cleaned_name)
        content.name = cleaned_name
        if 'image' in content.__dict__:
            opened_image = PIL.Image.open(content.file)
            if opened_image.width > 1280:
                opened_image.thumbnail(
                    (1280, (opened_image.height / opened_image.width) * 1280)
                    )
                new_file_object = io.BytesIO()
                opened_image.save(new_file_object, format=extention)
                content.file = new_file_object
                content.image = opened_image
                content.size = len(new_file_object.getbuffer())
        file = GoogleCloudFile(name, 'rw', self)
        file.blob.cache_control = self.cache_control # pylint: disable=no-member
        file.blob.upload_from_file(
            content, rewind=True, size=content.size,
            content_type=file.mime_type, predefined_acl=self.default_acl) # pylint: disable=no-member
        return cleaned_name
        # cache_control and default_acl are to be initialized
