import argparse
import sys, os
def parseArgs():
    parser = argparse.ArgumentParser(prog='PxScan V1.0', description=''\
                                    '针对字典库的特殊路径进行爬取，字典库暂时只分：默认，jsp，php，asp',
                                     usage='PxScan.py [options]')
    parser.add_argument('-u', '--url', metavar='Url', type=str, default='')
    parser.add_argument('-d', '--dict', metavar='Directory', type=str, default='')
    parser.add_argument('-t', '--timeout', metavar='Timeout', type=int, default=10)
    parser.add_argument('-v', '--version', )
    parser.add_argument('-tech',metavar='Tech Engine', type=str, default='')
    if len(sys.argv) == 1 :
        sys.argv.append('-h')
    args = parser.parse_args()
    checkArgs(args)
    return args

def checkArgs(args):
    if not args.url:
        print('''
            Args Missing! -u/--url URL''')
    if args.dict and not os.path.isfile(args.dict):
        print('找不到文件%s'%args.d)
        exit(-1)