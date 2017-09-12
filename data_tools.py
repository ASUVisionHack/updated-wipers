"""
data_tools.py
Author: Daniel D'Souza
"""


def parse_data(filename):
    """
    parse data parses an output file, and converts it into a data structure.
    :param filename: The absolute location of your data file
    :return: data structure with information about each file
    """
    with open(filename, 'r') as data:
        results = []

        for line in data.readlines():
            name_end = line.find('.avi ') + 5

            filename = line[:name_end].rstrip()
            rest = int(line[name_end:].rstrip(), 2)
            # print(filename)
            # print('{0:6b}'.format(rest))

            result = dict(
                filename=filename,
                bridge= True if (0b100000 & rest) >> 5 else False,
                entry=  True if (0b010000 & rest) >> 4 else False,
                exit=   True if (0b001000 & rest) >> 3 else False,
                bump=   True if (0b000100 & rest) >> 2 else False,
                wipers= True if (0b000010 & rest) >> 1 else False,
                zebra=  True if (0b000001 & rest) else False,
            )
            # print(result['zebra'])
            results.append(result)

        return results


def get_data(results, bridge=False, entry=False, exit=False, wipers=False, bump=False, zebra=False, all=False):
    """
    Returns a list of video file names containing the specified events
    :param results:
    :param bridge: True if you want videos with bridges
    :param entry:
    :param exit:
    :param wipers:
    :param bump:
    :param zebra:
    :return: a list with the video file names with the events you want
    """
    assert len(results) > 0
    relevant_data = [video_data['filename'] for video_data in results if
                     (bridge and video_data['bridge']) or
                     (entry and video_data['entry']) or
                     (exit and video_data['exit']) or
                     (wipers and video_data['wipers']) or
                     (bump and video_data['bump']) or
                     (zebra and video_data['patterns']) or
                     all]

    return relevant_data


if __name__ == '__main__':
    import argparse
    import os
    parser = argparse.ArgumentParser()
    parser.add_argument('folder', help='the folder with train.txt')
    args = parser.parse_args()

    results = parse_data(args.folder+'/train.txt')

    for event in ['bridge', 'entry', 'exit', 'wipers', 'bump', 'zebra']:
        os.makedirs(event)

    for video_data in results:
        video_filename = video_data['filename']

        if video_data['bridge']:
            os.symlink(args.folder + '/' + video_filename, 'bridge/'+video_filename)
        if video_data['entry']:
            os.symlink(args.folder + '/' + video_filename, 'entry/'+video_filename)
        if video_data['exit']:
            os.symlink(args.folder + '/' + video_filename, 'exit/'+video_filename)
        if video_data['wipers']:
            os.symlink(args.folder + '/' + video_filename, 'wipers/'+video_filename)
        if video_data['bump']:
            os.symlink(args.folder + '/' + video_filename, 'bump/'+video_filename)
        if video_data['zebra']:
            os.symlink(args.folder + '/' + video_filename, 'zebra/'+video_filename)


#     res = parse_data('/home/dadsouza/Documents/ASUVisionHack/competition_data/trainset/train.txt')
#     data = get_data(res, entry=True)
#
# print(data)