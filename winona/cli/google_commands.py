#!/usr/bin/env python3

from ..api import read_public_google_sheet


def display_draft_sheet(sheet_url):
    print(sheet_url)
    df = read_public_google_sheet(sheet_url)
    print(df)
    return

