#!/usr/bin/env python3

import argparse, yaml, os, jinja2, sys, pprint, colorama
from build import *
from colorama import Fore, Style

args = createXParser().parse_args()

launchDirectory     = os.path.realpath(args.launch)
thisDirectory       = os.path.realpath(os.path.dirname(__file__))
outputDirectory     = os.path.realpath(args.output) if args.output else None

if args.competition is None:
    build = 'root'
    args.volume = args.semester = args.round = None
elif args.volume is None:
    build = 'competition'
    args.semester = args.round = None
elif args.semester is None:
    build = 'volume'
    args.round = None
elif args.round is None:
    build = 'semester'
else:
    build = 'round'

context = buildBookletContext(launchDirectory, args.competition, args.volume, args.semester, args.round)
if args.debug:
    pprint.pprint(context)

print(Fore.CYAN + Style.DIM + "Invoking template builder on {build} 'seminar{competition}{volume}{semester}{round}'".format(
    build       = build,
    competition = '' if args.competition    is None else '/{}'.format(args.competition),
    volume      = '' if args.volume         is None else '/{}'.format(args.volume),
    semester    = '' if args.semester       is None else '/{}'.format(args.semester),
    round       = '' if args.round          is None else '/{}'.format(args.round),
) + Style.RESET_ALL)

buildFormatTemplate(thisDirectory, 'format-{build}.tex'.format(build = build), context, outputDirectory)

print(Fore.GREEN + "Template builder successful" + Style.RESET_ALL)
