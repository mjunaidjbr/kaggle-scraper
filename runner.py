#!/usr/bin/env python

import os
import sys
import time
import logging
import argparse

import scraper

logger = logging.getLogger(__name__)


def command_line_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Run a web scraper.'
    )
    parser.add_argument(
        '-b',
        '--browser',
        type=str,
        choices=['chrome', 'firefox'],
        default='chrome',
        help='The browser to use for scraping.'
    )
    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help='Whether to enable verbose logging.'
    )
    parser.add_argument(
        '-he',
        '--headless',
        type=bool,
        default=True,
        help='Whether to run the browser in headless mode.'
    )
    return parser.parse_args()


if __name__ == '__main__':
    command_line_args = command_line_args()
    if command_line_args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    logger.info('Starting scraper...')
    try:
        sys.path.append(command_line_args.path)

        scraper.run(
            browser=command_line_args.browser,
            headless=command_line_args.headless
        )
    except Exception as e:
        logger.error(f'Error running scraper: {e}')
        sys.exit(1)
    logger.info('Scraper finished.')
    time.sleep(5)
    sys.exit(0)
