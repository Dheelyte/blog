from cloudinary_storage.storage import MediaCloudinaryStorage


class CKEditorCloudinaryStorage(MediaCloudinaryStorage):

    def _save(self, name, content):
        # === THE FIX ===
        # Reset the file pointer to the beginning.
        # This is necessary because CKEditor's validation process read the file
        # and left the pointer at the end.
        if hasattr(content, 'seek'):
            content.seek(0)

        # 2. Fix the Folder Organization:
        # Since we can't pass 'location' in __init__, we prepend the folder 
        # to the filename here. Cloudinary treats path slashes as folders.
        if not name.startswith('ckeditor/'):
            name = f'ckeditor/{name}'
            
        return super()._save(name, content)