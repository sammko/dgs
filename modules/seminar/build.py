#!/usr/bin/python3

import argparse, yaml, os, jinja2, sys
from utils import jinjaEnv, mergeInto, renderList

parser = argparse.ArgumentParser(
    description             = "Prepare and compile a DeGeŠ round from repository",
)
parser.add_argument('seminar', choices = ['FKS', 'KMS', 'KSP', 'UFO', 'PRASK', 'FX'])
parser.add_argument('volume', type = int)
parser.add_argument('semester', type = int, choices = [1, 2])
parser.add_argument('round', type = int, choices = [1, 2, 3])
args = parser.parse_args()

thisdir = os.path.dirname(os.path.realpath(__file__))

try:
    roundDirectory = 'source/{seminar}/{volume:02d}/{semester}/{round}/'.format(seminar = args.seminar, volume = args.volume, semester = args.semester, round = args.round)

    seminarMeta     = yaml.load(open(os.path.join(roundDirectory, '..', '..', '..', 'meta.yaml'), 'r'))
    volumeMeta      = yaml.load(open(os.path.join(roundDirectory, '..', '..', 'meta.yaml'), 'r'))
    semesterMeta    = yaml.load(open(os.path.join(roundDirectory, '..', 'meta.yaml'), 'r'))
    roundMeta       = yaml.load(open(os.path.join(roundDirectory, 'meta.yaml'), 'r'))

    problemsMetas   = []
    for name in sorted(os.listdir(roundDirectory)):
        if os.path.isdir(os.path.join(roundDirectory, name)) and os.path.isfile(os.path.join(roundDirectory, name, 'meta.yaml')):
            problemMeta = yaml.load(open(os.path.join(roundDirectory, name, 'meta.yaml')))
            problemMeta['id'] = name
            problemMeta['solutionBy'] = renderList(problemMeta['solutionBy'], textbf = True)
            problemMeta['evaluation'] = renderList(problemMeta['evaluation'], textbf = True)
            problemsMetas.append(problemMeta)

except FileNotFoundError as e:
    print("Fatal: could not open file {}".format(e))
    sys.exit(-1)

context = {
    'seminar': seminarMeta,
    'semester': semesterMeta,
    'round': roundMeta,
}

style = yaml.load(open(os.path.join('modules', 'seminar', 'styles', args.seminar, 'style.yaml'), 'r'))

update = {
    'seminar': {
        'id':   args.seminar,
    },
    'volume': {
        'id':   '{:02d}'.format(args.volume),
    },
    'semester': {
        'id': args.semester,
        'nominative': ['zimná', 'letná'][args.semester - 1],
        'genitive': ['zimnej', 'letnej'][args.semester - 1],
    },
    'round': {
        'id': args.round,
        'problems': problemsMetas,
    },
}


context = mergeInto(mergeInto(context, style), update)

outputDir = 'input/{seminar}/{volume:02d}/{semester}/{round}/'.format(seminar = args.seminar, volume = args.volume, semester = args.semester, round = args.round)

for template in ['problems.tex', 'solutions.tex']:
    print(jinjaEnv(os.path.join(thisdir, 'templates')).get_template(template).render(context), file = open(os.path.join(outputDir, template), 'w'))

for template in ['root.sty']:
    print(jinjaEnv(os.path.join(thisdir, 'styles')).get_template(template).render(context), file = open(os.path.join(outputDir, template), 'w'))