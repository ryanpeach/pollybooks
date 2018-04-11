import subprocess
import codecs
from tqdm import tqdm

def run_on_list(list_of_paragraphs,
        outdir,
        voice='Salli',
        paragraph_space="2s",
        debug=False,
        sr=16000):

    cnt = 0
    file_names = ''

    for line in tqdm(list_of_paragraphs):
        command = 'aws polly synthesize-speech --text-type ssml --output-format "mp3" --voice-id "{voice}" --text "{text}" --sample-rate {sr} {outfile}'

        rendered = '<speak><amazon:effect name=\\"drc\\">' + line.strip() + '<break time=\\"{paragraph_space}\\"/></amazon:effect></speak>'.format(paragraph_space=paragraph_space)

        file_name = ' {outdir}polly_out{suffix}.mp3'.format(outdir=outdir,suffix=u''.join(str(cnt)).encode('utf-8'))
        cnt += 1
        command = command.format(text=rendered, outfile=file_name, voice=voice, sr=sr)
        file_names += file_name
        if debug: print(command)
        subprocess.call(command, shell=True)

    if debug: print(file_names)
    outfile = '{outdir}result.mp3'.format(outdir=outdir)
    execute_command = 'cat ' + file_names + '>'+outfile
    subprocess.call(execute_command, shell=True)

    if debug: print(file_names)
    execute_command = 'rm ' + file_names
    print('Removing temporary files: ' + (execute_command if debug else ''))
    subprocess.call(execute_command, shell=True)

    return outfile

if __name__=="__main__":
    from preprocessing import remove_word_wrap, split_chapters
    remove_word_wrap("../examples/frankenstein.txt", outfile="../examples/output/frankenstein.txt")
    chapters = split_chapters("../examples/output/frankenstein.txt", outpath="../examples/output/frankenstein/frankenstein")
    run_on_list(chapters['Letter 1'], "../examples/output/mp3/")
