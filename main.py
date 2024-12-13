import argparse
from feed_generator import save_rss_feed
from fetch import fetch_and_generate_feed
from config import column_dict

if __name__ == "__main__":
    # test purpose can use "jxky"
    parser = argparse.ArgumentParser(
        description="Fetch and save RSS feed for a specified column."
    )
    parser.add_argument(
        "column",
        type=str,
        nargs="?",
        default="lgyw",
        help='The column to fetch the RSS feed for. Default is "lgyw".',
    )
    parser.add_argument(
        "output_file",
        type=str,
        nargs="?",
        default="rss_feed.xml",
        help="Output file to save the RSS feed.",
    )

    args = parser.parse_args()

    fg = fetch_and_generate_feed(args.column)
    if fg:
        save_rss_feed(fg, args.output_file)
