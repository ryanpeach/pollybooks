import os
# from pollybooks.polly import run_on_file
# from calibre.customize import FileTypePlugin

# class HelloWorld(FileTypePlugin):

#     name                = 'Amazon Polly Program' # Name of the plugin
#     description         = 'Runs Amazon Polly on a text version of an ebook.'
#     supported_platforms = ['osx', 'linux'] # Platforms this plugin will run on
#     author              = 'Ryan Peach' # The author of this plugin
#     version             = (1, 0, 0)   # The version number of this plugin
#     file_types          = set(['txt']) # The file types that this plugin will be applied to
#     on_postprocess      = True # Run this plugin after conversion is complete
#     minimum_calibre_version = (0, 7, 53)

#     def run(self, path_to_ebook):
#         from calibre.ebooks.metadata.meta import get_metadata, set_metadata
#         file = open(path_to_ebook, 'r+b')
#         ext = os.path.splitext(path_to_ebook)[-1][1:].lower()
#         mi = get_metadata(file, ext)

#         outfile = run_on_file(path_to_ebook)

#         set_metadata(outfile, mi, 'mp3')
#         return path_to_ebook
