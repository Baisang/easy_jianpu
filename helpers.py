import subprocess
import random
import string

def generate_random_filename(extension):
    file_name = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))
    file_name += '.' + extension
    return file_name

def convert_jianpu_to_midi(jianpu):
    pdf = convert_jianpu_to_jianpu(jianpu)
    file_slug = pdf[:len(pdf)-4]
    return '{}.midi'.format(file_slug)

def convert_jianpu_to_western(jianpu):
    ly = convert_jianpu_to_ly(jianpu, western=True)
    ly = convert_jianpuly_westernly(ly)
    return convert_ly_to_pdf(ly)

def convert_jianpu_to_jianpu(jianpu):
    ly = convert_jianpu_to_ly(jianpu)
    return convert_ly_to_pdf(ly)

def convert_jianpu_to_ly(jianpu, western=False):
    if western:
        if 'WithStaff' not in jianpu:
            jianpu = 'WithStaff\n{}'.format(jianpu)
    s = subprocess.Popen(['python2', 'jianpu-ly.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    input = jianpu.encode()
    output, _ = s.communicate(input)
    return output.decode()

def convert_ly_to_pdf(ly):
    # Write ly to a temporary file
    ly_file_name = 'output/{}'.format(generate_random_filename('ly'))
    file_slug = ly_file_name[:len(ly_file_name)-3]
    with open(ly_file_name, 'w') as f:
        f.write(ly)
    # Run lilypond using this file
    try:
        subprocess.check_output(['lilypond', '-o', file_slug, ly_file_name], stderr=subprocess.STDOUT)
    except Exception as e:
        return e
    # TODO: support like midis and stuff
    return '{}.pdf'.format(file_slug)

def convert_jianpuly_westernly(jianpuly):
    flag = 1
    new_ly = []
    for line in jianpuly.splitlines():
        # TODO: regex match this
        if 'BEGIN JIANPU STAFF' in line:
            flag = 0
        if flag:
            new_ly.append(line)
        if 'END JIANPU STAFF' in line:
            flag = 1
    return '\n'.join(new_ly)

