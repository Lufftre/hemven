import argparse
import sold

parser = argparse.ArgumentParser()
parser.add_argument('--download', help='Download new raw html pages from hemnet')
parser.add_argument('--name', help='Specify filename for dataframe', default='sold.csv')
args = parser.parse_args()

if args.download:
    sold.download()

sold.getdf().to_csv(f'out/{args.name}', index=False)
